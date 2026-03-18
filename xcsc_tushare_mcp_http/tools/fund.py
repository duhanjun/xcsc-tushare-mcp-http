"""
公募基金数据工具模块

该模块提供公募基金相关的数据查询工具，包括：
- 基金列表查询
- 基金净值查询
- 基金行情查询
- 基金分红查询
- 基金持仓查询
- 基金经理查询
- 基金管理人查询
- 基金规模查询

这些工具主要用于获取公募基金的基本信息、净值、持仓等数据。
"""

from typing import Any, Dict, Optional

from .base import format_dataframe, format_error


def register_fund_tools(mcp, pro):
    """
    注册公募基金数据工具到 MCP 服务器

    该函数注册所有公募基金相关的工具，包括基金列表、基金净值、
    基金行情、基金分红、基金持仓、基金经理、基金管理人、基金规模等。

    Args:
        mcp: FastMCP 服务器实例
        pro: XCSC Tushare Pro API 实例
    """

    @mcp.tool()
    def get_fund_basic(
        ts_code: Optional[str] = None,
        market: Optional[str] = None,
        fund_type: Optional[str] = None,
        status: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取基金列表

        获取公募基金的基本信息列表，包括基金代码、基金名称、
        基金类型、成立日期、管理公司等信息。

        Args:
            ts_code: TS代码（多个代码用逗号分隔）
            market: 市场（E场内 O场外）
            fund_type: 基金类型（股票型、混合型、债券型、货币型等）
            status: 基金状态（L上市 D退市）
            fields: 返回字段（用逗号分隔）

        Returns:
            Dict[str, Any]: 包含基金列表信息的字典，格式如下：
                {
                    "success": True,
                    "data": [
                        {
                            "ts_code": "000001.OF",
                            "name": "华夏成长混合",
                            "management": "华夏基金管理有限公司",
                            "fund_type": "混合型",
                            "found_date": "20011218",
                            ...
                        }
                    ],
                    "count": 1,
                    "columns": ["ts_code", "name", "management", ...]
                }
        """
        try:
            kwargs = {}
            if ts_code:
                kwargs["ts_code"] = ts_code
            if market:
                kwargs["market"] = market
            if fund_type:
                kwargs["fund_type"] = fund_type
            if status:
                kwargs["status"] = status
            if fields:
                kwargs["fields"] = fields
            df = pro.fund_basic(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_fund_nav(
        ts_code: Optional[str] = None,
        nav_date: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取基金净值

        获取公募基金的每日净值数据，包括单位净值、累计净值、
        日增长率等信息。

        Args:
            ts_code: TS代码（多个代码用逗号分隔）
            nav_date: 净值日期（YYYYMMDD格式）
            start_date: 开始日期（YYYYMMDD格式）
            end_date: 结束日期（YYYYMMDD格式）
            fields: 返回字段（用逗号分隔）

        Returns:
            Dict[str, Any]: 包含基金净值数据的字典
        """
        try:
            kwargs = {}
            if ts_code:
                kwargs["ts_code"] = ts_code
            if nav_date:
                kwargs["nav_date"] = nav_date
            if start_date:
                kwargs["start_date"] = start_date
            if end_date:
                kwargs["end_date"] = end_date
            if fields:
                kwargs["fields"] = fields
            df = pro.fund_nav(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_fund_daily(
        ts_code: Optional[str] = None,
        trade_date: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取基金行情

        获取场内基金的每日行情数据，包括开盘价、收盘价、
        最高价、最低价、成交量、成交额等信息。

        Args:
            ts_code: TS代码（多个代码用逗号分隔）
            trade_date: 交易日期（YYYYMMDD格式）
            start_date: 开始日期（YYYYMMDD格式）
            end_date: 结束日期（YYYYMMDD格式）
            fields: 返回字段（用逗号分隔）

        Returns:
            Dict[str, Any]: 包含基金行情数据的字典
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
            df = pro.fund_daily(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_fund_div(
        ts_code: Optional[str] = None,
        ann_date: Optional[str] = None,
        record_date: Optional[str] = None,
        ex_date: Optional[str] = None,
        pay_date: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取基金分红

        获取公募基金的分红数据，包括分红方案、权益登记日、
        除息日、派息日等信息。

        Args:
            ts_code: TS代码（多个代码用逗号分隔）
            ann_date: 公告日期（YYYYMMDD格式）
            record_date: 权益登记日（YYYYMMDD格式）
            ex_date: 除息日（YYYYMMDD格式）
            pay_date: 派息日（YYYYMMDD格式）
            fields: 返回字段（用逗号分隔）

        Returns:
            Dict[str, Any]: 包含基金分红数据的字典
        """
        try:
            kwargs = {}
            if ts_code:
                kwargs["ts_code"] = ts_code
            if ann_date:
                kwargs["ann_date"] = ann_date
            if record_date:
                kwargs["record_date"] = record_date
            if ex_date:
                kwargs["ex_date"] = ex_date
            if pay_date:
                kwargs["pay_date"] = pay_date
            if fields:
                kwargs["fields"] = fields
            df = pro.fund_div(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_fund_portfolio(
        ts_code: Optional[str] = None,
        ann_date: Optional[str] = None,
        end_date: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取基金持仓

        获取公募基金的持仓明细数据，包括持仓股票、持仓比例、
        持仓市值等信息。

        Args:
            ts_code: TS代码（多个代码用逗号分隔）
            ann_date: 公告日期（YYYYMMDD格式）
            end_date: 报告期（YYYYMMDD格式）
            fields: 返回字段（用逗号分隔）

        Returns:
            Dict[str, Any]: 包含基金持仓数据的字典
        """
        try:
            kwargs = {}
            if ts_code:
                kwargs["ts_code"] = ts_code
            if ann_date:
                kwargs["ann_date"] = ann_date
            if end_date:
                kwargs["end_date"] = end_date
            if fields:
                kwargs["fields"] = fields
            df = pro.fund_portfolio(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_fund_manager(
        ts_code: Optional[str] = None,
        name: Optional[str] = None,
        ann_date: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取基金经理

        获取公募基金的基金经理信息，包括基金经理姓名、任职日期、
        离职日期、管理基金等信息。

        Args:
            ts_code: TS代码（多个代码用逗号分隔）
            name: 基金经理姓名
            ann_date: 公告日期（YYYYMMDD格式）
            fields: 返回字段（用逗号分隔）

        Returns:
            Dict[str, Any]: 包含基金经理信息的字典
        """
        try:
            kwargs = {}
            if ts_code:
                kwargs["ts_code"] = ts_code
            if name:
                kwargs["name"] = name
            if ann_date:
                kwargs["ann_date"] = ann_date
            if fields:
                kwargs["fields"] = fields
            df = pro.fund_manager(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_fund_company(
        name: Optional[str] = None,
        shortname: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取基金管理人

        获取公募基金管理公司的基本信息，包括公司名称、简称、
        成立日期、管理规模等信息。

        Args:
            name: 公司名称
            shortname: 公司简称
            fields: 返回字段（用逗号分隔）

        Returns:
            Dict[str, Any]: 包含基金管理人信息的字典
        """
        try:
            kwargs = {}
            if name:
                kwargs["name"] = name
            if shortname:
                kwargs["shortname"] = shortname
            if fields:
                kwargs["fields"] = fields
            df = pro.fund_company(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_fund_share(
        ts_code: Optional[str] = None,
        trade_date: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取基金规模

        获取公募基金的规模数据，包括基金份额、基金资产净值等信息。

        Args:
            ts_code: TS代码（多个代码用逗号分隔）
            trade_date: 交易日期（YYYYMMDD格式）
            start_date: 开始日期（YYYYMMDD格式）
            end_date: 结束日期（YYYYMMDD格式）
            fields: 返回字段（用逗号分隔）

        Returns:
            Dict[str, Any]: 包含基金规模数据的字典
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
            df = pro.fund_share(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)
