"""
指数数据工具模块

该模块提供指数相关的数据查询工具，包括：
- 指数日线/周线/月线行情查询
- 指数成分和权重查询
- 指数成份股查询
- 大盘指数每日指标查询
- 市场每日交易统计查询
- 深圳市场每日交易概况查询

这些工具主要用于获取各类市场指数的行情和成分信息。
"""

from typing import Any, Dict, Optional

from .base import format_dataframe, format_error


def register_index_tools(mcp, pro):
    """
    注册指数数据工具到 MCP 服务器

    该函数注册所有指数相关的工具，包括指数日线、周线、月线行情、
    指数成分权重、指数成份股、市场统计等。

    Args:
        mcp: FastMCP 服务器实例
        pro: XCSC Tushare Pro API 实例
    """

    @mcp.tool()
    def get_index_daily(
        ts_code: Optional[str] = None,
        trade_date: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取A股指数日行情

        获取A股各类指数的日线行情数据，包括上证指数、深证成指、
        创业板指、沪深300等主要指数。

        Args:
            ts_code: 指数代码（多个代码用逗号分隔），如 "000001.SH,399001.SZ"
            trade_date: 交易日期（YYYYMMDD格式）
            start_date: 开始日期（YYYYMMDD格式）
            end_date: 结束日期（YYYYMMDD格式）
            fields: 返回字段（用逗号分隔）

        Returns:
            Dict[str, Any]: 包含指数日线行情数据的字典，格式如下：
                {
                    "success": True,
                    "data": [
                        {
                            "ts_code": "000001.SH",
                            "trade_date": "20240102",
                            "close": 2972.78,
                            "open": 2962.28,
                            "high": 2976.27,
                            "low": 2962.28,
                            "pre_close": 2974.93,
                            "change": -2.15,
                            "pct_chg": -0.07,
                            "vol": 251216000,
                            "amount": 307266000000
                        }
                    ],
                    "count": 1,
                    "columns": ["ts_code", "trade_date", "close", ...]
                }
        """
        try:
            kwargs = {}
            if ts_code:
                kwargs["ts_code"] = ts_code
            if trade_date:
                kwargs["trade_date"] = trade_date
            if start_date:
                kwargs["start_date"] = start_date
            if end_date:
                kwargs["end_date"] = end_date
            if fields:
                kwargs["fields"] = fields
            df = pro.index_daily(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_index_weekly(
        ts_code: Optional[str] = None,
        trade_date: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取指数周线行情

        获取A股各类指数的周线行情数据。

        Args:
            ts_code: 指数代码（多个代码用逗号分隔）
            trade_date: 交易日期（YYYYMMDD格式）
            start_date: 开始日期（YYYYMMDD格式）
            end_date: 结束日期（YYYYMMDD格式）
            fields: 返回字段（用逗号分隔）

        Returns:
            Dict[str, Any]: 包含指数周线行情数据的字典
        """
        try:
            kwargs = {}
            if ts_code:
                kwargs["ts_code"] = ts_code
            if trade_date:
                kwargs["trade_date"] = trade_date
            if start_date:
                kwargs["start_date"] = start_date
            if end_date:
                kwargs["end_date"] = end_date
            if fields:
                kwargs["fields"] = fields
            df = pro.index_weekly(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_index_monthly(
        ts_code: Optional[str] = None,
        trade_date: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取指数月线行情

        获取A股各类指数的月线行情数据。

        Args:
            ts_code: 指数代码（多个代码用逗号分隔）
            trade_date: 交易日期（YYYYMMDD格式）
            start_date: 开始日期（YYYYMMDD格式）
            end_date: 结束日期（YYYYMMDD格式）
            fields: 返回字段（用逗号分隔）

        Returns:
            Dict[str, Any]: 包含指数月线行情数据的字典
        """
        try:
            kwargs = {}
            if ts_code:
                kwargs["ts_code"] = ts_code
            if trade_date:
                kwargs["trade_date"] = trade_date
            if start_date:
                kwargs["start_date"] = start_date
            if end_date:
                kwargs["end_date"] = end_date
            if fields:
                kwargs["fields"] = fields
            df = pro.index_monthly(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_index_weight(
        index_code: Optional[str] = None,
        trade_date: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取指数成分和权重

        获取各类指数的成分股及其权重数据，包括沪深300、中证500、
        上证50等主要指数的成分股权重信息。

        Args:
            index_code: 指数代码，如 "000300.SH"（沪深300）
            trade_date: 交易日期（YYYYMMDD格式）
            start_date: 开始日期（YYYYMMDD格式）
            end_date: 结束日期（YYYYMMDD格式）
            fields: 返回字段（用逗号分隔）

        Returns:
            Dict[str, Any]: 包含指数成分和权重数据的字典
        """
        try:
            kwargs = {}
            if index_code:
                kwargs["index_code"] = index_code
            if trade_date:
                kwargs["trade_date"] = trade_date
            if start_date:
                kwargs["start_date"] = start_date
            if end_date:
                kwargs["end_date"] = end_date
            if fields:
                kwargs["fields"] = fields
            df = pro.index_weight(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_index_basic(
        ts_code: Optional[str] = None,
        market: Optional[str] = None,
        publisher: Optional[str] = None,
        category: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取A股指数成份股

        获取A股各类指数的基本信息，包括指数名称、指数代码、
        发布机构、指数类别等信息。

        Args:
            ts_code: 指数代码（多个代码用逗号分隔）
            market: 市场（MS主板/创业板，SZSE深交所，SSE上交所）
            publisher: 发布机构（如中证指数有限公司）
            category: 指数类别（如规模指数、行业指数、主题指数等）
            fields: 返回字段（用逗号分隔）

        Returns:
            Dict[str, Any]: 包含指数基本信息的字典
        """
        try:
            kwargs = {}
            if ts_code:
                kwargs["ts_code"] = ts_code
            if market:
                kwargs["market"] = market
            if publisher:
                kwargs["publisher"] = publisher
            if category:
                kwargs["category"] = category
            if fields:
                kwargs["fields"] = fields
            df = pro.index_basic(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_index_dailybasic(
        ts_code: Optional[str] = None,
        trade_date: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取大盘指数每日指标

        获取大盘指数的每日指标数据，包括市盈率、市净率、
        股息率等估值指标。

        Args:
            ts_code: 指数代码（多个代码用逗号分隔）
            trade_date: 交易日期（YYYYMMDD格式）
            start_date: 开始日期（YYYYMMDD格式）
            end_date: 结束日期（YYYYMMDD格式）
            fields: 返回字段（用逗号分隔）

        Returns:
            Dict[str, Any]: 包含大盘指数每日指标数据的字典
        """
        try:
            kwargs = {}
            if ts_code:
                kwargs["ts_code"] = ts_code
            if trade_date:
                kwargs["trade_date"] = trade_date
            if start_date:
                kwargs["start_date"] = start_date
            if end_date:
                kwargs["end_date"] = end_date
            if fields:
                kwargs["fields"] = fields
            df = pro.index_dailybasic(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_daily_info(
        trade_date: Optional[str] = None,
        ts_code: Optional[str] = None,
        exchange: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取市场每日交易统计

        获取沪深市场的每日交易统计数据，包括市场总成交额、
        总成交量、涨跌家数、市盈率等市场统计信息。

        Args:
            trade_date: 交易日期（YYYYMMDD格式）
            ts_code: TS代码
            exchange: 交易所代码（SSE上交所 SZSE深交所）
            start_date: 开始日期（YYYYMMDD格式）
            end_date: 结束日期（YYYYMMDD格式）
            fields: 返回字段（用逗号分隔）

        Returns:
            Dict[str, Any]: 包含市场每日交易统计数据的字典
        """
        try:
            kwargs = {}
            if trade_date:
                kwargs["trade_date"] = trade_date
            if ts_code:
                kwargs["ts_code"] = ts_code
            if exchange:
                kwargs["exchange"] = exchange
            if start_date:
                kwargs["start_date"] = start_date
            if end_date:
                kwargs["end_date"] = end_date
            if fields:
                kwargs["fields"] = fields
            df = pro.daily_info(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_sz_daily_info(
        trade_date: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取深圳市场每日交易概况

        获取深圳市场的每日交易概况数据，包括主板、中小板、
        创业板的成交情况、市盈率、换手率等信息。

        Args:
            trade_date: 交易日期（YYYYMMDD格式）
            start_date: 开始日期（YYYYMMDD格式）
            end_date: 结束日期（YYYYMMDD格式）
            fields: 返回字段（用逗号分隔）

        Returns:
            Dict[str, Any]: 包含深圳市场每日交易概况数据的字典
        """
        try:
            kwargs = {}
            if trade_date:
                kwargs["trade_date"] = trade_date
            if start_date:
                kwargs["start_date"] = start_date
            if end_date:
                kwargs["end_date"] = end_date
            if fields:
                kwargs["fields"] = fields
            df = pro.sz_daily_info(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)
