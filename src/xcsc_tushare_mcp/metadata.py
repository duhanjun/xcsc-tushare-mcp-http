"""
元数据模块

该模块负责 API 元数据的生成、缓存和加载。

主要功能：
1. 解析 references/ 目录中的 Markdown 文档
2. 提取 API 信息（名称、描述、参数、返回值等）
3. 检测 references/ 目录变化，自动重新生成元数据
4. 缓存元数据到 api_metadata.json 文件

这样项目具备动态更新能力，只需维护 references/ 目录中的 .md 文件，
服务器启动时会自动检测变化并重新生成元数据。

使用示例：
    >>> from xcsc_tushare_mcp.metadata import load_api_metadata
    >>> metadata = load_api_metadata()
    >>> print(f"共有 {metadata['total_apis']} 个 API")
    >>> 
    >>> # 强制重新加载（忽略缓存）
    >>> metadata = load_api_metadata(force_reload=True)
"""

import os
import re
import json
import hashlib
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime


# 全局缓存
_metadata_cache: Optional[Dict[str, Any]] = None
_metadata_hash: Optional[str] = None


def _get_references_dir() -> Path:
    """
    获取 references 目录路径
    
    Returns:
        Path: references 目录的绝对路径
    """
    return Path(__file__).parent / "references"


def _get_metadata_file() -> Path:
    """
    获取元数据文件路径
    
    Returns:
        Path: api_metadata.json 文件的绝对路径
    """
    return Path(__file__).parent / "api_metadata.json"


def _calculate_references_hash() -> str:
    """
    计算 references 目录的哈希值
    
    用于检测目录内容是否发生变化。计算方式：
    1. 遍历所有 .md 文件
    2. 将文件相对路径和修改时间加入哈希计算
    
    Returns:
        str: 目录内容的 MD5 哈希值
    """
    references_dir = _get_references_dir()
    hasher = hashlib.md5()
    
    for md_file in sorted(references_dir.rglob("*.md")):
        relative_path = md_file.relative_to(references_dir)
        hasher.update(str(relative_path).encode())
        
        mtime = md_file.stat().st_mtime
        hasher.update(str(mtime).encode())
    
    return hasher.hexdigest()


def _parse_markdown_table(content: str) -> List[Dict[str, str]]:
    """
    解析 Markdown 表格
    
    从 Markdown 内容中提取所有表格，返回表格数据列表。
    每个表格是一个字典列表，字典的键是表头，值是单元格内容。
    
    Args:
        content: Markdown 文本内容
    
    Returns:
        List[Dict[str, str]]: 表格数据列表
    """
    lines = content.split('\n')
    tables = []
    current_table = []
    in_table = False
    headers = []
    
    for line in lines:
        if '|' in line and line.strip().startswith('|'):
            if not in_table:
                in_table = True
                headers = [h.strip().replace('\\', '') for h in line.split('|')[1:-1]]
            else:
                if '---' in line:
                    continue
                cells = [c.strip().replace('\\', '') for c in line.split('|')[1:-1]]
                if len(cells) == len(headers):
                    current_table.append(dict(zip(headers, cells)))
        else:
            if in_table and current_table:
                tables.append(current_table)
                current_table = []
            in_table = False
    
    if current_table:
        tables.append(current_table)
    
    return tables


def _extract_limit_info(content: str) -> str:
    """
    提取限量信息
    
    从 Markdown 内容中提取 API 的限量/权限信息。
    
    Args:
        content: Markdown 文本内容
    
    Returns:
        str: 限量信息，如果未找到则返回 "无限制"
    """
    content = content.replace('\\', '')
    patterns = [
        r'限量[：:]\s*(.+?)(?:\n|$)',
        r'权限[：:]\s*(.+?)(?:\n|$)',
        r'单次[：:]\s*(.+?)(?:\n|$)',
    ]
    for pattern in patterns:
        match = re.search(pattern, content)
        if match:
            return match.group(1).strip()
    return "无限制"


def _extract_permission_info(content: str) -> str:
    """
    提取权限信息
    
    从 Markdown 内容中提取 API 的权限要求信息。
    
    Args:
        content: Markdown 文本内容
    
    Returns:
        str: 权限信息，如果未找到则返回 "基础权限"
    """
    content = content.replace('\\', '')
    patterns = [
        r'权限要求[：:]\s*(.+?)(?:\n|$)',
        r'需要权限[：:]\s*(.+?)(?:\n|$)',
        r'积分[：:]\s*(.+?)(?:\n|$)',
    ]
    for pattern in patterns:
        match = re.search(pattern, content)
        if match:
            return match.group(1).strip()
    return "基础权限"


