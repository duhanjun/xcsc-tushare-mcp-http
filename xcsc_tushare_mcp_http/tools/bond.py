"""
债券(Bond)数据工具模块

本模块提供中国债券市场相关的数据查询工具，包括：
- 可转债基本信息
- 可转债行情
- 可转债发行信息
- 可转债赎回信息
- 可转债回售信息
- 可转债强制赎回信息
- 债券基本资料

债券是发行人向投资者发行的、承诺按约定利率支付利息并到期偿还本金的债务凭证。
可转债是一种可以在特定条件下转换为公司股票的债券。
"""

from typing import Any, Dict, Optional

from .base import format_dataframe, format_error


def register_bond_tools(mcp, pro):
    """
    注册债券相关工具到 MCP 服务器

    该函数将债券数据查询工具注册到 MCP 服务器，
    使 AI 助手能够通过 MCP 协议获取中国债券市场相关数据。

    Args:
        mcp: FastMCP 服务器实例，用于注册工具
        pro: XCSC Tushare Pro API 实例，用于获取数据
    """

    @mcp.tool()
    def get_cb_basic(
        ts_code: Optional[str] = None,
        exchange: Optional[str] = None,
        list_date: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取可转债基本信息

        获取可转债的基本信息，包括债券代码、债券名称、正股代码、
        转股价格、票面利率、到期日期等。

        Args:
            ts_code: TS代码（如 "110043.SH" 表示浦发转债）
            exchange: 交易所代码（SSE上交所 SZSE深交所）
            list_date: 上市日期（YYYYMMDD格式）
            fields: 返回字段（用逗号分隔）

        Returns:
            Dict[str, Any]: 包含可转债基本信息的字典，格式如下：
                {
                    "success": True,
                    "data": [
                        {
                            "ts_code": "110043.SH",
                            "bond_short_name": "浦发转债",
                            "stock_code": "600000.SH",
                            "stock_short_name": "浦发银行",
                            "list_date": "20191115",
                            "maturity_date": "20251027",
                            "issue_size": 5000000.00,
                            "convert_price": 15.05,
                            "coupon_rate": 0.20
                        }
                    ],
                    "count": 1,
                    "columns": ["ts_code", "bond_short_name", "stock_code", ...]
                }

        说明:
            - convert_price: 转股价格，即可转债转换为股票时的价格
            - coupon_rate: 票面利率，债券的年利息率
            - issue_size: 发行规模，单位通常为万元

        示例:
            >>> get_cb_basic(ts_code="110043.SH")
        """
        try:
            kwargs = {}
            if ts_code:
                kwargs["ts_code"] = ts_code
            if exchange:
                kwargs["exchange"] = exchange
            if list_date:
                kwargs["list_date"] = list_date
            if fields:
                kwargs["fields"] = fields
            df = pro.cb_basic(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_cb_daily(
        ts_code: Optional[str] = None,
        trade_date: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取可转债行情

        获取可转债的日线行情数据，包括开盘价、最高价、最低价、
        收盘价、成交量、转股溢价率、纯债溢价率等。

        Args:
            ts_code: TS代码（如 "110043.SH"）
            trade_date: 交易日期（YYYYMMDD格式）
            start_date: 开始日期（YYYYMMDD格式）
            end_date: 结束日期（YYYYMMDD格式）
            fields: 返回字段（用逗号分隔）

        Returns:
            Dict[str, Any]: 包含可转债行情数据的字典，格式如下：
                {
                    "success": True,
                    "data": [
                        {
                            "ts_code": "110043.SH",
                            "trade_date": "20240102",
                            "pre_close": 105.50,
                            "open": 105.80,
                            "high": 106.20,
                            "low": 105.30,
                            "close": 106.00,
                            "change": 0.50,
                            "vol": 50000,
                            "amount": 5300000.00,
                            "conversion_premium": 0.25,
                            "bond_premium": 0.15
                        }
                    ],
                    "count": 1,
                    "columns": ["ts_code", "trade_date", "close", ...]
                }

        说明:
            - conversion_premium: 转股溢价率，可转债价格相对于转股价值的溢价程度
            - bond_premium: 纯债溢价率，可转债价格相对于纯债价值的溢价程度

        示例:
            >>> get_cb_daily(ts_code="110043.SH", start_date="20240101", end_date="20240131")
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
            df = pro.cb_daily(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_cb_issue(
        ts_code: Optional[str] = None,
        ann_date: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取可转债发行

        获取可转债的发行信息，包括发行公告日、申购日期、
        中签率、发行价格、募集资金总额等。

        Args:
            ts_code: TS代码（如 "110043.SH"）
            ann_date: 公告日期（YYYYMMDD格式）
            fields: 返回字段（用逗号分隔）

        Returns:
            Dict[str, Any]: 包含可转债发行数据的字典，格式如下：
                {
                    "success": True,
                    "data": [
                        {
                            "ts_code": "110043.SH",
                            "ann_date": "20191025",
                            "issue_date": "20191028",
                            "lottery_date": "20191029",
                            "list_date": "20191115",
                            "issue_price": 100.00,
                            "issue_size": 5000000.00,
                            "winning_rate": 0.015
                        }
                    ],
                    "count": 1,
                    "columns": ["ts_code", "ann_date", "issue_date", ...]
                }

        示例:
            >>> get_cb_issue(ts_code="110043.SH")
        """
        try:
            kwargs = {}
            if ts_code:
                kwargs["ts_code"] = ts_code
            if ann_date:
                kwargs["ann_date"] = ann_date
            if fields:
                kwargs["fields"] = fields
            df = pro.cb_issue(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_cb_call(
        ts_code: Optional[str] = None,
        call_type: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取可转债有条件赎回价格和触发比例

        获取可转债的有条件赎回条款，包括赎回触发价格、
        赎回价格、触发条件等。

        Args:
            ts_code: TS代码（如 "110043.SH"）
            call_type: 赎回类型（如 "conditional" 有条件赎回）
            fields: 返回字段（用逗号分隔）

        Returns:
            Dict[str, Any]: 包含可转债有条件赎回价格和触发比例数据的字典，格式如下：
                {
                    "success": True,
                    "data": [
                        {
                            "ts_code": "110043.SH",
                            "call_type": "conditional",
                            "call_trigger_price": 19.56,
                            "call_price": 100.50,
                            "call_trigger_days": 15,
                            "call_trigger_ratio": 1.30
                        }
                    ],
                    "count": 1,
                    "columns": ["ts_code", "call_type", "call_trigger_price", ...]
                }

        说明:
            - call_trigger_price: 赎回触发价格，正股价格达到此价格可能触发赎回
            - call_trigger_ratio: 触发比例，正股价格相对于转股价格的倍数
            - call_trigger_days: 触发天数，正股价格连续达到触发条件的天数

        示例:
            >>> get_cb_call(ts_code="110043.SH")
        """
        try:
            kwargs = {}
            if ts_code:
                kwargs["ts_code"] = ts_code
            if call_type:
                kwargs["call_type"] = call_type
            if fields:
                kwargs["fields"] = fields
            df = pro.cb_call(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_cb_put(
        ts_code: Optional[str] = None,
        put_type: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取可转债有条件回售价格和触发比例

        获取可转债的有条件回售条款，包括回售触发价格、
        回售价格、触发条件等。

        Args:
            ts_code: TS代码（如 "110043.SH"）
            put_type: 回售类型（如 "conditional" 有条件回售）
            fields: 返回字段（用逗号分隔）

        Returns:
            Dict[str, Any]: 包含可转债有条件回售价格和触发比例数据的字典，格式如下：
                {
                    "success": True,
                    "data": [
                        {
                            "ts_code": "110043.SH",
                            "put_type": "conditional",
                            "put_trigger_price": 10.54,
                            "put_price": 103.00,
                            "put_trigger_days": 30,
                            "put_trigger_ratio": 0.70
                        }
                    ],
                    "count": 1,
                    "columns": ["ts_code", "put_type", "put_trigger_price", ...]
                }

        说明:
            - put_trigger_price: 回售触发价格，正股价格达到此价格可能触发回售
            - put_trigger_ratio: 触发比例，正股价格相对于转股价格的倍数
            - put_trigger_days: 触发天数，正股价格连续达到触发条件的天数
            - put_price: 回售价格，投资者回售债券时获得的价格

        示例:
            >>> get_cb_put(ts_code="110043.SH")
        """
        try:
            kwargs = {}
            if ts_code:
                kwargs["ts_code"] = ts_code
            if put_type:
                kwargs["put_type"] = put_type
            if fields:
                kwargs["fields"] = fields
            df = pro.cb_put(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_cb_force_call(
        ts_code: Optional[str] = None,
        ann_date: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取可转债强制赎回信息

        获取可转债的强制赎回公告信息，包括赎回公告日、
        赎回登记日、赎回价格、赎回原因等。

        Args:
            ts_code: TS代码（如 "110043.SH"）
            ann_date: 公告日期（YYYYMMDD格式）
            start_date: 开始日期（YYYYMMDD格式）
            end_date: 结束日期（YYYYMMDD格式）
            fields: 返回字段（用逗号分隔）

        Returns:
            Dict[str, Any]: 包含可转债强制赎回信息数据的字典，格式如下：
                {
                    "success": True,
                    "data": [
                        {
                            "ts_code": "110043.SH",
                            "ann_date": "20240115",
                            "call_reg_date": "20240201",
                            "call_price": 100.50,
                            "call_reason": "正股收盘价连续30个交易日中至少有15个交易日不低于转股价的130%"
                        }
                    ],
                    "count": 1,
                    "columns": ["ts_code", "ann_date", "call_reg_date", ...]
                }

        示例:
            >>> get_cb_force_call(ts_code="110043.SH")
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
            df = pro.cb_force_call(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_bond_basic(
        ts_code: Optional[str] = None,
        bond_type: Optional[str] = None,
        market: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取中国债券基本资料

        获取中国债券市场的基本资料，包括国债、企业债、
        公司债、金融债等各类债券的基本信息。

        Args:
            ts_code: TS代码（如 "019547.SH" 表示国债）
            bond_type: 债券类型（如 "国债"、"企业债"、"公司债"、"金融债"等）
            market: 市场（如 "银行间"、"交易所"）
            fields: 返回字段（用逗号分隔）

        Returns:
            Dict[str, Any]: 包含中国债券基本资料数据的字典，格式如下：
                {
                    "success": True,
                    "data": [
                        {
                            "ts_code": "019547.SH",
                            "bond_name": "16国债19",
                            "bond_type": "国债",
                            "issue_date": "20160922",
                            "maturity_date": "20260922",
                            "issue_size": 3000000.00,
                            "coupon_rate": 2.74,
                            "market": "交易所"
                        }
                    ],
                    "count": 1,
                    "columns": ["ts_code", "bond_name", "bond_type", ...]
                }

        示例:
            >>> get_bond_basic(bond_type="国债")
        """
        try:
            kwargs = {}
            if ts_code:
                kwargs["ts_code"] = ts_code
            if bond_type:
                kwargs["bond_type"] = bond_type
            if market:
                kwargs["market"] = market
            if fields:
                kwargs["fields"] = fields
            df = pro.bond_basic(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)
