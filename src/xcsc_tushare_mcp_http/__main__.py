"""
命令行入口模块

该模块支持通过 `python -m xcsc_tushare_mcp_http` 方式启动服务器。

启动方式：
    $ python -m xcsc_tushare_mcp_http

或安装后直接运行：
    $ xcsc-tushare-mcp-http

启动前请确保已设置 XCSC_TUSHARE_TOKEN 环境变量。
"""

from .server import main


if __name__ == "__main__":
    main()
