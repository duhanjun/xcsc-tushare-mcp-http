"""
XCSC Tushare MCP HTTP 服务器包

该包提供基于 XCSC Tushare 的 MCP 服务器实现，支持通过 HTTP 协议
获取湘财证券金融数据。

主要功能：
- 提供 3 个核心 MCP 工具：get_api_list, get_api_doc, get_api_query
- 支持动态元数据生成，自动从 references/ 目录解析 API 文档
- 内置 API Key 认证
- 支持 HTTP 传输协议

环境变量：
    XCSC_TUSHARE_TOKEN: XCSC Tushare API Token（必填）
    XCSC_TUSHARE_SERVER: XCSC Tushare 服务器地址
    MCP_HOST: 服务器监听地址，默认 0.0.0.0
    MCP_PORT: 服务器监听端口，默认 8000
    MCP_API_KEY: API 认证密钥
    MCP_AUTH_ENABLED: 是否启用认证，默认 true
"""

__version__ = "1.0.0"
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
