"""
工具模块

该模块提供三个核心 MCP 工具，用于与 XCSC Tushare API 交互：
1. get_api_list: 获取所有 API 的简化列表
2. get_api_doc: 获取指定 API 的详细文档
3. get_api_query: 通用查询接口

同时提供基础函数：
- format_dataframe: 格式化 DataFrame 为标准响应
- format_error: 格式化异常为标准错误响应

使用流程：
1. 调用 get_api_list() 获取所有可用 API
2. 调用 get_api_doc(api_name) 获取 API 详细文档（参数说明）
3. 调用 get_api_query(api_name, params) 执行查询

示例：
    >>> # 获取 API 列表
    >>> result = get_api_list()
    >>> print(result['data'].keys())
    
    >>> # 获取 API 文档
    >>> doc = get_api_doc("stock_basic")
    >>> print(doc['data']['input_params'])
    
    >>> # 执行查询
    >>> result = get_api_query("stock_basic", '{"ts_code": "000001.SZ"}')
    >>> print(result['data'])
"""

import json
import logging
from typing import Any, Dict, Optional

import pandas as pd

from .metadata import load_api_metadata

# 模块级日志器
logger = logging.getLogger(__name__)


def format_dataframe(df: Optional[pd.DataFrame]) -> Dict[str, Any]:
    """
    格式化 DataFrame 为标准 JSON 响应
    
    将 pandas DataFrame 转换为统一的字典格式，处理 NaN 值和特殊类型。
    
    Args:
        df: API 返回的 DataFrame，可能为 None 或空
    
    Returns:
        Dict[str, Any]: 标准化响应，包含以下字段：
            - success: 是否成功
            - data: 数据列表（字典列表）
            - count: 数据条数
            - columns: 列名列表
    """
    if df is None or df.empty:
        return {
            "success": True,
            "data": [],
            "count": 0,
            "columns": [],
        }

    df = df.fillna("")
    data = df.to_dict(orient="records")

    for record in data:
        for key, value in record.items():
            if pd.isna(value):
                record[key] = None
            elif hasattr(value, "item"):
                record[key] = value.item()
            elif isinstance(value, (pd.Timestamp, pd.Timedelta)):
                record[key] = str(value)

    return {
        "success": True,
        "data": data,
        "count": len(data),
        "columns": list(df.columns),
    }


def format_error(error: Exception) -> Dict[str, Any]:
    """
    格式化异常为标准错误响应
    
    将异常对象转换为统一的错误响应格式，并记录错误日志。
    
    Args:
        error: 异常对象
    
    Returns:
        Dict[str, Any]: 标准化错误响应
    """
    error_msg = str(error)
    logger.error(f"API 错误: {error_msg}")
    return {
        "success": False,
        "error": error_msg,
        "data": [],
        "count": 0,
        "columns": [],
    }


def register_tools(mcp, pro):
    """
    注册工具到 MCP 服务器
    
    将三个核心工具（get_api_list、get_api_doc、get_api_query）
    注册到 FastMCP 服务器实例。
    
    Args:
        mcp: FastMCP 服务器实例
        pro: XCSC Tushare Pro API 实例
    """

    @mcp.tool()
    def get_api_list() -> Dict[str, Any]:
        """
        获取所有 API 的简化列表

        返回所有 API 的名称、描述和分类，帮助大模型快速了解有哪些接口可用。

        Returns:
            Dict[str, Any]: 包含 API 列表的响应
        """
        try:
            metadata = load_api_metadata()
            apis = metadata.get("apis", {})
            
            simplified_apis = {}
            for api_name, doc in apis.items():
                simplified_apis[api_name] = {
                    "api_name": api_name,
                    "description": doc.get("description", ""),
                    "category": doc.get("category", ""),
                }
            
            return {
                "success": True,
                "total_apis": len(simplified_apis),
                "data": simplified_apis,
            }
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_api_doc(api_name: str) -> Dict[str, Any]:
        """
        获取指定 API 的详细文档

        返回指定 API 的完整文档，包括描述、参数、输出字段等。

        Args:
            api_name: API 名称，如 "stock_basic"

        Returns:
            Dict[str, Any]: 包含 API 详细文档的响应
        """
        try:
            metadata = load_api_metadata()
            apis = metadata.get("apis", {})
            
            if api_name not in apis:
                return {
                    "success": False,
                    "error": f"未找到 API '{api_name}'",
                    "hint": "请使用 get_api_list() 查看所有可用的 API 名称",
                }
            
            return {
                "success": True,
                "data": apis[api_name],
            }
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_api_query(api_name: str, params: Optional[str] = None) -> Dict[str, Any]:
        """
        通用 API 查询接口

        调用底层 XCSC Tushare API 获取数据。

        Args:
            api_name: API 名称，如 "stock_basic"
            params: JSON 格式的参数字符串，如 '{"ts_code": "000001.SZ"}'

        Returns:
            Dict[str, Any]: 包含查询结果的响应
        """
        try:
            kwargs = {}
            if params:
                kwargs = json.loads(params)
            
            df = getattr(pro, api_name)(**kwargs)
            return format_dataframe(df)
        except json.JSONDecodeError as e:
            return {
                "success": False,
                "error": f"参数 JSON 解析失败: {str(e)}",
                "hint": "params 必须是有效的 JSON 字符串",
            }
        except AttributeError:
            return {
                "success": False,
                "error": f"API '{api_name}' 不存在",
                "hint": "请通过 get_api_list() 查看可用的 API",
            }
        except Exception as e:
            return format_error(e)
