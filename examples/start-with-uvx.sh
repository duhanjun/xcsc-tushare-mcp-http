#!/bin/bash

# XCSC Tushare MCP 服务器启动脚本（使用 UVX）
# 支持两种模式：stdio（默认）和 http
# 使用方法:
#   - stdio 模式: XCSC_TUSHARE_TOKEN='your_token' ./start-with-uvx.sh
#   - HTTP 模式: XCSC_TUSHARE_TOKEN='your_token' MCP_TRANSPORT=http ./start-with-uvx.sh

# 设置默认值
: ${XCSC_TUSHARE_TOKEN:=""}
: ${MCP_TRANSPORT:="stdio"}
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
echo "  传输方式: ${MCP_TRANSPORT}"

if [ "$MCP_TRANSPORT" = "http" ]; then
    echo "  服务地址: http://${MCP_HOST}:${MCP_PORT}/mcp"
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
else
    echo ""
    echo "MCP 客户端配置:"
    cat <<EOF
{
  "mcpServers": {
    "xcsc-tushare": {
      "command": "uvx",
      "args": [
        "xcsc-tushare-mcp-http"
      ],
      "env": {
        "XCSC_TUSHARE_TOKEN": "${XCSC_TUSHARE_TOKEN}"
      }
    }
  }
}
EOF
    echo ""
    echo "提示: stdio 模式不需要单独启动服务器，直接配置 MCP 客户端即可！"
    echo "      本脚本主要用于 HTTP 模式。"
    echo ""
    read -p "是否继续在 stdio 模式下运行测试？(y/n): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "已取消。"
        exit 0
    fi
fi

echo ""
echo "=========================================="
echo "  正在启动服务器..."
echo "=========================================="
echo ""

# 使用 UVX 启动服务器
XCSC_TUSHARE_TOKEN="${XCSC_TUSHARE_TOKEN}" \
MCP_TRANSPORT="${MCP_TRANSPORT}" \
MCP_API_KEY="${MCP_API_KEY}" \
MCP_AUTH_ENABLED="${MCP_AUTH_ENABLED}" \
MCP_HOST="${MCP_HOST}" \
MCP_PORT="${MCP_PORT}" \
uvx xcsc-tushare-mcp-http
