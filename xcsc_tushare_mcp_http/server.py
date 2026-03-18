"""
XCSC Tushare MCP HTTP 服务器主模块

该模块是 XCSC Tushare MCP 服务器的入口点，负责：
1. 初始化 FastMCP 服务器
2. 注册所有工具（股票、指数、基金、期货等）
3. 配置认证中间件
4. 启动 HTTP 服务器
"""

from fastmcp import FastMCP
import xcsc_tushare as ts

from .config import config
from .tools import register_all_tools
from .auth import create_auth_middleware

mcp = FastMCP(
    name=config.MCP_NAME,
    instructions="""
XCSC Tushare MCP Server - 湘财证券金融数据接口服务

本服务提供湘财证券(xcsc-tushare)的金融数据查询功能，包括：
- 沪深股票：基础数据、行情数据、财务数据、市场参考数据
- 指数：指数行情、成分权重
- 公募基金：基金列表、净值、持仓等
- 共同基金：基金资料、净值、投资组合等
- 期货：合约信息、日线行情、持仓排名等
- 期权：合约信息、日线行情
- 债券：可转债基本信息、行情等

使用前请确保已设置 XCSC_TUSHARE_TOKEN 环境变量。
""",
)

ts.set_token(config.XCSC_TUSHARE_TOKEN)
pro = ts.pro_api(env=config.XCSC_ENV, server=config.XCSC_TUSHARE_SERVER)

register_all_tools(mcp, pro)


def main():
    """
    服务器主入口函数

    该函数完成以下任务：
    1. 打印启动信息
    2. 创建并配置 FastMCP HTTP 应用
    3. 根据配置添加认证中间件（如果启用）
    4. 使用 uvicorn 启动 HTTP 服务器
    """
    print(f"正在启动 {config.MCP_NAME}...")
    print(f"XCSC Tushare Token: {config.XCSC_TUSHARE_TOKEN[:10]}***" if config.XCSC_TUSHARE_TOKEN else "警告: 未设置 XCSC_TUSHARE_TOKEN!")
    print(f"环境: {config.XCSC_ENV}")
    print(f"服务器地址: http://{config.MCP_HOST}:{config.MCP_PORT}{config.MCP_PATH}")

    if config.MCP_AUTH_ENABLED:
        print(f"认证: 已启用")
        print(f"API Key: {config.MCP_API_KEY[:8]}...{config.MCP_API_KEY[-4:]}")
    else:
        print(f"认证: 已禁用")

    app = mcp.http_app()

    if config.MCP_AUTH_ENABLED:
        app = create_auth_middleware(
            app,
            api_key=config.MCP_API_KEY,
            auth_enabled=config.MCP_AUTH_ENABLED
        )

    import uvicorn
    uvicorn.run(
        app,
        host=config.MCP_HOST,
        port=config.MCP_PORT,
        timeout_graceful_shutdown=5
    )


if __name__ == "__main__":
    main()
