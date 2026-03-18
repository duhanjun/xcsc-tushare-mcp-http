"""
配置模块

该模块负责从环境变量中读取和配置服务器的各项参数。
支持通过环境变量自定义服务器行为，包括：
- XCSC Tushare API Token 和服务器地址
- 服务器监听地址和端口
- API 认证密钥
- 认证功能开关
- 环境配置（prd/dev）

环境变量说明：
- XCSC_TUSHARE_TOKEN: XCSC Tushare Pro API Token（必填）
- XCSC_TUSHARE_SERVER: XCSC Tushare 服务器地址，默认 http://tushare.xcsc.com:7172
- XCSC_ENV: 环境配置，默认 prd
- MCP_HOST: 服务器监听地址，默认 0.0.0.0
- MCP_PORT: 服务器监听端口，默认 8000
- MCP_PATH: MCP 服务路径，默认 /mcp
- MCP_NAME: MCP 服务名称，默认 xcsc-tushare-mcp-http
- MCP_API_KEY: API 认证密钥，未设置时使用默认值
- MCP_AUTH_ENABLED: 是否启用认证，默认 true
"""

import os
import secrets
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


def _get_or_generate_api_key() -> str:
    """
    获取或生成 API Key
    
    如果环境变量 MCP_API_KEY 已设置，则使用其值。
    否则使用默认值。
    
    Returns:
        str: API Key 字符串
    """
    api_key = os.getenv("MCP_API_KEY", "")
    if not api_key:
        api_key = secrets.token_hex(32)
        key_file = Path.home() / ".xcsc_tushare_mcp_api_key"
        if key_file.exists():
            api_key = key_file.read_text().strip()
        else:
            key_file.write_text(api_key)
            key_file.chmod(0o600)
    return api_key


@dataclass
class Config:
    """
    服务器配置类
    
    使用 dataclass 存储所有配置项，所有值从环境变量读取，
    提供了合理的默认值。
    
    Attributes:
        XCSC_TUSHARE_TOKEN: XCSC Tushare API Token
        XCSC_TUSHARE_SERVER: XCSC Tushare 服务器地址
        XCSC_ENV: 环境配置（prd/dev）
        MCP_HOST: 服务器监听地址
        MCP_PORT: 服务器监听端口
        MCP_PATH: MCP 服务路径
        MCP_NAME: MCP 服务名称
        MCP_API_KEY: API 认证密钥
        MCP_AUTH_ENABLED: 是否启用认证
    """
    
    # XCSC Tushare API Token，从环境变量读取
    XCSC_TUSHARE_TOKEN: str = os.getenv("XCSC_TUSHARE_TOKEN", "")
    
    # XCSC Tushare 服务器地址
    XCSC_TUSHARE_SERVER: str = os.getenv("XCSC_TUSHARE_SERVER", "http://tushare.xcsc.com:7172")
    
    # 环境配置（prd/dev）
    XCSC_ENV: str = os.getenv("XCSC_ENV", "prd")
    
    # 服务器监听地址，默认 0.0.0.0（监听所有网卡）
    MCP_HOST: str = os.getenv("MCP_HOST", "0.0.0.0")
    
    # 服务器监听端口，默认 8000
    MCP_PORT: int = int(os.getenv("MCP_PORT", "8000"))
    
    # MCP 服务路径，默认 /mcp
    MCP_PATH: str = os.getenv("MCP_PATH", "/mcp")
    
    # MCP 服务名称，用于显示和标识
    MCP_NAME: str = os.getenv("MCP_NAME", "xcsc-tushare-mcp-http")
    
    # API 认证密钥，用于保护 API 访问安全
    MCP_API_KEY: str = _get_or_generate_api_key()
    
    # 是否启用认证，默认启用以保证安全
    MCP_AUTH_ENABLED: bool = os.getenv("MCP_AUTH_ENABLED", "true").lower() == "true"

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
            Optional[str]: 如果配置无效返回错误信息，否则返回 None
        """
        if not self.XCSC_TUSHARE_TOKEN:
            return "XCSC_TUSHARE_TOKEN 环境变量是必填项"
        return None


# 全局配置实例
config = Config.from_env()
