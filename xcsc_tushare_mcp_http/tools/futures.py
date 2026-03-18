"""
期货(Futures)数据工具模块

本模块提供中国期货市场相关的数据查询工具，包括：
- 期货合约基本信息
- 期货日线行情
- 持仓排名数据
- 结算参数
- 主力与连续合约映射
- 仓单日报

期货是一种标准化的远期合约，约定在未来某个特定日期以特定价格
买入或卖出一定数量的标的资产。
"""

from typing import Any, Dict, Optional

from .base import format_dataframe, format_error


def register_futures_tools(mcp, pro):
    """
    注册期货相关工具到 MCP 服务器

    该函数将期货数据查询工具注册到 MCP 服务器，
    使 AI 助手能够通过 MCP 协议获取中国期货市场相关数据。

    Args:
        mcp: FastMCP 服务器实例，用于注册工具
        pro: XCSC Tushare Pro API 实例，用于获取数据
    """

    @mcp.tool()
    def get_fut_basic(
        ts_code: Optional[str] = None,
        exchange: Optional[str] = None,
        fut_code: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取期货合约信息

        获取期货合约的基本信息，包括合约代码、合约名称、
        上市日期、交割月份、最小变动价位、交割方式等。

        Args:
            ts_code: TS代码（如 "CU2403.SH" 表示上期所2024年3月铜期货）
            exchange: 交易所代码（CFFEX中金所 DCE大商所 CZCE郑商所 SHFE上期所 INE上能源）
            fut_code: 期货合约产品代码（如 "CU" 表示铜期货）
            fields: 返回字段（用逗号分隔）

        Returns:
            Dict[str, Any]: 包含期货合约信息的字典，格式如下：
                {
                    "success": True,
                    "data": [
                        {
                            "ts_code": "CU2403.SH",
                            "symbol": "cu2403",
                            "name": "沪铜2403",
                            "exchange": "SHFE",
                            "fut_code": "CU",
                            "list_date": "20230316",
                            "delist_date": "20240315",
                            "delivery_month": "202403"
                        }
                    ],
                    "count": 1,
                    "columns": ["ts_code", "symbol", "name", ...]
                }

        示例:
            >>> get_fut_basic(exchange="SHFE", fut_code="CU")
        """
        try:
            kwargs = {}
            if ts_code:
                kwargs["ts_code"] = ts_code
            if exchange:
                kwargs["exchange"] = exchange
            if fut_code:
                kwargs["fut_code"] = fut_code
            if fields:
                kwargs["fields"] = fields
            df = pro.fut_basic(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_fut_daily(
        ts_code: Optional[str] = None,
        trade_date: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        exchange: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取期货日线行情

        获取期货合约的日线行情数据，包括开盘价、最高价、最低价、
        收盘价、成交量、持仓量、结算价等。

        Args:
            ts_code: TS代码（如 "CU2403.SH"）
            trade_date: 交易日期（YYYYMMDD格式）
            start_date: 开始日期（YYYYMMDD格式）
            end_date: 结束日期（YYYYMMDD格式）
            exchange: 交易所代码
            fields: 返回字段（用逗号分隔）

        Returns:
            Dict[str, Any]: 包含期货日线行情数据的字典，格式如下：
                {
                    "success": True,
                    "data": [
                        {
                            "ts_code": "CU2403.SH",
                            "trade_date": "20240102",
                            "pre_close": 68950.00,
                            "pre_settle": 68980.00,
                            "open": 69000.00,
                            "high": 69500.00,
                            "low": 68800.00,
                            "close": 69200.00,
                            "settle": 69250.00,
                            "change": 220.00,
                            "vol": 125000,
                            "amount": 8656250000.00,
                            "oi": 150000
                        }
                    ],
                    "count": 1,
                    "columns": ["ts_code", "trade_date", "close", ...]
                }

        示例:
            >>> get_fut_daily(ts_code="CU2403.SH", start_date="20240101", end_date="20240131")
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
            df = pro.fut_daily(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_fut_holding(
        ts_code: Optional[str] = None,
        trade_date: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        exchange: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取每日持仓排名

        获取期货合约每日持仓排名数据，包括前20名会员的
        持买单量、持卖单量、净持仓等信息。

        Args:
            ts_code: TS代码（如 "CU2403.SH"）
            trade_date: 交易日期（YYYYMMDD格式）
            start_date: 开始日期（YYYYMMDD格式）
            end_date: 结束日期（YYYYMMDD格式）
            exchange: 交易所代码
            fields: 返回字段（用逗号分隔）

        Returns:
            Dict[str, Any]: 包含每日持仓排名数据的字典，格式如下：
                {
                    "success": True,
                    "data": [
                        {
                            "ts_code": "CU2403.SH",
                            "trade_date": "20240102",
                            "broker": "中信期货",
                            "vol": 5000,
                            "vol_chg": 200,
                            "long_hld": 3000,
                            "long_chg": 100,
                            "short_hld": 2000,
                            "short_chg": -100
                        }
                    ],
                    "count": 1,
                    "columns": ["ts_code", "trade_date", "broker", ...]
                }

        示例:
            >>> get_fut_holding(ts_code="CU2403.SH", trade_date="20240102")
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
            df = pro.fut_holding(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_fut_settle(
        ts_code: Optional[str] = None,
        trade_date: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        exchange: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取每日结算参数

        获取期货合约每日结算参数，包括交易保证金比例、
        涨跌停板幅度、手续费率等。

        Args:
            ts_code: TS代码（如 "CU2403.SH"）
            trade_date: 交易日期（YYYYMMDD格式）
            start_date: 开始日期（YYYYMMDD格式）
            end_date: 结束日期（YYYYMMDD格式）
            exchange: 交易所代码
            fields: 返回字段（用逗号分隔）

        Returns:
            Dict[str, Any]: 包含每日结算参数数据的字典，格式如下：
                {
                    "success": True,
                    "data": [
                        {
                            "ts_code": "CU2403.SH",
                            "trade_date": "20240102",
                            "margin_rate": 0.10,
                            "limit_up": 76180.00,
                            "limit_down": 62320.00,
                            "settle_price": 69250.00
                        }
                    ],
                    "count": 1,
                    "columns": ["ts_code", "trade_date", "margin_rate", ...]
                }

        示例:
            >>> get_fut_settle(ts_code="CU2403.SH", trade_date="20240102")
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
            df = pro.fut_settle(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_fut_mapping(
        ts_code: Optional[str] = None,
        trade_date: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取期货主力与连续合约

        获取期货主力合约和连续合约的映射关系，主力合约是
        持仓量最大的合约，连续合约用于连接不同交割月份的数据。

        Args:
            ts_code: TS代码（如 "CU.ZH" 表示铜主力合约）
            trade_date: 交易日期（YYYYMMDD格式）
            start_date: 开始日期（YYYYMMDD格式）
            end_date: 结束日期（YYYYMMDD格式）
            fields: 返回字段（用逗号分隔）

        Returns:
            Dict[str, Any]: 包含期货主力与连续合约数据的字典，格式如下：
                {
                    "success": True,
                    "data": [
                        {
                            "ts_code": "CU.ZH",
                            "trade_date": "20240102",
                            "mapping_ts_code": "CU2403.SH",
                            "contract_type": "主力合约"
                        }
                    ],
                    "count": 1,
                    "columns": ["ts_code", "trade_date", "mapping_ts_code", ...]
                }

        示例:
            >>> get_fut_mapping(ts_code="CU.ZH", trade_date="20240102")
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
            df = pro.fut_mapping(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_fut_wsr(
        ts_code: Optional[str] = None,
        trade_date: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取仓单日报

        获取期货品种的标准仓单日报数据，包括仓单数量、
        有效预报、仓单变化等信息，反映现货库存情况。

        Args:
            ts_code: TS代码（如 "CU.SHF" 表示上期所铜）
            trade_date: 交易日期（YYYYMMDD格式）
            start_date: 开始日期（YYYYMMDD格式）
            end_date: 结束日期（YYYYMMDD格式）
            fields: 返回字段（用逗号分隔）

        Returns:
            Dict[str, Any]: 包含仓单日报数据的字典，格式如下：
                {
                    "success": True,
                    "data": [
                        {
                            "ts_code": "CU.SHF",
                            "trade_date": "20240102",
                            "receipt_num": 35000,
                            "receipt_chg": 500,
                            "forecast": 2000,
                            "warehouse": "上海期货交易所指定交割仓库"
                        }
                    ],
                    "count": 1,
                    "columns": ["ts_code", "trade_date", "receipt_num", ...]
                }

        示例:
            >>> get_fut_wsr(ts_code="CU.SHF", trade_date="20240102")
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
            df = pro.fut_wsr(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)
