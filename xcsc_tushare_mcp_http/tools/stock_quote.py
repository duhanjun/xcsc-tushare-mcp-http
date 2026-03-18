"""
股票行情数据工具模块

该模块提供股票行情相关的数据查询工具，包括：
- 日线/周线/月线行情查询
- 分钟数据查询
- 每日指标（基本面指标）查询
- 停复牌信息查询
- 涨跌停价格查询
- 复权因子查询
- 涨跌停和炸板数据查询
- 个股资金流向查询
- 港股通相关数据查询

这些工具主要用于获取股票的交易行情和市场数据。
"""

from typing import Any, Dict, Optional

from .base import format_dataframe, format_error


def register_stock_quote_tools(mcp, pro):
    """
    注册股票行情数据工具到 MCP 服务器

    该函数注册所有股票行情相关的工具，包括日线、周线、月线行情、
    分钟数据、每日指标、停复牌信息、涨跌停价格等。

    Args:
        mcp: FastMCP 服务器实例
        pro: XCSC Tushare Pro API 实例
    """

    @mcp.tool()
    def get_daily_quote(
        ts_code: Optional[str] = None,
        trade_date: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取中国A股日行情

        获取沪深A股的日线行情数据，包括开盘价、收盘价、最高价、
        最低价、成交量、成交额等。

        Args:
            ts_code: TS代码（多个代码用逗号分隔），如 "000001.SZ"
            trade_date: 交易日期（YYYYMMDD格式）
            start_date: 开始日期（YYYYMMDD格式）
            end_date: 结束日期（YYYYMMDD格式）
            fields: 返回字段（用逗号分隔）

        Returns:
            Dict[str, Any]: 包含日线行情数据的字典，格式如下：
                {
                    "success": True,
                    "data": [
                        {
                            "ts_code": "000001.SZ",
                            "trade_date": "20240102",
                            "open": 10.5,
                            "high": 10.8,
                            "low": 10.3,
                            "close": 10.6,
                            "pre_close": 10.4,
                            "change": 0.2,
                            "pct_chg": 1.92,
                            "vol": 123456,
                            "amount": 1300000.0
                        }
                    ],
                    "count": 1,
                    "columns": ["ts_code", "trade_date", "open", ...]
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
            df = pro.daily(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_weekly_quote(
        ts_code: Optional[str] = None,
        trade_date: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取A股周线行情

        获取沪深A股的周线行情数据，包括周开盘价、周收盘价、
        周最高价、周最低价、周成交量、周成交额等。

        Args:
            ts_code: TS代码（多个代码用逗号分隔）
            trade_date: 交易日期（YYYYMMDD格式）
            start_date: 开始日期（YYYYMMDD格式）
            end_date: 结束日期（YYYYMMDD格式）
            fields: 返回字段（用逗号分隔）

        Returns:
            Dict[str, Any]: 包含周线行情数据的字典
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
            df = pro.weekly(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_monthly_quote(
        ts_code: Optional[str] = None,
        trade_date: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取A股月线行情

        获取沪深A股的月线行情数据，包括月开盘价、月收盘价、
        月最高价、月最低价、月成交量、月成交额等。

        Args:
            ts_code: TS代码（多个代码用逗号分隔）
            trade_date: 交易日期（YYYYMMDD格式）
            start_date: 开始日期（YYYYMMDD格式）
            end_date: 结束日期（YYYYMMDD格式）
            fields: 返回字段（用逗号分隔）

        Returns:
            Dict[str, Any]: 包含月线行情数据的字典
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
            df = pro.monthly(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_min_quote(
        ts_code: Optional[str] = None,
        trade_date: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        freq: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取分钟数据

        获取沪深A股的分钟级行情数据，支持1分钟、5分钟、
        15分钟、30分钟、60分钟等多种周期。

        Args:
            ts_code: TS代码（多个代码用逗号分隔）
            trade_date: 交易日期（YYYYMMDD格式）
            start_date: 开始日期（YYYYMMDD格式）
            end_date: 结束日期（YYYYMMDD格式）
            freq: 分钟周期（1min/5min/15min/30min/60min）
            fields: 返回字段（用逗号分隔）

        Returns:
            Dict[str, Any]: 包含分钟行情数据的字典
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
            if freq:
                kwargs["freq"] = freq
            if fields:
                kwargs["fields"] = fields
            df = pro.stk_mins(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_daily_basic(
        ts_code: Optional[str] = None,
        trade_date: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取每日指标（基本面指标）

        获取沪深A股的每日基本面指标数据，包括市盈率、市净率、
        换手率、量比、成交额、市值等指标。

        Args:
            ts_code: TS代码（多个代码用逗号分隔）
            trade_date: 交易日期（YYYYMMDD格式）
            start_date: 开始日期（YYYYMMDD格式）
            end_date: 结束日期（YYYYMMDD格式）
            fields: 返回字段（用逗号分隔）

        Returns:
            Dict[str, Any]: 包含每日指标数据的字典
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
            df = pro.daily_basic_ts(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_suspend_info(
        ts_code: Optional[str] = None,
        suspend_date: Optional[str] = None,
        resume_date: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取A股停复牌信息

        获取沪深A股的股票停复牌信息，包括停牌日期、
        复牌日期、停牌原因等。

        Args:
            ts_code: TS代码（多个代码用逗号分隔）
            suspend_date: 停牌日期（YYYYMMDD格式）
            resume_date: 复牌日期（YYYYMMDD格式）
            fields: 返回字段（用逗号分隔）

        Returns:
            Dict[str, Any]: 包含停复牌信息的字典
        """
        try:
            kwargs = {}
            if ts_code:
                kwargs["ts_code"] = ts_code
            if suspend_date:
                kwargs["suspend_date"] = suspend_date
            if resume_date:
                kwargs["resume_date"] = resume_date
            if fields:
                kwargs["fields"] = fields
            df = pro.suspend(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_stk_limit(
        ts_code: Optional[str] = None,
        trade_date: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取每日涨跌停价格

        获取沪深A股每日的涨跌停价格限制，包括涨停价、
        跌停价、昨收价等信息。

        Args:
            ts_code: TS代码（多个代码用逗号分隔）
            trade_date: 交易日期（YYYYMMDD格式）
            start_date: 开始日期（YYYYMMDD格式）
            end_date: 结束日期（YYYYMMDD格式）
            fields: 返回字段（用逗号分隔）

        Returns:
            Dict[str, Any]: 包含涨跌停价格信息的字典
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
            df = pro.stk_limit(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_adj_factor(
        ts_code: Optional[str] = None,
        trade_date: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取股票复权因子

        获取沪深A股的复权因子数据，用于计算复权价格。
        复权因子考虑了分红、送股、配股等对股价的影响。

        Args:
            ts_code: TS代码（多个代码用逗号分隔）
            trade_date: 交易日期（YYYYMMDD格式）
            start_date: 开始日期（YYYYMMDD格式）
            end_date: 结束日期（YYYYMMDD格式）
            fields: 返回字段（用逗号分隔）

        Returns:
            Dict[str, Any]: 包含复权因子数据的字典
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
            df = pro.adj_factor(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_limit_list(
        trade_date: Optional[str] = None,
        ts_code: Optional[str] = None,
        limit_type: Optional[str] = None,
        exchange: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取涨跌停和炸板数据

        获取沪深A股每日的涨停、跌停和炸板股票数据，
        包括封单量、封单金额、首次封板时间等信息。

        Args:
            trade_date: 交易日期（YYYYMMDD格式）
            ts_code: TS代码（多个代码用逗号分隔）
            limit_type: 涨跌停类型（U涨停 D跌停 Z炸板）
            exchange: 交易所代码（SSE上交所 SZSE深交所）
            fields: 返回字段（用逗号分隔）

        Returns:
            Dict[str, Any]: 包含涨跌停和炸板数据的字典
        """
        try:
            kwargs = {}
            if trade_date:
                kwargs["trade_date"] = trade_date
            if ts_code:
                kwargs["ts_code"] = ts_code
            if limit_type:
                kwargs["limit_type"] = limit_type
            if exchange:
                kwargs["exchange"] = exchange
            if fields:
                kwargs["fields"] = fields
            df = pro.limit_list(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_moneyflow(
        ts_code: Optional[str] = None,
        trade_date: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取个股资金流向

        获取沪深A股的个股资金流向数据，包括小单、中单、
        大单、特大单的流入流出金额。

        Args:
            ts_code: TS代码（多个代码用逗号分隔）
            trade_date: 交易日期（YYYYMMDD格式）
            start_date: 开始日期（YYYYMMDD格式）
            end_date: 结束日期（YYYYMMDD格式）
            fields: 返回字段（用逗号分隔）

        Returns:
            Dict[str, Any]: 包含个股资金流向数据的字典
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
            df = pro.moneyflow(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_ggt_top10(
        trade_date: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        market_type: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取港股通十大成交股

        获取港股通每日十大成交活跃股数据，包括买入金额、
        卖出金额、成交净买入等信息。

        Args:
            trade_date: 交易日期（YYYYMMDD格式）
            start_date: 开始日期（YYYYMMDD格式）
            end_date: 结束日期（YYYYMMDD格式）
            market_type: 市场类型（1沪市港股通 2深市港股通）
            fields: 返回字段（用逗号分隔）

        Returns:
            Dict[str, Any]: 包含港股通十大成交股数据的字典
        """
        try:
            kwargs = {}
            if trade_date:
                kwargs["trade_date"] = trade_date
            if start_date:
                kwargs["start_date"] = start_date
            if end_date:
                kwargs["end_date"] = end_date
            if market_type:
                kwargs["market_type"] = market_type
            if fields:
                kwargs["fields"] = fields
            df = pro.ggt_top10(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_ggt_daily(
        trade_date: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取港股通(沪)每日成交

        获取沪市港股通每日的成交统计数据，包括买入金额、
        卖出金额、成交总额等信息。

        Args:
            trade_date: 交易日期（YYYYMMDD格式）
            start_date: 开始日期（YYYYMMDD格式）
            end_date: 结束日期（YYYYMMDD格式）
            fields: 返回字段（用逗号分隔）

        Returns:
            Dict[str, Any]: 包含港股通(沪)每日成交数据的字典
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
            df = pro.ggt_daily(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_ggt_daily_stat(
        trade_date: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取港股通每日成交统计

        获取港股通每日的成交统计数据，包括买入金额、
        卖出金额、成交总额、成交笔数等信息。

        Args:
            trade_date: 交易日期（YYYYMMDD格式）
            start_date: 开始日期（YYYYMMDD格式）
            end_date: 结束日期（YYYYMMDD格式）
            fields: 返回字段（用逗号分隔）

        Returns:
            Dict[str, Any]: 包含港股通每日成交统计数据的字典
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
            df = pro.ggt_daily_stat(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_ggt_monthly_stat(
        month: Optional[str] = None,
        start_month: Optional[str] = None,
        end_month: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取港股通每月成交统计

        获取港股通每月的成交统计数据，包括买入金额、
        卖出金额、成交总额、成交笔数等信息。

        Args:
            month: 月份（YYYYMM格式）
            start_month: 开始月份（YYYYMM格式）
            end_month: 结束月份（YYYYMM格式）
            fields: 返回字段（用逗号分隔）

        Returns:
            Dict[str, Any]: 包含港股通每月成交统计数据的字典
        """
        try:
            kwargs = {}
            if month:
                kwargs["month"] = month
            if start_month:
                kwargs["start_month"] = start_month
            if end_month:
                kwargs["end_month"] = end_month
            if fields:
                kwargs["fields"] = fields
            df = pro.ggt_monthly_stat(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_hk_hold(
        code: Optional[str] = None,
        trade_date: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        exchange: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取沪深港股通持股明细

        获取沪深港股通每日的持股明细数据，包括持股数量、
        持股市值、持股比例等信息。

        Args:
            code: 股票代码
            trade_date: 交易日期（YYYYMMDD格式）
            start_date: 开始日期（YYYYMMDD格式）
            end_date: 结束日期（YYYYMMDD格式）
            exchange: 交易所代码（HK港交所）
            fields: 返回字段（用逗号分隔）

        Returns:
            Dict[str, Any]: 包含沪深港股通持股明细数据的字典
        """
        try:
            kwargs = {}
            if code:
                kwargs["code"] = code
            if trade_date:
                kwargs["trade_date"] = trade_date
            if start_date:
                kwargs["start_date"] = start_date
            if end_date:
                kwargs["end_date"] = end_date
            if exchange:
                kwargs["exchange"] = exchange
            if fields:
                kwargs["fields"] = fields
            df = pro.hk_hold(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_ggt_moneyflow(
        trade_date: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取沪深港通资金流向

        获取沪深港通每日的资金流向数据，包括沪市港股通、
        深市港股通的资金流入流出情况。

        Args:
            trade_date: 交易日期（YYYYMMDD格式）
            start_date: 开始日期（YYYYMMDD格式）
            end_date: 结束日期（YYYYMMDD格式）
            fields: 返回字段（用逗号分隔）

        Returns:
            Dict[str, Any]: 包含沪深港通资金流向数据的字典
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
            df = pro.ggt_moneyflow(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_sggt_top10(
        trade_date: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        market_type: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取沪深股通十大成交股

        获取沪深股通每日十大成交活跃股数据，包括买入金额、
        卖出金额、成交净买入等信息。

        Args:
            trade_date: 交易日期（YYYYMMDD格式）
            start_date: 开始日期（YYYYMMDD格式）
            end_date: 结束日期（YYYYMMDD格式）
            market_type: 市场类型（1沪市 2深市）
            fields: 返回字段（用逗号分隔）

        Returns:
            Dict[str, Any]: 包含沪深股通十大成交股数据的字典
        """
        try:
            kwargs = {}
            if trade_date:
                kwargs["trade_date"] = trade_date
            if start_date:
                kwargs["start_date"] = start_date
            if end_date:
                kwargs["end_date"] = end_date
            if market_type:
                kwargs["market_type"] = market_type
            if fields:
                kwargs["fields"] = fields
            df = pro.sggt_top10(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)