def _parse_reference_doc(file_path: Path, references_dir: Path, category: str) -> Optional[Dict[str, Any]]:
    """
    解析单个 reference 文档
    
    从 Markdown 文件中提取 API 信息，包括：
    - API 名称
    - 描述
    - 限量/权限信息
    - 输入参数
    - 输出参数
    - 示例
    
    Args:
        file_path: Markdown 文件路径
        references_dir: references 目录路径
        category: API 分类
    
    Returns:
        Optional[Dict[str, Any]]: API 信息字典，如果解析失败则返回 None
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 提取接口名称（处理转义字符 \_）
        interface_match = re.search(r'接口[：:]\s*([a-zA-Z_\\][a-zA-Z0-9_\\]*)', content)
        if not interface_match:
            return None
        
        api_name = interface_match.group(1).replace('\\', '')
        
        # 提取描述
        desc_match = re.search(r'描述[：:]\s*(.+?)(?:\n|$)', content)
        description = desc_match.group(1).strip().replace('\\', '') if desc_match else ""
        
        # 提取限量和权限信息
        limit = _extract_limit_info(content)
        permission = _extract_permission_info(content)
        
        # 解析表格
        tables = _parse_markdown_table(content)
        
        input_params = []
        output_params = []
        
        for table in tables:
            if not table:
                continue
            first_row = table[0]
            
            # 输入参数表（包含"必选"列）
            if '必选' in first_row:
                for row in table:
                    name = row.get('名称', '')
                    param_type = row.get('类型', '')
                    required = row.get('必选', '')
                    desc = row.get('描述', '')
                    if name and not name.startswith('---'):
                        input_params.append({
                            'name': name,
                            'type': param_type,
                            'required': required == 'Y',
                            'description': desc
                        })
            # 输出参数表（包含"默认显示"列）
            elif '默认显示' in first_row:
                for row in table:
                    name = row.get('名称', '')
                    param_type = row.get('类型', '')
                    desc = row.get('描述', '')
                    if name and not name.startswith('---'):
                        output_params.append({
                            'name': name,
                            'type': param_type,
                            'description': desc
                        })
        
        # 生成示例参数
        example_params = {}
        for param in input_params[:3]:
            if param['required']:
                if 'ts_code' in param['name']:
                    example_params[param['name']] = '000001.SZ'
                elif 'date' in param['name'].lower():
                    example_params[param['name']] = '20240101'
                elif 'exchange' in param['name'].lower():
                    example_params[param['name']] = 'SSE'
        
        example = f"get_api_query('{api_name}', '{json.dumps(example_params, ensure_ascii=False)}')" if example_params else f"get_api_query('{api_name}')"
        
        # 使用相对于 references 目录的相对路径，添加 references/ 前缀
        relative_path = file_path.relative_to(references_dir)
        source_file = "references/" + str(relative_path).replace('\\', '/')
        
        return {
            'api_name': api_name,
            'description': description,
            'category': category,
            'limit': limit,
            'permission': permission,
            'input_params': input_params,
            'output_params': output_params,
            'example': example,
            'source_file': source_file
        }
    except Exception as e:
        print(f"解析 {file_path} 失败: {e}")
        return None


def generate_api_metadata() -> Dict[str, Any]:
    """
    从 references 目录生成 API 元数据
    
    遍历 references/ 目录中的所有 .md 文件，解析 API 信息并生成元数据。
    
    Returns:
        Dict[str, Any]: 包含以下字段的字典：
            - version: 元数据版本
            - generated_at: 生成时间
            - total_apis: API 总数
            - apis: API 信息字典，键为 api_name
    """
    references_dir = _get_references_dir()
    metadata = {}
    
    for md_file in references_dir.rglob('*.md'):
        try:
            relative_path = md_file.relative_to(references_dir)
            category = str(relative_path.parent).replace('\\', '_').replace('/', '_')
            
            parsed = _parse_reference_doc(md_file, references_dir, category)
            if parsed:
                api_name = parsed['api_name']
                metadata[api_name] = parsed
        except Exception as e:
            print(f"解析 {md_file} 失败: {e}")
    
    return {
        'version': '1.0.1',
        'generated_at': datetime.now().isoformat(),
        'total_apis': len(metadata),
        'apis': metadata,
    }


def save_api_metadata(metadata: Dict[str, Any]) -> None:
    """
    保存 API 元数据到文件
    
    将元数据保存到 api_metadata.json 文件。
    
    Args:
        metadata: API 元数据字典
    """
    metadata_file = _get_metadata_file()
    with open(metadata_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)


def load_api_metadata(force_reload: bool = False) -> Dict[str, Any]:
    """
    加载 API 元数据
    
    如果 references 目录有变化，自动重新生成元数据。
    使用全局缓存避免重复加载。
    
    Args:
        force_reload: 是否强制重新加载，忽略缓存，默认 False
    
    Returns:
        Dict[str, Any]: API 元数据字典
    
    使用示例：
        >>> metadata = load_api_metadata()
        >>> print(f"共有 {metadata['total_apis']} 个 API")
        >>> 
        >>> # 强制重新加载
        >>> metadata = load_api_metadata(force_reload=True)
    """
    global _metadata_cache, _metadata_hash
    
    if _metadata_cache is not None and not force_reload:
        return _metadata_cache
    
    references_dir = _get_references_dir()
    metadata_file = _get_metadata_file()
    
    current_hash = _calculate_references_hash()
    
    need_generate = False
    
    if not metadata_file.exists():
        need_generate = True
        print(f"元数据文件不存在，正在生成...")
    elif _metadata_hash is None or current_hash != _metadata_hash:
        need_generate = True
        print(f"检测到 references 目录变化，正在更新元数据...")
    
    if need_generate:
        metadata = generate_api_metadata()
        save_api_metadata(metadata)
        _metadata_hash = current_hash
        _metadata_cache = metadata
        print(f"元数据已生成: {metadata['total_apis']} 个 API")
    else:
        with open(metadata_file, 'r', encoding='utf-8') as f:
            _metadata_cache = json.load(f)
        _metadata_hash = current_hash
    
    return _metadata_cache
