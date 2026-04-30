# Docker 部署指南

## 概述

本项目支持使用 Docker 容器化部署，方便在各种环境中快速启动 XCSC Tushare MCP 服务器。

Docker 部署主要用于 HTTP 模式，适合远程部署和多客户端共享。

## 文件说明

| 文件 | 说明 |
|------|------|
| `Dockerfile` | Docker 镜像构建文件 |
| `.dockerignore` | Docker 构建忽略文件 |
| `docker-compose.yml` | Docker Compose 配置文件 |

## 快速开始

### 方法一：使用 Docker 命令

#### 1. 构建镜像

```bash
docker build -t xcsc-tushare-mcp:latest .
```

#### 2. 运行容器（HTTP 模式）

```bash
docker run -d \
  --name xcsc-tushare-mcp \
  -p 8000:8000 \
  -e XCSC_TUSHARE_TOKEN="your_token_here" \
  -e MCP_TRANSPORT=http \
  -e XCSC_TUSHARE_TIMEOUT=60 \
  -e MCP_API_KEY="your_api_key" \
  -e MCP_AUTH_ENABLED=true \
  -e MCP_LOG_LEVEL=INFO \
  --restart unless-stopped \
  xcsc-tushare-mcp:latest
```

#### 3. 查看日志

```bash
docker logs -f xcsc-tushare-mcp
```

#### 4. 停止容器

```bash
docker stop xcsc-tushare-mcp
docker rm xcsc-tushare-mcp
```

### 方法二：使用 Docker Compose（推荐）

#### 1. 设置环境变量

创建 `.env` 文件：

```bash
# 必填
XCSC_TUSHARE_TOKEN=your_token_here

# 可选（使用默认值）
# XCSC_TUSHARE_SERVER=http://tushare.xcsc.com:7172
# XCSC_ENV=prd
# XCSC_TUSHARE_TIMEOUT=60
# MCP_HOST=0.0.0.0
# MCP_PORT=8000
# MCP_PATH=/mcp
# MCP_NAME=xcsc-tushare-mcp
# MCP_AUTH_ENABLED=true
# MCP_LOG_LEVEL=INFO
```

#### 2. 启动服务

```bash
# 前台运行
docker-compose up

# 后台运行
docker-compose up -d

# 构建并运行
docker-compose up --build
```

#### 3. 查看日志

```bash
# 查看日志
docker-compose logs

# 实时跟踪日志
docker-compose logs -f

# 查看最近 100 行
docker-compose logs --tail=100
```

#### 4. 停止服务

```bash
docker-compose down
```

#### 5. 重启服务

```bash
docker-compose restart
```

## 环境变量说明

| 变量名 | 必填 | 默认值 | 说明 |
|--------|------|--------|------|
| `XCSC_TUSHARE_TOKEN` | 是 | - | XCSC Tushare API Token |
| `XCSC_TUSHARE_SERVER` | 否 | `http://tushare.xcsc.com:7172` | 服务器地址 |
| `XCSC_ENV` | 否 | `prd` | 运行环境 |
| `XCSC_TUSHARE_TIMEOUT` | 否 | `60` | API 超时时间（秒） |
| `MCP_TRANSPORT` | 否 | `stdio` | 传输方式，`stdio` 或 `http`（Docker 默认 `http`） |
| `MCP_HOST` | 否 | `0.0.0.0` | 监听地址（仅 HTTP 模式） |
| `MCP_PORT` | 否 | `8000` | 监听端口（仅 HTTP 模式） |
| `MCP_PATH` | 否 | `/mcp` | 服务路径（仅 HTTP 模式） |
| `MCP_NAME` | 否 | `xcsc-tushare-mcp` | 服务名称 |
| `MCP_API_KEY` | 否 | 自动生成 | API 认证密钥（仅 HTTP 模式） |
| `MCP_AUTH_ENABLED` | 否 | `true` | 是否启用认证（仅 HTTP 模式） |
| `MCP_LOG_LEVEL` | 否 | `INFO` | 日志级别 |

## 镜像信息

### 基础镜像
- `python:3.12-slim`

### 镜像大小
- 预计约 200-300 MB

### 暴露端口
- `8000` - HTTP 服务端口

### 健康检查
- 每 30 秒检查一次服务健康状态
- 超时时间 10 秒
- 失败 3 次后标记为不健康

## 故障排除

### 容器无法启动

检查日志：
```bash
docker logs xcsc-tushare-mcp
```

常见问题：
1. **Token 未设置**: 确保设置了 `XCSC_TUSHARE_TOKEN`
2. **端口冲突**: 检查 8000 端口是否被占用
3. **内存不足**: 增加 Docker 容器内存限制

### 连接超时

增加超时时间：
```bash
-e XCSC_TUSHARE_TIMEOUT=120
```

### 认证失败

检查 API Key：
```bash
# 查看自动生成的 API Key
docker logs xcsc-tushare-mcp | grep "API Key"
```

## 构建优化

### 多阶段构建（可选）

如果需要更小的镜像，可以使用多阶段构建：

```dockerfile
# 构建阶段
FROM python:3.12-slim as builder
WORKDIR /app
COPY . .
RUN pip install --user -e .

# 运行阶段
FROM python:3.12-slim
COPY --from=builder /root/.local /root/.local
COPY --from=builder /app/src /app/src
ENV PATH=/root/.local/bin:$PATH
ENV MCP_TRANSPORT=http
CMD ["xcsc-tushare-mcp"]
```

## 安全建议

1. **使用自定义 API Key**: 设置 `MCP_API_KEY` 环境变量
2. **限制容器资源**: 使用 Docker Compose 中的资源限制
3. **使用 HTTPS**: 在生产环境中使用反向代理（如 Nginx）启用 HTTPS
4. **定期更新**: 定期拉取最新镜像更新

## 相关链接

- [Docker 官方文档](https://docs.docker.com/)
- [Docker Compose 官方文档](https://docs.docker.com/compose/)
