#!/bin/bash

# XCSC Tushare MCP 服务器启动脚本（使用 UVX）
# 使用方法：./start-with-uvx.sh

# 设置默认值
: ${XCSC_TUSHARE_TOKEN:=""}
: ${MCP_API_KEY:="$(openssl rand -hex 16)"}
: ${MCP_AUTH_ENABLED:="true"}
: ${MCP_HOST:="0.0.0.0"}
: ${MCP_PORT:="8000"}

# 检查是否设置了 XCSC_TUSHARE_TOKEN
if [ -z "$XCSC_TUSHARE_TOKEN" ]; then
    echo "错误: 请设置 XCSC_TUSHARE_TOKEN 环境变量"
    echo "使用方法: XCSC_TUSHARE_TOKEN='your_token' ./start-with-uvx.sh"
    exit 1
fi

# 显示启动信息
echo "=========================================="
echo "  XCSC Tushare MCP 服务器"
echo "=========================================="
echo ""
echo "配置信息:"
echo "  服务器地址: http://${MCP_HOST}:${MCP_PORT}/mcp"
echo "  认证状态: ${MCP_AUTH_ENABLED}"
if [ "$MCP_AUTH_ENABLED" = "true" ]; then
    echo "  API Key: ${MCP_API_KEY:0:8}...${MCP_API_KEY: -4}"
fi
echo ""
echo "MCP 客户端配置:"
cat <<EOF
{
  "mcpServers": {
    "xcsc-tushare": {
      "url": "http://localhost:${MCP_PORT}/mcp",
      "headers": {
        "Authorization": "Bearer ${MCP_API_KEY}"
      }
    }
  }
}
EOF
echo ""
echo "=========================================="
echo "  正在启动服务器..."
echo "=========================================="
echo ""

# 使用 UVX 启动服务器
XCSC_TUSHARE_TOKEN="${XCSC_TUSHARE_TOKEN}" \
MCP_API_KEY="${MCP_API_KEY}" \
MCP_AUTH_ENABLED="${MCP_AUTH_ENABLED}" \
MCP_HOST="${MCP_HOST}" \
MCP_PORT="${MCP_PORT}" \
uvx xcsc-tushare-mcp-http
