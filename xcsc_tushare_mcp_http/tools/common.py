"""
通用工具模块

该模块提供与 XCSC Tushare API 相关的通用工具函数：
1. xcsc_query: 通用 API 查询接口，可调用任意 XCSC Tushare API
2. get_api_list: 获取支持的 API 接口列表
3. get_api_doc: 获取指定 API 接口的详细文档
4. test_connection: 测试 XCSC Tushare API 连接状态

这些工具不直接访问具体数据，而是提供 API 元信息查询和通用查询功能。
"""

from typing import Any, Dict, Optional
import json

from .base import format_dataframe, format_error


def register_common_tools(mcp, pro):
    """
    注册通用工具到 MCP 服务器

    该函数注册所有通用工具，包括通用查询接口、API 列表查询、
    API 文档查询和连接测试工具。

    Args:
        mcp: FastMCP 服务器实例
        pro: XCSC Tushare Pro API 实例
    """

    @mcp.tool()
    def xcsc_query(api_name: str, params: Optional[str] = None) -> Dict[str, Any]:
        """
        通用 XCSC Tushare API 查询接口

        通过该接口可以调用任意 XCSC Tushare API，只需传入 API 名称和参数。
        适用于工具列表中未封装的 API 接口。

        Args:
            api_name: API 接口名称，如 'daily', 'stock_basic', 'index_daily' 等
            params: JSON 格式的参数字符串，如 '{"ts_code": "000001.SZ", "start_date": "20240101"}'

        Returns:
            Dict[str, Any]: 包含查询结果的字典，格式如下：
                {
                    "success": bool,  # 查询是否成功
                    "data": list,     # 数据列表
                    "count": int,     # 记录数量
                    "columns": list   # 字段列表
                }

        示例：
            xcsc_query("daily", '{"ts_code": "000001.SZ", "trade_date": "20240101"}')
        """
        try:
            kwargs = {}
            if params:
                kwargs = json.loads(params)
            df = getattr(pro, api_name)(**kwargs)
            return format_dataframe(df)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_api_list() -> Dict[str, Any]:
        """
        获取支持的 API 接口列表

        返回 XCSC Tushare 支持的所有 API 分类和接口名称，
        包括股票、指数、基金、期货、期权、债券等类别。

        Returns:
            Dict[str, Any]: 包含 API 分类和接口列表的响应，格式如下：
                {
                    "success": True,
                    "data": {
                        "category_name": {
                            "api_name": "api_description"
                        }
                    }
                }
        """
        api_list = {
            "common": {
                "query": "通用查询接口",
                "trade_cal": "交易日历",
            },
            "stock_basic": {
                "stock_basic": "中国A股基本资料",
                "namechange": "中国A股证券曾用名",
                "stock_company": "中国A股公司简介",
                "stk_managers": "上市公司管理层",
                "stk_managers_salary": "管理层薪酬和持股",
            },
            "stock_quote": {
                "daily": "中国A股日行情",
                "weekly": "周线行情",
                "monthly": "月线行情",
                "stk_mins": "分钟数据",
                "daily_basic_ts": "每日指标",
                "suspend": "A股停复牌信息",
                "stk_limit": "每日涨跌停价格",
                "adj_factor": "股票复权因子",
                "limit_list": "涨跌停和炸板数据",
                "moneyflow": "个股资金流向",
            },
            "stock_hkconnect": {
                "ggt_top10": "港股通十大成交股",
                "ggt_daily": "港股通(沪)每日成交",
                "ggt_daily_stat": "港股通每日成交统计",
                "ggt_monthly_stat": "港股通每月成交统计",
                "hk_hold": "沪深港股通持股明细",
                "ggt_moneyflow": "沪深港通资金流向",
                "sggt_top10": "沪深股通十大成交股",
            },
            "stock_finance": {
                "income": "利润表",
                "balancesheet": "资产负债表",
                "cashflow": "现金流量表",
                "fina_indicator": "重要财务指标",
                "forecast": "业绩预告",
                "express": "业绩快报",
                "dividend": "分红送股",
                "fina_mainbz": "主营业务构成",
                "fina_audit": "财务审计意见",
                "report_rcd": "财报披露计划",
            },
            "stock_market": {
                "top10_holders": "前十大股东",
                "top10_floatholders": "前十大流通股东",
                "stk_holdernumber": "股东人数",
                "stk_sharechange": "股东增减持",
                "share_float": "股权质押明细数据",
                "share_float_stat": "股权质押统计数据",
                "repurchase": "股票回购",
                "block_trade": "大宗交易",
                "concept": "概念股分类表",
                "concept_detail": "概念股明细列表",
                "margin_detail": "融资融券交易明细",
                "margin": "融资融券交易汇总",
                "top_list": "龙虎榜每日明细",
                "top_inst": "龙虎榜机构明细",
                "stk_account": "股票开户数据",
            },
            "index": {
                "index_daily": "A股指数日行情",
                "index_weekly": "指数周线行情",
                "index_monthly": "指数月线行情",
                "index_weight": "指数成分和权重",
                "index_basic": "A股指数成份股",
                "index_dailybasic": "大盘指数每日指标",
                "daily_info": "市场每日交易统计",
                "sz_daily_info": "深圳市场每日交易概况",
            },
            "fund": {
                "fund_basic": "基金列表",
                "fund_nav": "基金净值",
                "fund_daily": "基金行情",
                "fund_div": "基金分红",
                "fund_portfolio": "基金持仓",
                "fund_manager": "基金经理",
                "fund_company": "基金管理人",
                "fund_share": "基金规模",
            },
            "mutual_fund": {
                "fund_description": "中国共同基金基本资料",
                "mf_nav": "中国共同基金净值",
                "mf_manager": "中国共同基金基金经理",
                "mf_benchmark": "中国共同基金业绩比较基准行情",
                "mf_stock_portfolio": "中国共同基金投资组合-持股明细",
                "mf_bond_portfolio": "中国共同基金投资组合-持券明细",
                "mf_asset_allocation": "中国共同基金投资组合-资产配置",
                "mf_industry_allocation": "中国共同基金投资组合-行业配置",
                "mf_other_portfolio": "中国共同基金投资组合-其他证券",
                "mf_wind_classify": "中国Wind基金分类",
            },
            "futures": {
                "fut_basic": "期货合约信息",
                "fut_daily": "期货日线行情",
                "fut_holding": "每日持仓排名",
                "fut_settle": "每日结算参数",
                "fut_mapping": "期货主力与连续合约",
                "fut_wsr": "仓单日报",
            },
            "option": {
                "opt_basic": "期权合约信息",
                "opt_daily": "期权日线行情",
            },
            "bond": {
                "cb_basic": "可转债基本信息",
                "cb_daily": "可转债行情",
                "cb_issue": "可转债发行",
                "cb_call": "可转债有条件赎回价格和触发比例",
                "cb_put": "可转债有条件回售价格和触发比例",
                "cb_force_call": "可转债强制赎回信息",
                "bond_basic": "中国债券基本资料",
            },
        }
        return {"success": True, "data": api_list}

    @mcp.tool()
    def get_api_doc(api_name: str) -> Dict[str, Any]:
        """
        获取指定 API 的文档说明

        根据 API 名称返回该接口的详细文档，包括：
        - 接口描述
        - 输入参数说明
        - 返回字段列表

        Args:
            api_name: API 接口名称，如 'stock_basic', 'daily', 'index_daily' 等

        Returns:
            Dict[str, Any]: 包含 API 接口文档的字典，格式如下：
                {
                    "success": True,
                    "data": {
                        "description": "接口描述",
                        "input_params": {"param_name": "param_description"},
                        "output_params": ["field1", "field2", ...]
                    }
                }
            如果 API 不存在，返回错误信息。
        """
        docs = {
            "stock_basic": {
                "description": "获取A股基本资料信息",
                "input_params": {
                    "ts_code": "TS代码（多个代码用逗号分隔）",
                    "exchange": "交易所代码（SSE上交所 SZSE深交所）",
                    "is_shsc": "是否沪深港通标的（N否 H沪股通 S深股通）",
                    "start_date": "开始日期",
                    "end_date": "结束日期",
                },
                "output_params": [
                    "ts_code",
                    "symbol",
                    "name",
                    "comp_name",
                    "exchange",
                    "area",
                    "industry",
                    "market",
                    "list_date",
                    "is_hs",
                    "delist_date",
                ],
            },
            "daily": {
                "description": "获取A股日行情数据",
                "input_params": {
                    "ts_code": "TS代码（多个代码用逗号分隔）",
                    "trade_date": "交易日期（YYYYMMDD格式）",
                    "start_date": "开始日期",
                    "end_date": "结束日期",
                },
                "output_params": [
                    "ts_code",
                    "trade_date",
                    "open",
                    "high",
                    "low",
                    "close",
                    "pre_close",
                    "change",
                    "pct_chg",
                    "vol",
                    "amount",
                ],
            },
            "index_daily": {
                "description": "获取A股指数日行情数据",
                "input_params": {
                    "ts_code": "指数代码",
                    "trade_date": "交易日期（YYYYMMDD格式）",
                    "start_date": "开始日期",
                    "end_date": "结束日期",
                },
                "output_params": [
                    "ts_code",
                    "trade_date",
                    "close",
                    "open",
                    "high",
                    "low",
                    "pre_close",
                    "change",
                    "pct_chg",
                    "vol",
                    "amount",
                ],
            },
            "trade_cal": {
                "description": "获取各大交易所交易日历数据",
                "input_params": {
                    "exchange": "交易所（SSE上交所 SZSE深交所 CFFEX中金所等）",
                    "start_date": "开始日期",
                    "end_date": "结束日期",
                    "is_open": "是否交易（0休市 1交易）",
                },
                "output_params": ["exchange", "cal_date", "is_open", "pretrade_date"],
            },
        }

        if api_name in docs:
            return {"success": True, "data": docs[api_name]}
        else:
            return {
                "success": False,
                "error": f"未找到 API '{api_name}' 的文档。请使用 get_api_list() 查看所有可用 API。",
            }

    @mcp.tool()
    def test_connection() -> Dict[str, Any]:
        """
        测试 XCSC Tushare API 连接状态

        通过调用交易日历接口来验证 XCSC Tushare API 连接是否正常。

        Returns:
            Dict[str, Any]: 连接测试结果，格式如下：
                {
                    "success": True/False,
                    "message": "连接状态描述",
                    "sample_records": int  # 获取到的记录数
                }
        """
        try:
            df = pro.trade_cal(start_date="20240101", end_date="20240110")
            return {
                "success": True,
                "message": "XCSC Tushare API 连接正常",
                "sample_records": len(df) if df is not None else 0,
            }
        except Exception as e:
            return format_error(e)
