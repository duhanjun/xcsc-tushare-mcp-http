"""
XCSC Tushare MCP 服务器包

该包提供基于 XCSC Tushare 的 MCP 服务器实现，支持 stdio 和 HTTP 两种
传输协议，为 AI 助手提供湘财证券金融数据接口。

主要功能：
- 提供 3 个核心 MCP 工具：get_api_list, get_api_doc, get_api_query
- 支持动态元数据生成，自动从 references/ 目录解析 API 文档
- HTTP 模式下支持 API Key 认证
- 支持 stdio 和 HTTP 两种传输方式

环境变量：
    XCSC_TUSHARE_TOKEN: XCSC Tushare API Token（必填）
    XCSC_TUSHARE_SERVER: XCSC Tushare 服务器地址
    XCSC_ENV: 运行环境，默认 prd
    MCP_TRANSPORT: 传输方式，stdio 或 http，默认 stdio
    MCP_HOST: 服务器监听地址，默认 0.0.0.0（仅 HTTP 模式）
    MCP_PORT: 服务器监听端口，默认 8000（仅 HTTP 模式）
    MCP_PATH: MCP 服务路径，默认 /mcp（仅 HTTP 模式）
    MCP_NAME: 服务名称，默认 xcsc-tushare-mcp
    MCP_API_KEY: API 认证密钥（仅 HTTP 模式）
    MCP_AUTH_ENABLED: 是否启用认证，默认 true（仅 HTTP 模式）
    MCP_LOG_LEVEL: 日志级别，默认 INFO
    MCP_AUTO_GENERATE_METADATA: 是否自动重新生成元数据，默认 true
    XCSC_TUSHARE_TIMEOUT: API 请求超时时间（秒），默认 60
"""

__version__ = "1.1.0"
__author__ = "HanjunDu"
__email__ = "hanjun.du@outlook.com"

from .config import config, Config
from .auth import AuthMiddleware, create_auth_middleware

__all__ = [
    "config",
    "Config",
    "AuthMiddleware",
    "create_auth_middleware",
    "__version__",
]
