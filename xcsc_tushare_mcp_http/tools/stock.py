"""
股票基础数据工具模块

该模块提供股票基础信息相关的数据查询工具，包括：
- 股票基本资料查询
- 股票曾用名查询
- 公司简介查询
- 管理层信息查询
- 交易日历查询

这些工具主要用于获取股票的基本信息和元数据。
"""

from typing import Any, Dict, Optional

from .base import format_dataframe, format_error


def register_stock_tools(mcp, pro):
    """
    注册股票基础数据工具到 MCP 服务器

    该函数注册所有股票基础数据相关的工具，包括股票基本资料、
    曾用名、公司简介、管理层信息和交易日历等。

    Args:
        mcp: FastMCP 服务器实例
        pro: XCSC Tushare Pro API 实例
    """

    @mcp.tool()
    def get_stock_basic(
        ts_code: Optional[str] = None,
        exchange: Optional[str] = None,
        is_shsc: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取中国A股基本资料

        获取沪深A股上市公司的基本资料信息，包括公司名称、所属行业、
        上市日期、交易所等基本信息。

        Args:
            ts_code: TS代码（多个代码用逗号分隔），如 "000001.SZ,600000.SH"
            exchange: 交易所代码（SSE上交所 SZSE深交所）
            is_shsc: 是否沪深港通标的（N否 H沪股通 S深股通）
            start_date: 开始日期（YYYYMMDD格式）
            end_date: 结束日期（YYYYMMDD格式）
            fields: 返回字段（用逗号分隔，默认返回所有字段）

        Returns:
            Dict[str, Any]: 包含股票基本资料的字典，格式如下：
                {
                    "success": True,
                    "data": [
                        {
                            "ts_code": "000001.SZ",
                            "symbol": "000001",
                            "name": "平安银行",
                            "comp_name": "平安银行股份有限公司",
                            "exchange": "SZSE",
                            "area": "深圳",
                            "industry": "银行",
                            "market": "主板",
                            "list_date": "19910403",
                            ...
                        }
                    ],
                    "count": 1,
                    "columns": ["ts_code", "symbol", "name", ...]
                }
        """
        try:
            kwargs = {}
            if ts_code:
                kwargs["ts_code"] = ts_code
            if exchange:
                kwargs["exchange"] = exchange
            if is_shsc:
                kwargs["is_shsc"] = is_shsc
            if start_date:
                kwargs["start_date"] = start_date
            if end_date:
                kwargs["end_date"] = end_date
            if fields:
                kwargs["fields"] = fields
            df = pro.stock_basic(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_name_change(
        ts_code: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取中国A股证券曾用名

        获取沪深A股上市公司历史上的曾用名变更记录，
        包括变更日期、变更前后的名称等信息。

        Args:
            ts_code: TS代码（多个代码用逗号分隔）
            start_date: 开始日期（YYYYMMDD格式）
            end_date: 结束日期（YYYYMMDD格式）
            fields: 返回字段（用逗号分隔）

        Returns:
            Dict[str, Any]: 包含证券曾用名变更记录的字典
        """
        try:
            kwargs = {}
            if ts_code:
                kwargs["ts_code"] = ts_code
            if start_date:
                kwargs["start_date"] = start_date
            if end_date:
                kwargs["end_date"] = end_date
            if fields:
                kwargs["fields"] = fields
            df = pro.namechange(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_stock_company(
        ts_code: Optional[str] = None,
        exchange: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取中国A股公司简介

        获取沪深A股上市公司的详细公司简介，包括主营业务、
        公司简介、经营范围等信息。

        Args:
            ts_code: TS代码（多个代码用逗号分隔）
            exchange: 交易所代码（SSE上交所 SZSE深交所）
            fields: 返回字段（用逗号分隔）

        Returns:
            Dict[str, Any]: 包含公司简介信息的字典
        """
        try:
            kwargs = {}
            if ts_code:
                kwargs["ts_code"] = ts_code
            if exchange:
                kwargs["exchange"] = exchange
            if fields:
                kwargs["fields"] = fields
            df = pro.stock_company(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_stk_managers(
        ts_code: Optional[str] = None,
        ann_date: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取上市公司管理层

        获取沪深A股上市公司的管理层人员信息，包括董事、监事、
        高管等人员的姓名、职务、任职日期等信息。

        Args:
            ts_code: TS代码（多个代码用逗号分隔）
            ann_date: 公告日期（YYYYMMDD格式）
            start_date: 开始日期（YYYYMMDD格式）
            end_date: 结束日期（YYYYMMDD格式）
            fields: 返回字段（用逗号分隔）

        Returns:
            Dict[str, Any]: 包含管理层信息的字典
        """
        try:
            kwargs = {}
            if ts_code:
                kwargs["ts_code"] = ts_code
            if ann_date:
                kwargs["ann_date"] = ann_date
            if start_date:
                kwargs["start_date"] = start_date
            if end_date:
                kwargs["end_date"] = end_date
            if fields:
                kwargs["fields"] = fields
            df = pro.stk_managers(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_stk_managers_salary(
        ts_code: Optional[str] = None,
        ann_date: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取管理层薪酬和持股

        获取沪深A股上市公司管理层的薪酬和持股信息，
        包括年薪、持股数量等数据。

        Args:
            ts_code: TS代码（多个代码用逗号分隔）
            ann_date: 公告日期（YYYYMMDD格式）
            start_date: 开始日期（YYYYMMDD格式）
            end_date: 结束日期（YYYYMMDD格式）
            fields: 返回字段（用逗号分隔）

        Returns:
            Dict[str, Any]: 包含管理层薪酬和持股信息的字典
        """
        try:
            kwargs = {}
            if ts_code:
                kwargs["ts_code"] = ts_code
            if ann_date:
                kwargs["ann_date"] = ann_date
            if start_date:
                kwargs["start_date"] = start_date
            if end_date:
                kwargs["end_date"] = end_date
            if fields:
                kwargs["fields"] = fields
            df = pro.stk_managers_salary(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_trade_calendar(
        exchange: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        is_open: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取各大交易所交易日历

        获取沪深交易所、中金所等各大交易所的交易日历信息，
        包括日期、是否开市、上一交易日等信息。

        Args:
            exchange: 交易所代码（SSE上交所 SZSE深交所 CFFEX中金所 DCE大商所 CZCE郑商所 SHFE上期所 INE上能源）
            start_date: 开始日期（YYYYMMDD格式）
            end_date: 结束日期（YYYYMMDD格式）
            is_open: 是否交易（0休市 1交易）
            fields: 返回字段（用逗号分隔）

        Returns:
            Dict[str, Any]: 包含交易日历信息的字典，格式如下：
                {
                    "success": True,
                    "data": [
                        {
                            "exchange": "SSE",
                            "cal_date": "20240101",
                            "is_open": 0,
                            "pretrade_date": "20231229"
                        }
                    ],
                    "count": 1,
                    "columns": ["exchange", "cal_date", "is_open", "pretrade_date"]
                }
        """
        try:
            kwargs = {}
            if exchange:
                kwargs["exchange"] = exchange
            if start_date:
                kwargs["start_date"] = start_date
            if end_date:
                kwargs["end_date"] = end_date
            if is_open:
                kwargs["is_open"] = is_open
            if fields:
                kwargs["fields"] = fields
            df = pro.trade_cal(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)
