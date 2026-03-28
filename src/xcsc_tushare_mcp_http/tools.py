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
        获取所有 API 的列表信息

        【调用时机】
        - 用户询问"有哪些数据可以查询"、"能查什么数据"时
        - 用户想了解某个分类下有哪些具体接口时
        - 不确定某个数据需求应该使用哪个 API 时
        - 需要浏览所有可用数据接口时

        【返回内容】
        返回所有 API 的名称、描述和分类，共 91 个接口，涵盖：
        - 沪深股票：基础数据、行情数据、财务数据、市场参考数据
        - 指数：指数行情、指数成分、成分权重、市场交易统计等
        - 公募基金：基金列表、净值、持仓、分红、管理人等
        - 共同基金：基金资料、净值、投资组合、业绩基准等
        - 期货：合约信息、日线行情、持仓排名、仓单日报、结算参数等
        - 期权：合约信息、日线行情
        - 债券：中国债券基本资料、可转债基本信息、行情、发行、赎回回售信息等

        【使用建议】
        获取列表后，根据用户需求找到合适的 api_name，然后调用 get_api_doc() 获取详细参数说明。

        Returns:
            Dict[str, Any]: 包含 API 列表的响应
                - success: 是否成功
                - total_apis: API 总数
                - data: API 字典，key 为 api_name，value 包含 api_name、description、category
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

        【调用时机】
        - 已确定要使用的 api_name，需要了解具体参数要求时
        - 查询失败，需要确认参数格式是否正确时
        - 用户想了解某个接口返回哪些字段时
        - 需要查看接口示例代码时

        【返回内容】
        返回指定 API 的完整文档，包括：
        - description: 接口描述
        - category: 所属分类
        - limit: 单次查询最大条数限制
        - permission: 所需权限
        - input_params: 输入参数列表（名称、类型、是否必选、描述）
        - output_params: 输出字段列表（名称、类型、描述）
        - example: 调用示例

        【使用建议】
        仔细阅读 input_params 中的参数要求，特别是必选参数和格式要求，
        然后构造正确的 params 参数调用 get_api_query()。

        Args:
            api_name: API 名称，如 "stock_basic"、"daily"、"income" 等
                      必须是 get_api_list() 返回的有效 API 名称

        Returns:
            Dict[str, Any]: 包含 API 详细文档的响应
                - success: 是否成功
                - data: API 详细信息（成功时）
                - error: 错误信息（失败时）
                - hint: 提示信息（失败时）
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
        执行通用查询 API，获取实际数据

        【调用时机】
        - 已通过 get_api_list() 确定要使用的 api_name
        - 已通过 get_api_doc() 了解参数要求
        - 已构造好符合格式要求的 params 参数
        - 准备获取实际数据时

        【参数格式要求】★★★ 重要 ★★★

        1. 日期格式：
           - 格式：YYYYMMDD（8位数字字符串）
           - 示例："20240101"、"20231231"
           - 错误示例："2024-01-01"、"2024/01/01"、"01-01-2024"

        2. 股票代码格式：
           - 格式：代码.交易所后缀
           - 上交所：代码.SH（如 "600000.SH"、"000001.SH"）
           - 深交所：代码.SZ（如 "000001.SZ"、"002415.SZ"）
           - 多个代码用逗号分隔："000001.SZ,600000.SH"

        3. 指数代码格式：
           - 格式：指数代码.交易所后缀
           - 示例："000001.SH"（上证指数）、"399001.SZ"（深证成指）
           - 中证指数："000300.CSI"（沪深300）

        4. 期货合约代码格式：
           - 格式：合约代码.交易所
           - 上期所(SHF)：如 "CU2401.SHF"（铜2401合约）
           - 大商所(DCE)：如 "M2401.DCE"（豆粕2401合约）
           - 郑商所(CZCE)：如 "CF401.CZCE"（棉花401合约）
           - 中金所(CFFEX)：如 "IF2401.CFFEX"（沪深300股指期货）
           - 能源中心(INE)：如 "SC2401.INE"（原油期货）

        5. 基金代码格式：
           - 格式：基金代码.交易所后缀
           - 示例："165509.SZ"、"510300.SH"

        6. 交易所代码：
           - SSE：上交所
           - SZSE：深交所
           - SHF：上期所
           - DCE：大商所
           - CZCE：郑商所
           - CFFEX：中金所
           - INE：能源中心

        【常见参数说明】

        | 参数名 | 说明 | 示例 |
        |--------|------|------|
        | ts_code | TS代码（股票/指数/基金/合约代码） | "000001.SZ" |
        | trade_date | 交易日期 | "20240101" |
        | start_date | 开始日期 | "20240101" |
        | end_date | 结束日期 | "20241231" |
        | ann_date | 公告日期 | "20240315" |
        | report_period | 报告期（季度末日期） | "20231231" |
        | exchange | 交易所 | "SSE"、"SZSE"、"SHF" |

        【params 参数构造示例】

        示例1 - 查询单只股票日行情：
        '{"ts_code": "000001.SZ", "start_date": "20240101", "end_date": "20240131"}'

        示例2 - 查询某日全部股票行情：
        '{"trade_date": "20240115"}'

        示例3 - 查询股票基本信息：
        '{"ts_code": "000001.SZ,600000.SH"}'

        示例4 - 查询财务报表：
        '{"ts_code": "600000.SH", "report_period": "20231231", "report_type": "1"}'

        示例5 - 查询期货日线：
        '{"ts_code": "CU2401.SHF", "start_date": "20240101", "end_date": "20240131"}'

        示例6 - 查询基金净值：
        '{"ts_code": "165509.SZ"}'

        示例7 - 无参数查询（获取全部列表）：
        不传 params 或 params=null

        【注意事项】★★★ 重要 ★★★

        1. params 必须是有效的 JSON 字符串，注意引号转义
        2. 日期必须是 YYYYMMDD 格式，不要使用其他格式
        3. 代码必须带交易所后缀（.SZ、.SH 等）
        4. 每个接口有单次查询条数限制，详见 get_api_doc() 返回的 limit 字段
        5. 部分接口需要特定权限，详见 get_api_doc() 返回的 permission 字段
        6. 查询前建议先调用 get_api_doc() 确认参数要求

        Args:
            api_name: API 名称，必须是 get_api_list() 返回的有效名称
            params: JSON 格式的参数字符串，可为 None

        Returns:
            Dict[str, Any]: 包含查询结果的响应
                - success: 是否成功
                - data: 数据列表（成功时）
                - count: 数据条数
                - columns: 列名列表
                - error: 错误信息（失败时）
                - hint: 提示信息（失败时）
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
                "hint": "params 必须是有效的 JSON 字符串，注意引号格式",
            }
        except AttributeError:
            return {
                "success": False,
                "error": f"API '{api_name}' 不存在",
                "hint": "请通过 get_api_list() 查看可用的 API",
            }
        except Exception as e:
            return format_error(e)
