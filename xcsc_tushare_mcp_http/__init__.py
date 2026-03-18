"""
XCSC Tushare MCP HTTP 服务器包

该包提供基于 XCSC Tushare 的 MCP 服务器实现，
支持通过 HTTP 协议为 AI 助手提供湘财证券金融数据查询服务。

主要模块：
- server: 服务器主模块，负责初始化 FastMCP 和启动 HTTP 服务
- config: 配置管理模块，从环境变量读取配置参数
- auth: 认证中间件模块，提供 API Key 认证功能
- tools: 数据查询工具模块，包含各类金融数据查询接口

示例用法：
    >>> from xcsc_tushare_mcp_http import main
    >>> main()
    
    或者通过命令行：
    $ xcsc-tushare-mcp-http
"""

__version__ = "0.1.0"
__author__ = "HanjunDu"
__email__ = "hanjun.du@outlook.com"

from .server import main, mcp
from .config import config, Config
from .auth import AuthMiddleware, create_auth_middleware

__all__ = [
    "main",
    "mcp", 
    "config",
    "Config",
    "AuthMiddleware",
    "create_auth_middleware",
    "__version__",
]
