"""
股票财务数据工具模块

该模块提供股票财务报表相关的数据查询工具，包括：
- 利润表查询
- 资产负债表查询
- 现金流量表查询
- 重要财务指标查询
- 业绩预告查询
- 业绩快报查询
- 分红送股查询
- 主营业务构成查询
- 财务审计意见查询
- 财报披露计划查询

这些工具主要用于获取上市公司的财务数据和业绩信息。
"""

from typing import Any, Dict, Optional

from .base import format_dataframe, format_error


def register_stock_finance_tools(mcp, pro):
    """
    注册股票财务数据工具到 MCP 服务器

    该函数注册所有股票财务数据相关的工具，包括利润表、资产负债表、
    现金流量表、财务指标、业绩预告、分红送股等。

    Args:
        mcp: FastMCP 服务器实例
        pro: XCSC Tushare Pro API 实例
    """

    @mcp.tool()
    def get_income(
        ts_code: Optional[str] = None,
        ann_date: Optional[str] = None,
        f_ann_date: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        period: Optional[str] = None,
        report_type: Optional[str] = None,
        comp_type: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取利润表

        获取沪深A股上市公司的利润表数据，包括营业收入、营业成本、
        营业利润、净利润、每股收益等财务数据。

        Args:
            ts_code: TS代码（多个代码用逗号分隔）
            ann_date: 公告日期（YYYYMMDD格式）
            f_ann_date: 实际公告日期（YYYYMMDD格式）
            start_date: 开始日期（YYYYMMDD格式）
            end_date: 结束日期（YYYYMMDD格式）
            period: 报告期（YYYYMMDD格式，如20241231表示2024年年报）
            report_type: 报告类型（1合并报表 2单季合并 3调整单季合并表 4调整合并报表 5调整前合并报表）
            comp_type: 公司类型（1一般工商业 2银行 3保险 4证券）
            fields: 返回字段（用逗号分隔）

        Returns:
            Dict[str, Any]: 包含利润表数据的字典
        """
        try:
            kwargs = {}
            if ts_code:
                kwargs["ts_code"] = ts_code
            if ann_date:
                kwargs["ann_date"] = ann_date
            if f_ann_date:
                kwargs["f_ann_date"] = f_ann_date
            if start_date:
                kwargs["start_date"] = start_date
            if end_date:
                kwargs["end_date"] = end_date
            if period:
                kwargs["period"] = period
            if report_type:
                kwargs["report_type"] = report_type
            if comp_type:
                kwargs["comp_type"] = comp_type
            if fields:
                kwargs["fields"] = fields
            df = pro.income(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_balancesheet(
        ts_code: Optional[str] = None,
        ann_date: Optional[str] = None,
        f_ann_date: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        period: Optional[str] = None,
        report_type: Optional[str] = None,
        comp_type: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取资产负债表

        获取沪深A股上市公司的资产负债表数据，包括资产总额、负债总额、
        所有者权益、流动资产、非流动资产等财务数据。

        Args:
            ts_code: TS代码（多个代码用逗号分隔）
            ann_date: 公告日期（YYYYMMDD格式）
            f_ann_date: 实际公告日期（YYYYMMDD格式）
            start_date: 开始日期（YYYYMMDD格式）
            end_date: 结束日期（YYYYMMDD格式）
            period: 报告期（YYYYMMDD格式）
            report_type: 报告类型
            comp_type: 公司类型（1一般工商业 2银行 3保险 4证券）
            fields: 返回字段（用逗号分隔）

        Returns:
            Dict[str, Any]: 包含资产负债表数据的字典
        """
        try:
            kwargs = {}
            if ts_code:
                kwargs["ts_code"] = ts_code
            if ann_date:
                kwargs["ann_date"] = ann_date
            if f_ann_date:
                kwargs["f_ann_date"] = f_ann_date
            if start_date:
                kwargs["start_date"] = start_date
            if end_date:
                kwargs["end_date"] = end_date
            if period:
                kwargs["period"] = period
            if report_type:
                kwargs["report_type"] = report_type
            if comp_type:
                kwargs["comp_type"] = comp_type
            if fields:
                kwargs["fields"] = fields
            df = pro.balancesheet(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_cashflow(
        ts_code: Optional[str] = None,
        ann_date: Optional[str] = None,
        f_ann_date: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        period: Optional[str] = None,
        report_type: Optional[str] = None,
        comp_type: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取现金流量表

        获取沪深A股上市公司的现金流量表数据，包括经营活动现金流量、
        投资活动现金流量、筹资活动现金流量等财务数据。

        Args:
            ts_code: TS代码（多个代码用逗号分隔）
            ann_date: 公告日期（YYYYMMDD格式）
            f_ann_date: 实际公告日期（YYYYMMDD格式）
            start_date: 开始日期（YYYYMMDD格式）
            end_date: 结束日期（YYYYMMDD格式）
            period: 报告期（YYYYMMDD格式）
            report_type: 报告类型
            comp_type: 公司类型（1一般工商业 2银行 3保险 4证券）
            fields: 返回字段（用逗号分隔）

        Returns:
            Dict[str, Any]: 包含现金流量表数据的字典
        """
        try:
            kwargs = {}
            if ts_code:
                kwargs["ts_code"] = ts_code
            if ann_date:
                kwargs["ann_date"] = ann_date
            if f_ann_date:
                kwargs["f_ann_date"] = f_ann_date
            if start_date:
                kwargs["start_date"] = start_date
            if end_date:
                kwargs["end_date"] = end_date
            if period:
                kwargs["period"] = period
            if report_type:
                kwargs["report_type"] = report_type
            if comp_type:
                kwargs["comp_type"] = comp_type
            if fields:
                kwargs["fields"] = fields
            df = pro.cashflow(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_fina_indicator(
        ts_code: Optional[str] = None,
        ann_date: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        period: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取重要财务指标

        获取沪深A股上市公司的重要财务指标数据，包括盈利能力指标、
        偿债能力指标、运营能力指标、成长能力指标等。

        Args:
            ts_code: TS代码（多个代码用逗号分隔）
            ann_date: 公告日期（YYYYMMDD格式）
            start_date: 开始日期（YYYYMMDD格式）
            end_date: 结束日期（YYYYMMDD格式）
            period: 报告期（YYYYMMDD格式）
            fields: 返回字段（用逗号分隔）

        Returns:
            Dict[str, Any]: 包含重要财务指标数据的字典
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
            if period:
                kwargs["period"] = period
            if fields:
                kwargs["fields"] = fields
            df = pro.fina_indicator(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_forecast(
        ts_code: Optional[str] = None,
        ann_date: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        period: Optional[str] = None,
        type: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取业绩预告

        获取沪深A股上市公司的业绩预告数据，包括预告类型、
        预告净利润变动幅度、预告内容等信息。

        Args:
            ts_code: TS代码（多个代码用逗号分隔）
            ann_date: 公告日期（YYYYMMDD格式）
            start_date: 开始日期（YYYYMMDD格式）
            end_date: 结束日期（YYYYMMDD格式）
            period: 报告期（YYYYMMDD格式）
            type: 预告类型（预增/预减/预盈/预亏等）
            fields: 返回字段（用逗号分隔）

        Returns:
            Dict[str, Any]: 包含业绩预告数据的字典
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
            if period:
                kwargs["period"] = period
            if type:
                kwargs["type"] = type
            if fields:
                kwargs["fields"] = fields
            df = pro.forecast(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_express(
        ts_code: Optional[str] = None,
        ann_date: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        period: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取业绩快报

        获取沪深A股上市公司的业绩快报数据，包括营业收入、
        营业利润、利润总额、净利润等核心财务数据。

        Args:
            ts_code: TS代码（多个代码用逗号分隔）
            ann_date: 公告日期（YYYYMMDD格式）
            start_date: 开始日期（YYYYMMDD格式）
            end_date: 结束日期（YYYYMMDD格式）
            period: 报告期（YYYYMMDD格式）
            fields: 返回字段（用逗号分隔）

        Returns:
            Dict[str, Any]: 包含业绩快报数据的字典
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
            if period:
                kwargs["period"] = period
            if fields:
                kwargs["fields"] = fields
            df = pro.express(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_dividend(
        ts_code: Optional[str] = None,
        ann_date: Optional[str] = None,
        record_date: Optional[str] = None,
        ex_date: Optional[str] = None,
        imp_ann_date: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取分红送股

        获取沪深A股上市公司的分红送股数据，包括分红方案、
        股权登记日、除权除息日、派息日等信息。

        Args:
            ts_code: TS代码（多个代码用逗号分隔）
            ann_date: 公告日期（YYYYMMDD格式）
            record_date: 股权登记日（YYYYMMDD格式）
            ex_date: 除权除息日（YYYYMMDD格式）
            imp_ann_date: 实施公告日（YYYYMMDD格式）
            fields: 返回字段（用逗号分隔）

        Returns:
            Dict[str, Any]: 包含分红送股数据的字典
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
            if imp_ann_date:
                kwargs["imp_ann_date"] = imp_ann_date
            if fields:
                kwargs["fields"] = fields
            df = pro.dividend(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_fina_mainbz(
        ts_code: Optional[str] = None,
        period: Optional[str] = None,
        type: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取主营业务构成

        获取沪深A股上市公司的主营业务构成数据，包括各业务板块的
        营业收入、营业成本、毛利率等信息。

        Args:
            ts_code: TS代码（多个代码用逗号分隔）
            period: 报告期（YYYYMMDD格式）
            type: 类型（P按产品 D按地区）
            start_date: 开始日期（YYYYMMDD格式）
            end_date: 结束日期（YYYYMMDD格式）
            fields: 返回字段（用逗号分隔）

        Returns:
            Dict[str, Any]: 包含主营业务构成数据的字典
        """
        try:
            kwargs = {}
            if ts_code:
                kwargs["ts_code"] = ts_code
            if period:
                kwargs["period"] = period
            if type:
                kwargs["type"] = type
            if start_date:
                kwargs["start_date"] = start_date
            if end_date:
                kwargs["end_date"] = end_date
            if fields:
                kwargs["fields"] = fields
            df = pro.fina_mainbz(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_fina_audit(
        ts_code: Optional[str] = None,
        ann_date: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        period: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取财务审计意见

        获取沪深A股上市公司的财务审计意见数据，包括审计意见类型、
        审计机构、签字会计师等信息。

        Args:
            ts_code: TS代码（多个代码用逗号分隔）
            ann_date: 公告日期（YYYYMMDD格式）
            start_date: 开始日期（YYYYMMDD格式）
            end_date: 结束日期（YYYYMMDD格式）
            period: 报告期（YYYYMMDD格式）
            fields: 返回字段（用逗号分隔）

        Returns:
            Dict[str, Any]: 包含财务审计意见数据的字典
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
            if period:
                kwargs["period"] = period
            if fields:
                kwargs["fields"] = fields
            df = pro.fina_audit(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_report_rcd(
        ts_code: Optional[str] = None,
        end_date: Optional[str] = None,
        pre_date: Optional[str] = None,
        actual_date: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取财报披露计划

        获取沪深A股上市公司的财报披露计划数据，包括预约披露日期、
        实际披露日期、披露进度等信息。

        Args:
            ts_code: TS代码（多个代码用逗号分隔）
            end_date: 财报截止日期（YYYYMMDD格式）
            pre_date: 预约披露日期（YYYYMMDD格式）
            actual_date: 实际披露日期（YYYYMMDD格式）
            fields: 返回字段（用逗号分隔）

        Returns:
            Dict[str, Any]: 包含财报披露计划数据的字典
        """
        try:
            kwargs = {}
            if ts_code:
                kwargs["ts_code"] = ts_code
            if end_date:
                kwargs["end_date"] = end_date
            if pre_date:
                kwargs["pre_date"] = pre_date
            if actual_date:
                kwargs["actual_date"] = actual_date
            if fields:
                kwargs["fields"] = fields
            df = pro.report_rcd(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)
