# XCSC Tushare MCP HTTP Server Docker Image

FROM python:3.12-slim

WORKDIR /app

# 配置 pip 使用国内镜像源
RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/ && \
    pip config set install.trusted-host mirrors.aliyun.com

# 直接从 PyPI 安装
RUN pip install --no-cache-dir xcsc-tushare-mcp-http

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 暴露服务端口
EXPOSE 8000

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/mcp')" || exit 1

# 启动命令
CMD ["xcsc-tushare-mcp-http"]
