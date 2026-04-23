"""
命令行入口模块

该模块支持通过 `python -m xcsc_tushare_mcp_http` 方式启动服务器。

支持两种传输方式：
1. stdio（默认）：通过标准输入输出通信，推荐用于 MCP 客户端直接调用
2. http：通过 HTTP 协议通信，需要单独启动服务器

启动方式：
    $ python -m xcsc_tushare_mcp_http

或安装后直接运行：
    $ xcsc-tushare-mcp-http

使用 HTTP 模式：
    $ MCP_TRANSPORT=http python -m xcsc_tushare_mcp_http

启动前请确保已设置 XCSC_TUSHARE_TOKEN 环境变量。
"""

from .server import main


if __name__ == "__main__":
    main()
