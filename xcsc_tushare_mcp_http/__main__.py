"""
命令行入口模块

该模块作为包的命令行入口点，允许通过以下方式运行服务器：
- python -m xcsc_tushare_mcp_http
- xcsc-tushare-mcp-http（安装后）

启动服务器时会自动加载配置并初始化所有工具。
"""

import logging
import os

from .config import config
from .server import mcp

# 配置日志格式
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


def main():
    """
    服务器主入口函数
    
    该函数完成以下任务：
    1. 验证配置是否有效
    2. 打印启动信息
    3. 启动 FastMCP HTTP 服务器
    
    环境变量配置：
    - XCSC_TUSHARE_TOKEN: XCSC Tushare API Token（必填）
    - XCSC_TUSHARE_SERVER: 服务器地址（默认 http://tushare.xcsc.com:7172）
    - XCSC_ENV: 环境配置（默认 prd）
    - MCP_HOST: 监听地址（默认 0.0.0.0）
    - MCP_PORT: 监听端口（默认 8000）
    - MCP_PATH: 服务路径（默认 /mcp）
    - MCP_API_KEY: API 认证密钥（可选，默认自动生成）
    - MCP_AUTH_ENABLED: 是否启用认证（默认 true）
    """
    # 验证配置
    error = config.validate()
    if error:
        logger.warning(f"配置警告: {error}")

    # 打印启动信息
    logger.info(f"正在启动 {config.MCP_NAME}...")
    logger.info(f"环境: {config.XCSC_ENV}")
    logger.info(f"服务器地址: {config.XCSC_TUSHARE_SERVER}")
    logger.info(f"监听地址: http://{config.MCP_HOST}:{config.MCP_PORT}{config.MCP_PATH}")
    logger.info(f"认证状态: {'已启用' if config.MCP_AUTH_ENABLED else '已禁用'}")

    if config.MCP_AUTH_ENABLED:
        logger.info(f"API Key: {config.MCP_API_KEY[:8]}...")

    # 启动 MCP HTTP 服务器
    mcp.run(
        transport="http",
        host=config.MCP_HOST,
        port=config.MCP_PORT,
        path=config.MCP_PATH,
    )


if __name__ == "__main__":
    main()
