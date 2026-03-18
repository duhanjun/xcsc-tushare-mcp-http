"""
期权(Option)数据工具模块

本模块提供中国期权市场相关的数据查询工具，包括：
- 期权合约基本信息
- 期权日线行情

期权是一种金融衍生品，赋予持有者在特定日期或之前以特定价格
买入或卖出标的资产的权利（但非义务）。

中国期权市场主要包括：
- 上证50ETF期权（上交所）
- 沪深300ETF期权（上交所、深交所）
- 个股期权（上交所、深交所）
- 商品期权（大商所、郑商所、上期所）
"""

from typing import Any, Dict, Optional

from .base import format_dataframe, format_error


def register_option_tools(mcp, pro):
    """
    注册期权相关工具到 MCP 服务器

    该函数将期权数据查询工具注册到 MCP 服务器，
    使 AI 助手能够通过 MCP 协议获取中国期权市场相关数据。

    Args:
        mcp: FastMCP 服务器实例，用于注册工具
        pro: XCSC Tushare Pro API 实例，用于获取数据
    """

    @mcp.tool()
    def get_opt_basic(
        ts_code: Optional[str] = None,
        exchange: Optional[str] = None,
        opt_code: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取期权合约信息

        获取期权合约的基本信息，包括合约代码、合约名称、标的资产、
        行权价格、到期日、期权类型（看涨/看跌）等。

        Args:
            ts_code: TS代码（如 "10000001.SH" 表示上交所期权合约）
            exchange: 交易所代码（SSE上交所 SZSE深交所）
            opt_code: 期权合约产品代码（如 "510050" 表示50ETF期权）
            fields: 返回字段（用逗号分隔）

        Returns:
            Dict[str, Any]: 包含期权合约信息的字典，格式如下：
                {
                    "success": True,
                    "data": [
                        {
                            "ts_code": "10000001.SH",
                            "name": "50ETF购1月2600",
                            "exchange": "SSE",
                            "opt_code": "510050",
                            "underlying_code": "510050.SH",
                            "underlying_name": "50ETF",
                            "exercise_price": 2.600,
                            "maturity_date": "20240124",
                            "opt_type": "C",
                            "list_date": "20231225"
                        }
                    ],
                    "count": 1,
                    "columns": ["ts_code", "name", "exchange", ...]
                }

        说明:
            - opt_type: C表示看涨期权(Call)，P表示看跌期权(Put)
            - exercise_price: 行权价格，即期权合约规定的买卖标的资产的价格
            - maturity_date: 到期日，期权合约有效的最后日期

        示例:
            >>> get_opt_basic(exchange="SSE", opt_code="510050")
        """
        try:
            kwargs = {}
            if ts_code:
                kwargs["ts_code"] = ts_code
            if exchange:
                kwargs["exchange"] = exchange
            if opt_code:
                kwargs["opt_code"] = opt_code
            if fields:
                kwargs["fields"] = fields
            df = pro.opt_basic(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_opt_daily(
        ts_code: Optional[str] = None,
        trade_date: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        exchange: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取期权日线行情

        获取期权合约的日线行情数据，包括开盘价、最高价、最低价、
        收盘价、成交量、持仓量、隐含波动率、希腊字母等。

        Args:
            ts_code: TS代码（如 "10000001.SH"）
            trade_date: 交易日期（YYYYMMDD格式）
            start_date: 开始日期（YYYYMMDD格式）
            end_date: 结束日期（YYYYMMDD格式）
            exchange: 交易所代码
            fields: 返回字段（用逗号分隔）

        Returns:
            Dict[str, Any]: 包含期权日线行情数据的字典，格式如下：
                {
                    "success": True,
                    "data": [
                        {
                            "ts_code": "10000001.SH",
                            "trade_date": "20240102",
                            "pre_close": 0.1500,
                            "open": 0.1520,
                            "high": 0.1580,
                            "low": 0.1480,
                            "close": 0.1550,
                            "change": 0.0050,
                            "vol": 50000,
                            "amount": 7750000.00,
                            "oi": 120000,
                            "iv": 0.25,
                            "delta": 0.65,
                            "gamma": 0.15,
                            "theta": -0.02,
                            "vega": 0.001
                        }
                    ],
                    "count": 1,
                    "columns": ["ts_code", "trade_date", "close", ...]
                }

        说明:
            - iv: 隐含波动率(Implied Volatility)，反映市场对标的资产未来波动的预期
            - delta: 期权价格对标的资产价格的一阶导数，表示价格敏感度
            - gamma: delta对标的资产价格的变化率
            - theta: 期权价格随时间衰减的速度
            - vega: 期权价格对隐含波动率变化的敏感度
            - oi: 持仓量(Open Interest)，未平仓合约数量

        示例:
            >>> get_opt_daily(ts_code="10000001.SH", start_date="20240101", end_date="20240131")
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
            if exchange:
                kwargs["exchange"] = exchange
            if fields:
                kwargs["fields"] = fields
            df = pro.opt_daily(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)
