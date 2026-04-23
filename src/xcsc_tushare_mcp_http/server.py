"""
XCSC Tushare MCP 服务器主模块

该模块是 XCSC Tushare MCP 服务器的入口点，支持两种传输方式：
1. stdio 模式（默认）：通过标准输入输出进行通信
2. HTTP 模式：通过 HTTP 协议进行通信

功能：
1. 初始化 FastMCP 服务器
2. 注册所有工具（get_api_list、get_api_doc、get_api_query）
3. 根据配置选择传输方式启动

启动方式：
1. 安装后通过命令行启动（默认 stdio 模式）：
   $ xcsc-tushare-mcp-http

2. 使用 HTTP 模式：
   $ MCP_TRANSPORT=http xcsc-tushare-mcp-http

3. 作为模块运行：
   $ python -m xcsc_tushare_mcp_http

4. 直接运行 server.py：
   $ python src/xcsc_tushare_mcp_http/server.py

环境变量配置：
    XCSC_TUSHARE_TOKEN: XCSC Tushare API Token（必填）
    XCSC_TUSHARE_SERVER: XCSC Tushare 服务器地址
    MCP_TRANSPORT: 传输方式，'stdio' 或 'http'，默认 'stdio'
    MCP_HOST: 服务器监听地址，默认 0.0.0.0（仅 HTTP 模式）
    MCP_PORT: 服务器监听端口，默认 8000（仅 HTTP 模式）
    MCP_API_KEY: API 认证密钥（仅 HTTP 模式）
    MCP_AUTH_ENABLED: 是否启用认证，默认 true（仅 HTTP 模式）
"""

import logging
import sys
from pathlib import Path

# 支持直接运行 server.py（非模块方式）
if __name__ == "__main__" and __package__ is None:
    file = Path(__file__).resolve()
    root = file.parent.parent.parent
    sys.path.insert(0, str(root / "src"))
    __package__ = "xcsc_tushare_mcp_http"

from fastmcp import FastMCP
import xcsc_tushare as ts
from xcsc_tushare.client import DataApi

from .config import config
from .tools import register_tools
from .auth import create_auth_middleware
from .metadata import load_api_metadata
from . import __version__

# 配置日志
logging.basicConfig(
    level=getattr(logging, config.MCP_LOG_LEVEL, logging.INFO),
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# 创建 FastMCP 服务器实例
mcp = FastMCP(
    name=config.MCP_NAME,
    instructions="""
XCSC Tushare MCP Server - 湘财证券金融数据接口服务

本服务提供湘财证券(XCSC Tushare)的金融数据查询功能，包括：
- 沪深股票：基础数据、行情数据、财务数据、市场参考数据
- 指数：指数行情、指数成分、成分权重、市场交易统计等
- 公募基金：基金列表、净值、持仓、分红、管理人等
- 共同基金：基金资料、净值、投资组合、业绩基准等
- 期货：合约信息、日线行情、持仓排名、仓单日报、结算参数等
- 期权：合约信息、日线行情
- 债券：中国债券基本资料、可转债基本信息、行情、发行、赎回回售信息等

## 🔧 可用工具

本服务提供 **3 个核心工具**：

### 1. get_api_list()
获取所有 API 的列表信息（包含名称、描述、分类）。

### 2. get_api_doc(api_name)
获取指定 API 的详细文档（参数、输出字段、示例）。

### 3. get_api_query(api_name, params)
通用查询 API 接口，调用底层 XCSC Tushare API。

## 🚀 使用流程

1. 调用 get_api_list() 查看所有 API 的列表信息（包含名称、描述、分类）
2. 调用 get_api_doc(api_name) 获取指定 API 的详细文档（参数、输出字段、示例）
3. 调用 get_api_query(api_name, params) 获取数据（params 必须是有效的 JSON 字符串）

## ⚠️ 注意事项

1. api_name 统一：所有工具使用相同的 api_name
2. 参数格式：params 必须是有效的 JSON 字符串
3. 日期格式：YYYYMMDD，如 "20240101"
4. 股票代码：代码.交易所，如 "000001.SZ"、"600000.SH"
""",
)

# 初始化 XCSC Tushare
ts.set_token(config.XCSC_TUSHARE_TOKEN)
pro = DataApi(
    token=config.XCSC_TUSHARE_TOKEN,
    env=config.XCSC_ENV,
    server=config.XCSC_TUSHARE_SERVER,
    timeout=config.XCSC_TUSHARE_TIMEOUT
)

# 加载 API 元数据（自动检测 references/ 目录变化）
load_api_metadata()

# 注册工具到 MCP 服务器
register_tools(mcp, pro)


def main():
    """
    服务器主入口函数
    
    根据配置的传输方式启动相应的服务器。
    """
    logger.info(f"正在启动 {config.MCP_NAME}...")
    logger.info(f"版本: {__version__}")
    logger.info(f"传输方式: {config.MCP_TRANSPORT}")
    
    print(f"正在启动 {config.MCP_NAME}...")
    print(f"版本: {__version__}")
    print(f"传输方式: {config.MCP_TRANSPORT}")
    
    if config.XCSC_TUSHARE_TOKEN:
        logger.info(f"XCSC Tushare Token: {config.XCSC_TUSHARE_TOKEN[:10]}***")
        print(f"XCSC Tushare Token: {config.XCSC_TUSHARE_TOKEN[:10]}***")
    else:
        logger.warning("未设置 XCSC_TUSHARE_TOKEN!")
        print("警告: 未设置 XCSC_TUSHARE_TOKEN!")
    
    logger.info(f"运行环境: {config.XCSC_ENV}")
    
    print(f"运行环境: {config.XCSC_ENV}")

    if config.MCP_TRANSPORT == "stdio":
        _run_stdio_mode()
    else:
        _run_http_mode()


def _run_stdio_mode():
    """
    运行 stdio 模式
    """
    logger.info("启动 stdio 模式...")
    print("启动 stdio 模式...")
    mcp.run()


def _run_http_mode():
    """
    运行 HTTP 模式
    """
    logger.info(f"服务地址: http://{config.MCP_HOST}:{config.MCP_PORT}{config.MCP_PATH}")
    print(f"服务地址: http://{config.MCP_HOST}:{config.MCP_PORT}{config.MCP_PATH}")

    if config.MCP_AUTH_ENABLED:
        logger.info("认证状态: 已启用")
        print(f"认证状态: 已启用")
        print(f"API Key: {config.MCP_API_KEY[:8]}...{config.MCP_API_KEY[-4:]}")
    else:
        logger.info("认证状态: 已禁用")
        print(f"认证状态: 已禁用")

    # 获取 MCP HTTP 应用
    app = mcp.http_app()

    # 添加认证中间件
    if config.MCP_AUTH_ENABLED:
        app = create_auth_middleware(
            app,
            api_key=config.MCP_API_KEY,
            auth_enabled=config.MCP_AUTH_ENABLED
        )

    # 启动 HTTP 服务器
    import uvicorn
    
    logger.info("HTTP 服务器启动中...")
    uvicorn.run(
        app,
        host=config.MCP_HOST,
        port=config.MCP_PORT,
        timeout_graceful_shutdown=5
    )


if __name__ == "__main__":
    main()
