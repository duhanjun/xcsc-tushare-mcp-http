"""
共同基金(Mutual Fund)数据工具模块

本模块提供中国共同基金相关的数据查询工具，包括：
- 基金基本资料
- 基金净值
- 基金经理信息
- 业绩比较基准
- 投资组合（持股、持券、资产配置、行业配置等）
- Wind基金分类

共同基金是向不特定投资者公开发行受益凭证的证券投资基金，
通过汇集众多投资者的资金，由基金托管人托管，基金管理人管理和运用资金。
"""

from typing import Any, Dict, Optional

from .base import format_dataframe, format_error


def register_mutual_fund_tools(mcp, pro):
    """
    注册共同基金相关工具到 MCP 服务器

    该函数将共同基金数据查询工具注册到 MCP 服务器，
    使 AI 助手能够通过 MCP 协议获取中国共同基金相关数据。

    Args:
        mcp: FastMCP 服务器实例，用于注册工具
        pro: XCSC Tushare Pro API 实例，用于获取数据
    """

    @mcp.tool()
    def get_fund_description(
        ts_code: Optional[str] = None,
        fund_name: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取中国共同基金基本资料

        获取共同基金的详细基本信息，包括基金名称、基金类型、
        成立日期、管理公司、托管银行、投资策略等。

        Args:
            ts_code: 基金代码（如 "000001.OF"）
            fund_name: 基金名称（支持模糊查询）
            fields: 返回字段（用逗号分隔，如 "ts_code,name,management"）

        Returns:
            Dict[str, Any]: 包含共同基金基本资料的字典，格式如下：
                {
                    "success": True,
                    "data": [
                        {
                            "ts_code": "000001.OF",
                            "name": "华夏成长混合",
                            "management": "华夏基金管理有限公司",
                            "custodian": "中国建设银行股份有限公司",
                            "fund_type": "混合型",
                            "found_date": "20011218",
                            "invest_strategy": "成长型"
                        }
                    ],
                    "count": 1,
                    "columns": ["ts_code", "name", "management", ...]
                }

        示例:
            >>> get_fund_description(ts_code="000001.OF")
        """
        try:
            kwargs = {}
            if ts_code:
                kwargs["ts_code"] = ts_code
            if fund_name:
                kwargs["fund_name"] = fund_name
            if fields:
                kwargs["fields"] = fields
            df = pro.fund_description(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_mf_nav(
        ts_code: Optional[str] = None,
        end_date: Optional[str] = None,
        start_date: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取中国共同基金净值

        获取共同基金的历史净值数据，包括单位净值、累计净值、
        日增长率等信息。

        Args:
            ts_code: 基金代码（如 "000001.OF"）
            end_date: 结束日期（YYYYMMDD格式）
            start_date: 开始日期（YYYYMMDD格式）
            fields: 返回字段（用逗号分隔）

        Returns:
            Dict[str, Any]: 包含共同基金净值数据的字典，格式如下：
                {
                    "success": True,
                    "data": [
                        {
                            "ts_code": "000001.OF",
                            "nav_date": "20240102",
                            "unit_nav": 1.2345,
                            "accum_nav": 3.4567,
                            "daily_return": 0.0123
                        }
                    ],
                    "count": 1,
                    "columns": ["ts_code", "nav_date", "unit_nav", ...]
                }

        示例:
            >>> get_mf_nav(ts_code="000001.OF", start_date="20240101", end_date="20240131")
        """
        try:
            kwargs = {}
            if ts_code:
                kwargs["ts_code"] = ts_code
            if end_date:
                kwargs["end_date"] = end_date
            if start_date:
                kwargs["start_date"] = start_date
            if fields:
                kwargs["fields"] = fields
            df = pro.mf_nav(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_mf_manager(
        ts_code: Optional[str] = None,
        ann_date: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取中国共同基金基金经理

        获取共同基金的基金经理任职信息，包括基金经理姓名、
        任职日期、离职日期、管理规模等。

        Args:
            ts_code: 基金代码（如 "000001.OF"）
            ann_date: 公告日期（YYYYMMDD格式）
            start_date: 开始日期（YYYYMMDD格式）
            end_date: 结束日期（YYYYMMDD格式）
            fields: 返回字段（用逗号分隔）

        Returns:
            Dict[str, Any]: 包含共同基金基金经理数据的字典，格式如下：
                {
                    "success": True,
                    "data": [
                        {
                            "ts_code": "000001.OF",
                            "manager_name": "张三",
                            "begin_date": "20200101",
                            "end_date": None,
                            "management_scale": 50.5
                        }
                    ],
                    "count": 1,
                    "columns": ["ts_code", "manager_name", "begin_date", ...]
                }

        示例:
            >>> get_mf_manager(ts_code="000001.OF")
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
            df = pro.mf_manager(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_mf_benchmark(
        ts_code: Optional[str] = None,
        end_date: Optional[str] = None,
        start_date: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取中国共同基金业绩比较基准行情

        获取共同基金业绩比较基准的历史行情数据，用于评估
        基金业绩表现。

        Args:
            ts_code: 基金代码（如 "000001.OF"）
            end_date: 结束日期（YYYYMMDD格式）
            start_date: 开始日期（YYYYMMDD格式）
            fields: 返回字段（用逗号分隔）

        Returns:
            Dict[str, Any]: 包含共同基金业绩比较基准行情数据的字典，格式如下：
                {
                    "success": True,
                    "data": [
                        {
                            "ts_code": "000001.OF",
                            "trade_date": "20240102",
                            "benchmark_close": 3000.50,
                            "benchmark_return": 0.015
                        }
                    ],
                    "count": 1,
                    "columns": ["ts_code", "trade_date", "benchmark_close", ...]
                }

        示例:
            >>> get_mf_benchmark(ts_code="000001.OF", start_date="20240101")
        """
        try:
            kwargs = {}
            if ts_code:
                kwargs["ts_code"] = ts_code
            if end_date:
                kwargs["end_date"] = end_date
            if start_date:
                kwargs["start_date"] = start_date
            if fields:
                kwargs["fields"] = fields
            df = pro.mf_benchmark(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_mf_stock_portfolio(
        ts_code: Optional[str] = None,
        ann_date: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        period: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取中国共同基金投资组合-持股明细

        获取共同基金定期报告披露的股票持仓明细，包括持仓股票代码、
        持仓数量、持仓市值、占净值比例等信息。

        Args:
            ts_code: 基金代码（如 "000001.OF"）
            ann_date: 公告日期（YYYYMMDD格式）
            start_date: 开始日期（YYYYMMDD格式）
            end_date: 结束日期（YYYYMMDD格式）
            period: 报告期（如 "20240331" 表示2024年一季报）
            fields: 返回字段（用逗号分隔）

        Returns:
            Dict[str, Any]: 包含共同基金持股明细数据的字典，格式如下：
                {
                    "success": True,
                    "data": [
                        {
                            "ts_code": "000001.OF",
                            "period": "20240331",
                            "symbol": "000001.SZ",
                            "name": "平安银行",
                            "hold_num": 1000000,
                            "hold_value": 15000000.00,
                            "net_asset_ratio": 0.05
                        }
                    ],
                    "count": 1,
                    "columns": ["ts_code", "period", "symbol", ...]
                }

        示例:
            >>> get_mf_stock_portfolio(ts_code="000001.OF", period="20240331")
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
            df = pro.mf_stock_portfolio(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_mf_bond_portfolio(
        ts_code: Optional[str] = None,
        ann_date: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        period: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取中国共同基金投资组合-持券明细

        获取共同基金定期报告披露的债券持仓明细，包括持仓债券代码、
        持仓数量、持仓市值、占净值比例等信息。

        Args:
            ts_code: 基金代码（如 "000001.OF"）
            ann_date: 公告日期（YYYYMMDD格式）
            start_date: 开始日期（YYYYMMDD格式）
            end_date: 结束日期（YYYYMMDD格式）
            period: 报告期（如 "20240331" 表示2024年一季报）
            fields: 返回字段（用逗号分隔）

        Returns:
            Dict[str, Any]: 包含共同基金持券明细数据的字典，格式如下：
                {
                    "success": True,
                    "data": [
                        {
                            "ts_code": "000001.OF",
                            "period": "20240331",
                            "bond_code": "010107.SH",
                            "name": "21国债07",
                            "hold_num": 500000,
                            "hold_value": 50000000.00,
                            "net_asset_ratio": 0.10
                        }
                    ],
                    "count": 1,
                    "columns": ["ts_code", "period", "bond_code", ...]
                }

        示例:
            >>> get_mf_bond_portfolio(ts_code="000001.OF", period="20240331")
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
            df = pro.mf_bond_portfolio(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_mf_asset_allocation(
        ts_code: Optional[str] = None,
        ann_date: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        period: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取中国共同基金投资组合-资产配置

        获取共同基金定期报告披露的资产配置情况，包括股票、债券、
        现金等各类资产占基金净值的比例。

        Args:
            ts_code: 基金代码（如 "000001.OF"）
            ann_date: 公告日期（YYYYMMDD格式）
            start_date: 开始日期（YYYYMMDD格式）
            end_date: 结束日期（YYYYMMDD格式）
            period: 报告期（如 "20240331" 表示2024年一季报）
            fields: 返回字段（用逗号分隔）

        Returns:
            Dict[str, Any]: 包含共同基金资产配置数据的字典，格式如下：
                {
                    "success": True,
                    "data": [
                        {
                            "ts_code": "000001.OF",
                            "period": "20240331",
                            "stock_ratio": 0.65,
                            "bond_ratio": 0.25,
                            "cash_ratio": 0.08,
                            "other_ratio": 0.02
                        }
                    ],
                    "count": 1,
                    "columns": ["ts_code", "period", "stock_ratio", ...]
                }

        示例:
            >>> get_mf_asset_allocation(ts_code="000001.OF", period="20240331")
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
            df = pro.mf_asset_allocation(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_mf_industry_allocation(
        ts_code: Optional[str] = None,
        ann_date: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        period: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取中国共同基金投资组合-行业配置

        获取共同基金定期报告披露的行业配置情况，包括各行业
        占股票投资组合的比例。

        Args:
            ts_code: 基金代码（如 "000001.OF"）
            ann_date: 公告日期（YYYYMMDD格式）
            start_date: 开始日期（YYYYMMDD格式）
            end_date: 结束日期（YYYYMMDD格式）
            period: 报告期（如 "20240331" 表示2024年一季报）
            fields: 返回字段（用逗号分隔）

        Returns:
            Dict[str, Any]: 包含共同基金行业配置数据的字典，格式如下：
                {
                    "success": True,
                    "data": [
                        {
                            "ts_code": "000001.OF",
                            "period": "20240331",
                            "industry_name": "制造业",
                            "industry_ratio": 0.45,
                            "change_ratio": 0.05
                        }
                    ],
                    "count": 1,
                    "columns": ["ts_code", "period", "industry_name", ...]
                }

        示例:
            >>> get_mf_industry_allocation(ts_code="000001.OF", period="20240331")
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
            df = pro.mf_industry_allocation(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_mf_other_portfolio(
        ts_code: Optional[str] = None,
        ann_date: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        period: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取中国共同基金投资组合-其他证券

        获取共同基金定期报告披露的其他证券投资明细，包括权证、
        期货、期权等衍生品投资情况。

        Args:
            ts_code: 基金代码（如 "000001.OF"）
            ann_date: 公告日期（YYYYMMDD格式）
            start_date: 开始日期（YYYYMMDD格式）
            end_date: 结束日期（YYYYMMDD格式）
            period: 报告期（如 "20240331" 表示2024年一季报）
            fields: 返回字段（用逗号分隔）

        Returns:
            Dict[str, Any]: 包含共同基金其他证券数据的字典，格式如下：
                {
                    "success": True,
                    "data": [
                        {
                            "ts_code": "000001.OF",
                            "period": "20240331",
                            "sec_type": "权证",
                            "sec_code": "580000.SH",
                            "hold_value": 1000000.00,
                            "net_asset_ratio": 0.01
                        }
                    ],
                    "count": 1,
                    "columns": ["ts_code", "period", "sec_type", ...]
                }

        示例:
            >>> get_mf_other_portfolio(ts_code="000001.OF", period="20240331")
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
            df = pro.mf_other_portfolio(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_mf_wind_classify(
        ts_code: Optional[str] = None,
        wind_classify: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取中国Wind基金分类

        获取共同基金的Wind分类信息，Wind分类是业内广泛使用的
        基金分类标准，用于基金业绩比较和产品筛选。

        Args:
            ts_code: 基金代码（如 "000001.OF"）
            wind_classify: Wind基金分类（如 "偏股混合型基金"）
            fields: 返回字段（用逗号分隔）

        Returns:
            Dict[str, Any]: 包含Wind基金分类数据的字典，格式如下：
                {
                    "success": True,
                    "data": [
                        {
                            "ts_code": "000001.OF",
                            "wind_classify": "偏股混合型基金",
                            "classify_level": 3,
                            "update_date": "20240101"
                        }
                    ],
                    "count": 1,
                    "columns": ["ts_code", "wind_classify", "classify_level", ...]
                }

        示例:
            >>> get_mf_wind_classify(ts_code="000001.OF")
        """
        try:
            kwargs = {}
            if ts_code:
                kwargs["ts_code"] = ts_code
            if wind_classify:
                kwargs["wind_classify"] = wind_classify
            if fields:
                kwargs["fields"] = fields
            df = pro.mf_wind_classify(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)
