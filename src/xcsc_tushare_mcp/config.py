"""
配置模块

该模块负责从环境变量中读取和配置服务器的各项参数。

支持的环境变量：
    XCSC_TUSHARE_TOKEN: XCSC Tushare API Token（必填）
    XCSC_TUSHARE_SERVER: XCSC Tushare 服务器地址，默认 http://tushare.xcsc.com:7172
    XCSC_ENV: 运行环境，默认 prd
    MCP_TRANSPORT: 传输方式，可选 'stdio' 或 'http'，默认 'stdio'
    MCP_HOST: 服务器监听地址，默认 0.0.0.0（仅 HTTP 模式）
    MCP_PORT: 服务器监听端口，默认 8000（仅 HTTP 模式）
    MCP_PATH: MCP 服务路径，默认 /mcp（仅 HTTP 模式）
    MCP_NAME: 服务名称，默认 xcsc-tushare-mcp
    MCP_API_KEY: API 认证密钥，未设置时自动生成（仅 HTTP 模式）
    MCP_AUTH_ENABLED: 是否启用认证，默认 true（仅 HTTP 模式）
    MCP_LOG_LEVEL: 日志级别，默认 INFO
    MCP_AUTO_GENERATE_METADATA: 是否自动重新生成元数据，默认 true
    XCSC_TUSHARE_TIMEOUT: API 请求超时时间（秒），默认 60

使用示例：
    >>> from xcsc_tushare_mcp.config import config
    >>> print(config.MCP_HOST)
    '0.0.0.0'
"""

import os
import secrets
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


def _get_or_generate_api_key() -> str:
    """
    获取或生成 API Key
    
    如果环境变量 MCP_API_KEY 未设置，则尝试从 ~/.xcsc_tushare_mcp_api_key 文件读取。
    如果文件也不存在，则生成一个新的随机 API Key 并保存到该文件。
    
    Returns:
        str: API Key
    """
    api_key = os.getenv("MCP_API_KEY", "")
    if not api_key:
        key_file = Path.home() / ".xcsc_tushare_mcp_api_key"
        if key_file.exists():
            api_key = key_file.read_text().strip()
        else:
            api_key = secrets.token_hex(32)
            key_file.write_text(api_key)
            key_file.chmod(0o600)
    return api_key


@dataclass
class Config:
    """
    服务器配置类
    
    该类通过 dataclass 定义，所有配置项都可以从环境变量读取。
    
    Attributes:
        XCSC_TUSHARE_TOKEN: XCSC Tushare API Token
        XCSC_TUSHARE_SERVER: XCSC Tushare 服务器地址
        XCSC_ENV: 运行环境
        MCP_TRANSPORT: 传输方式，'stdio' 或 'http'
        MCP_HOST: 服务器监听地址
        MCP_PORT: 服务器监听端口
        MCP_PATH: MCP 服务路径
        MCP_NAME: 服务名称
        MCP_API_KEY: API 认证密钥
        MCP_AUTH_ENABLED: 是否启用认证
        MCP_LOG_LEVEL: 日志级别
        MCP_AUTO_GENERATE_METADATA: 是否自动重新生成元数据
        XCSC_TUSHARE_TIMEOUT: API 请求超时时间（秒）
    """
    
    XCSC_TUSHARE_TOKEN: str = os.getenv("XCSC_TUSHARE_TOKEN", "")
    XCSC_TUSHARE_SERVER: str = os.getenv("XCSC_TUSHARE_SERVER", "http://tushare.xcsc.com:7172")
    XCSC_ENV: str = os.getenv("XCSC_ENV", "prd")
    MCP_TRANSPORT: str = os.getenv("MCP_TRANSPORT", "stdio").lower()
    MCP_HOST: str = os.getenv("MCP_HOST", "0.0.0.0")
    MCP_PORT: int = int(os.getenv("MCP_PORT", "8000"))
    MCP_PATH: str = os.getenv("MCP_PATH", "/mcp")
    MCP_NAME: str = os.getenv("MCP_NAME", "xcsc-tushare-mcp")
    MCP_API_KEY: str = _get_or_generate_api_key()
    MCP_AUTH_ENABLED: bool = os.getenv("MCP_AUTH_ENABLED", "true").lower() == "true"
    MCP_LOG_LEVEL: str = os.getenv("MCP_LOG_LEVEL", "INFO")
    MCP_AUTO_GENERATE_METADATA: bool = os.getenv("MCP_AUTO_GENERATE_METADATA", "true").lower() == "true"
    XCSC_TUSHARE_TIMEOUT: int = int(os.getenv("XCSC_TUSHARE_TIMEOUT", "60"))
    
    def __post_init__(self):
        """
        初始化后验证传输方式
        """
        if self.MCP_TRANSPORT not in ["stdio", "http"]:
            self.MCP_TRANSPORT = "stdio"

    @classmethod
    def from_env(cls) -> "Config":
        """
        从环境变量创建配置实例
        
        Returns:
            Config: 配置实例
        """
        return cls()

    def validate(self) -> Optional[str]:
        """
        验证配置是否有效
        
        Returns:
            Optional[str]: 如果配置无效，返回错误信息；否则返回 None
        """
        if not self.XCSC_TUSHARE_TOKEN:
            return "XCSC_TUSHARE_TOKEN 环境变量是必填项"
        return None


# 全局配置实例
config = Config.from_env()
