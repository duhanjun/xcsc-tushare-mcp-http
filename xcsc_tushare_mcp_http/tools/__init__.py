"""
工具模块初始化文件

该模块作为工具模块的入口点，导出所有子模块的工具注册函数。
通过 register_all_tools 函数，可以一次性注册所有数据类型的工具。

支持的工具模块：
- stock: 股票基础数据工具
- stock_quote: 股票行情数据工具
- stock_finance: 股票财务数据工具
- stock_market: 股票市场参考数据工具
- index: 指数相关数据工具
- fund: 公募基金数据工具
- mutual_fund: 共同基金数据工具
- futures: 期货相关数据工具
- option: 期权相关数据工具
- bond: 债券相关数据工具
- common: 通用工具（API列表、文档查询、连接测试）
"""

from .base import format_dataframe, format_error
from .stock import register_stock_tools
from .stock_quote import register_stock_quote_tools
from .stock_finance import register_stock_finance_tools
from .stock_market import register_stock_market_tools
from .index import register_index_tools
from .fund import register_fund_tools
from .mutual_fund import register_mutual_fund_tools
from .futures import register_futures_tools
from .option import register_option_tools
from .bond import register_bond_tools
from .common import register_common_tools


def register_all_tools(mcp, pro):
    """
    注册所有工具到 MCP 服务器

    该函数依次调用各个数据类型的注册函数，
    将所有 XCSC Tushare 数据接口注册为 MCP 工具。

    Args:
        mcp: FastMCP 服务器实例
        pro: XCSC Tushare Pro API 实例
    """
    register_common_tools(mcp, pro)
    register_stock_tools(mcp, pro)
    register_stock_quote_tools(mcp, pro)
    register_stock_finance_tools(mcp, pro)
    register_stock_market_tools(mcp, pro)
    register_index_tools(mcp, pro)
    register_fund_tools(mcp, pro)
    register_mutual_fund_tools(mcp, pro)
    register_futures_tools(mcp, pro)
    register_option_tools(mcp, pro)
    register_bond_tools(mcp, pro)
