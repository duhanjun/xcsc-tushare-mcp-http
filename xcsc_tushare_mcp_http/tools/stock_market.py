"""
股票市场参考数据工具模块

该模块提供股票市场参考数据相关的查询工具，包括：
- 股东信息查询（前十大股东、前十大流通股东、股东人数）
- 股东增减持查询
- 股权质押查询（明细和统计）
- 股票回购查询
- 大宗交易查询
- 概念股查询（分类和明细）
- 融资融券查询（明细和汇总）
- 龙虎榜查询（每日明细和机构明细）
- 股票开户数据查询

这些工具主要用于获取股票的市场参考数据和交易统计数据。
"""

from typing import Any, Dict, Optional

from .base import format_dataframe, format_error


def register_stock_market_tools(mcp, pro):
    """
    注册股票市场参考数据工具到 MCP 服务器

    该函数注册所有股票市场参考数据相关的工具，包括股东信息、
    股权质押、股票回购、大宗交易、概念股、融资融券、龙虎榜等。

    Args:
        mcp: FastMCP 服务器实例
        pro: XCSC Tushare Pro API 实例
    """

    @mcp.tool()
    def get_top10_holders(
        ts_code: Optional[str] = None,
        period: Optional[str] = None,
        ann_date: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取前十大股东

        获取沪深A股上市公司的前十大股东持股信息，包括股东名称、
        持股数量、持股比例、持股变动等信息。

        Args:
            ts_code: TS代码（多个代码用逗号分隔）
            period: 报告期（YYYYMMDD格式）
            ann_date: 公告日期（YYYYMMDD格式）
            start_date: 开始日期（YYYYMMDD格式）
            end_date: 结束日期（YYYYMMDD格式）
            fields: 返回字段（用逗号分隔）

        Returns:
            Dict[str, Any]: 包含前十大股东信息的字典
        """
        try:
            kwargs = {}
            if ts_code:
                kwargs["ts_code"] = ts_code
            if period:
                kwargs["period"] = period
            if ann_date:
                kwargs["ann_date"] = ann_date
            if start_date:
                kwargs["start_date"] = start_date
            if end_date:
                kwargs["end_date"] = end_date
            if fields:
                kwargs["fields"] = fields
            df = pro.top10_holders(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_top10_floatholders(
        ts_code: Optional[str] = None,
        period: Optional[str] = None,
        ann_date: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取前十大流通股东

        获取沪深A股上市公司的前十大流通股东持股信息，包括股东名称、
        持股数量、持股比例、持股变动等信息。

        Args:
            ts_code: TS代码（多个代码用逗号分隔）
            period: 报告期（YYYYMMDD格式）
            ann_date: 公告日期（YYYYMMDD格式）
            start_date: 开始日期（YYYYMMDD格式）
            end_date: 结束日期（YYYYMMDD格式）
            fields: 返回字段（用逗号分隔）

        Returns:
            Dict[str, Any]: 包含前十大流通股东信息的字典
        """
        try:
            kwargs = {}
            if ts_code:
                kwargs["ts_code"] = ts_code
            if period:
                kwargs["period"] = period
            if ann_date:
                kwargs["ann_date"] = ann_date
            if start_date:
                kwargs["start_date"] = start_date
            if end_date:
                kwargs["end_date"] = end_date
            if fields:
                kwargs["fields"] = fields
            df = pro.top10_floatholders(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_stk_holdernumber(
        ts_code: Optional[str] = None,
        enddate: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取股东人数

        获取沪深A股上市公司的股东人数数据，包括股东总户数、
        户均持股数量、户均持股比例等信息。

        Args:
            ts_code: TS代码（多个代码用逗号分隔）
            enddate: 截止日期（YYYYMMDD格式）
            start_date: 开始日期（YYYYMMDD格式）
            end_date: 结束日期（YYYYMMDD格式）
            fields: 返回字段（用逗号分隔）

        Returns:
            Dict[str, Any]: 包含股东人数信息的字典
        """
        try:
            kwargs = {}
            if ts_code:
                kwargs["ts_code"] = ts_code
            if enddate:
                kwargs["enddate"] = enddate
            if start_date:
                kwargs["start_date"] = start_date
            if end_date:
                kwargs["end_date"] = end_date
            if fields:
                kwargs["fields"] = fields
            df = pro.stk_holdernumber(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_stk_sharechange(
        ts_code: Optional[str] = None,
        ann_date: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        holder_type: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取股东增减持

        获取沪深A股上市公司的股东增减持数据，包括增减持股东、
        增减持数量、增减持金额、增减持后持股比例等信息。

        Args:
            ts_code: TS代码（多个代码用逗号分隔）
            ann_date: 公告日期（YYYYMMDD格式）
            start_date: 开始日期（YYYYMMDD格式）
            end_date: 结束日期（YYYYMMDD格式）
            holder_type: 股东类型（G高管 P个人 C公司）
            fields: 返回字段（用逗号分隔）

        Returns:
            Dict[str, Any]: 包含股东增减持信息的字典
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
            if holder_type:
                kwargs["holder_type"] = holder_type
            if fields:
                kwargs["fields"] = fields
            df = pro.stk_sharechange(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_share_float(
        ts_code: Optional[str] = None,
        ann_date: Optional[str] = None,
        holder_name: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取股权质押明细数据

        获取沪深A股上市公司的股权质押明细数据，包括质押股东、
        质押数量、质押比例、质押日期、解押日期等信息。

        Args:
            ts_code: TS代码（多个代码用逗号分隔）
            ann_date: 公告日期（YYYYMMDD格式）
            holder_name: 股东名称
            start_date: 开始日期（YYYYMMDD格式）
            end_date: 结束日期（YYYYMMDD格式）
            fields: 返回字段（用逗号分隔）

        Returns:
            Dict[str, Any]: 包含股权质押明细数据的字典
        """
        try:
            kwargs = {}
            if ts_code:
                kwargs["ts_code"] = ts_code
            if ann_date:
                kwargs["ann_date"] = ann_date
            if holder_name:
                kwargs["holder_name"] = holder_name
            if start_date:
                kwargs["start_date"] = start_date
            if end_date:
                kwargs["end_date"] = end_date
            if fields:
                kwargs["fields"] = fields
            df = pro.share_float(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_share_float_stat(
        ts_code: Optional[str] = None,
        trade_date: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取股权质押统计数据

        获取沪深A股上市公司的股权质押统计数据，包括质押总股数、
        质押比例、质押笔数、解押笔数等统计信息。

        Args:
            ts_code: TS代码（多个代码用逗号分隔）
            trade_date: 交易日期（YYYYMMDD格式）
            start_date: 开始日期（YYYYMMDD格式）
            end_date: 结束日期（YYYYMMDD格式）
            fields: 返回字段（用逗号分隔）

        Returns:
            Dict[str, Any]: 包含股权质押统计数据的字典
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
            df = pro.share_float_stat(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_repurchase(
        ts_code: Optional[str] = None,
        ann_date: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取股票回购

        获取沪深A股上市公司的股票回购数据，包括回购方式、
        回购数量、回购金额、回购价格区间等信息。

        Args:
            ts_code: TS代码（多个代码用逗号分隔）
            ann_date: 公告日期（YYYYMMDD格式）
            start_date: 开始日期（YYYYMMDD格式）
            end_date: 结束日期（YYYYMMDD格式）
            fields: 返回字段（用逗号分隔）

        Returns:
            Dict[str, Any]: 包含股票回购信息的字典
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
            df = pro.repurchase(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_block_trade(
        ts_code: Optional[str] = None,
        trade_date: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取大宗交易

        获取沪深A股的大宗交易数据，包括成交日期、成交价格、
        成交数量、成交金额、买卖营业部等信息。

        Args:
            ts_code: TS代码（多个代码用逗号分隔）
            trade_date: 交易日期（YYYYMMDD格式）
            start_date: 开始日期（YYYYMMDD格式）
            end_date: 结束日期（YYYYMMDD格式）
            fields: 返回字段（用逗号分隔）

        Returns:
            Dict[str, Any]: 包含大宗交易数据的字典
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
            df = pro.block_trade(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_concept(
        src: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取概念股分类表

        获取沪深A股的概念股分类信息，包括概念名称、概念代码、
        概念来源等信息。

        Args:
            src: 来源（ts Tushare概念，下同）
            fields: 返回字段（用逗号分隔）

        Returns:
            Dict[str, Any]: 包含概念股分类信息的字典
        """
        try:
            kwargs = {}
            if src:
                kwargs["src"] = src
            if fields:
                kwargs["fields"] = fields
            df = pro.concept(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_concept_detail(
        id: Optional[str] = None,
        concept_name: Optional[str] = None,
        ts_code: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取概念股明细列表

        获取沪深A股的概念股明细数据，包括概念股代码、
        概念股名称、纳入日期等信息。

        Args:
            id: 概念代码
            concept_name: 概念名称
            ts_code: TS代码（多个代码用逗号分隔）
            fields: 返回字段（用逗号分隔）

        Returns:
            Dict[str, Any]: 包含概念股明细信息的字典
        """
        try:
            kwargs = {}
            if id:
                kwargs["id"] = id
            if concept_name:
                kwargs["concept_name"] = concept_name
            if ts_code:
                kwargs["ts_code"] = ts_code
            if fields:
                kwargs["fields"] = fields
            df = pro.concept_detail(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_margin_detail(
        ts_code: Optional[str] = None,
        trade_date: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取融资融券交易明细

        获取沪深A股的融资融券交易明细数据，包括融资买入额、
        融资偿还额、融券卖出量、融券偿还量等信息。

        Args:
            ts_code: TS代码（多个代码用逗号分隔）
            trade_date: 交易日期（YYYYMMDD格式）
            start_date: 开始日期（YYYYMMDD格式）
            end_date: 结束日期（YYYYMMDD格式）
            fields: 返回字段（用逗号分隔）

        Returns:
            Dict[str, Any]: 包含融资融券交易明细数据的字典
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
            df = pro.margin_detail(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_margin(
        trade_date: Optional[str] = None,
        exchange_id: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取融资融券交易汇总

        获取沪深交易所的融资融券交易汇总数据，包括融资余额、
        融券余量、融资融券余额等信息。

        Args:
            trade_date: 交易日期（YYYYMMDD格式）
            exchange_id: 交易所代码（SSE上交所 SZSE深交所）
            start_date: 开始日期（YYYYMMDD格式）
            end_date: 结束日期（YYYYMMDD格式）
            fields: 返回字段（用逗号分隔）

        Returns:
            Dict[str, Any]: 包含融资融券交易汇总数据的字典
        """
        try:
            kwargs = {}
            if trade_date:
                kwargs["trade_date"] = trade_date
            if exchange_id:
                kwargs["exchange_id"] = exchange_id
            if start_date:
                kwargs["start_date"] = start_date
            if end_date:
                kwargs["end_date"] = end_date
            if fields:
                kwargs["fields"] = fields
            df = pro.margin(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_top_list(
        trade_date: Optional[str] = None,
        ts_code: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取龙虎榜每日明细

        获取沪深A股的龙虎榜每日明细数据，包括上榜股票、
        上榜原因、买入金额、卖出金额等信息。

        Args:
            trade_date: 交易日期（YYYYMMDD格式）
            ts_code: TS代码（多个代码用逗号分隔）
            start_date: 开始日期（YYYYMMDD格式）
            end_date: 结束日期（YYYYMMDD格式）
            fields: 返回字段（用逗号分隔）

        Returns:
            Dict[str, Any]: 包含龙虎榜每日明细数据的字典
        """
        try:
            kwargs = {}
            if trade_date:
                kwargs["trade_date"] = trade_date
            if ts_code:
                kwargs["ts_code"] = ts_code
            if start_date:
                kwargs["start_date"] = start_date
            if end_date:
                kwargs["end_date"] = end_date
            if fields:
                kwargs["fields"] = fields
            df = pro.top_list(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_top_inst(
        trade_date: Optional[str] = None,
        ts_code: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取龙虎榜机构明细

        获取沪深A股的龙虎榜机构明细数据，包括机构专用席位、
        买入金额、卖出金额等信息。

        Args:
            trade_date: 交易日期（YYYYMMDD格式）
            ts_code: TS代码（多个代码用逗号分隔）
            start_date: 开始日期（YYYYMMDD格式）
            end_date: 结束日期（YYYYMMDD格式）
            fields: 返回字段（用逗号分隔）

        Returns:
            Dict[str, Any]: 包含龙虎榜机构明细数据的字典
        """
        try:
            kwargs = {}
            if trade_date:
                kwargs["trade_date"] = trade_date
            if ts_code:
                kwargs["ts_code"] = ts_code
            if start_date:
                kwargs["start_date"] = start_date
            if end_date:
                kwargs["end_date"] = end_date
            if fields:
                kwargs["fields"] = fields
            df = pro.top_inst(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_stk_account(
        date: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取股票开户数据

        获取沪深A股的股票开户数据，包括新增投资者数量、
        期末投资者数量等信息。

        Args:
            date: 统计日期（YYYYMMDD格式）
            start_date: 开始日期（YYYYMMDD格式）
            end_date: 结束日期（YYYYMMDD格式）
            fields: 返回字段（用逗号分隔）

        Returns:
            Dict[str, Any]: 包含股票开户数据的字典
        """
        try:
            kwargs = {}
            if date:
                kwargs["date"] = date
            if start_date:
                kwargs["start_date"] = start_date
            if end_date:
                kwargs["end_date"] = end_date
            if fields:
                kwargs["fields"] = fields
            df = pro.stk_account(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)
