# 通过 UVX 使用 XCSC Tushare MCP 服务器

## 概述

本项目支持 **两种传输方式**：

1. **stdio 模式（默认，推荐）**：通过标准输入输出进行通信，配置最简单
2. **HTTP 模式**：通过 HTTP 协议进行通信，适合远程部署

---

## 方式一：使用 stdio 模式（推荐，最简单）

这是最简单的方式，无需单独启动服务器，直接在 MCP 客户端配置中使用即可。

### 1. 配置 MCP 客户端

直接在您的 MCP 客户端配置文件中添加：

```json
{
  "mcpServers": {
    "xcsc-tushare": {
      "command": "uvx",
      "args": [
        "xcsc-tushare-mcp-http"
      ],
      "env": {
        "XCSC_TUSHARE_TOKEN": "your_token_here"
      }
    }
  }
}
```

或者如果已经安装了包：

```json
{
  "mcpServers": {
    "xcsc-tushare": {
      "command": "xcsc-tushare-mcp-http",
      "env": {
        "XCSC_TUSHARE_TOKEN": "your_token_here"
      }
    }
  }
}
```

### 2. 重启 MCP 客户端

重启您的 AI 助手客户端（如 Claude Desktop）即可使用。

---

## 方式二：使用 HTTP 模式

如果需要远程部署或多个客户端共享，可以使用 HTTP 模式。

### 1. 启动服务器

#### macOS / Linux

```bash
# 设置您的 XCSC Tushare Token
export XCSC_TUSHARE_TOKEN="your_token_here"
export MCP_TRANSPORT=http

# 使用启动脚本
cd /workspace/examples
chmod +x start-with-uvx.sh
./start-with-uvx.sh
```

#### Windows

```cmd
# 设置您的 XCSC Tushare Token
set XCSC_TUSHARE_TOKEN=your_token_here
set MCP_TRANSPORT=http

# 使用启动脚本
cd \workspace\examples
start-with-uvx.bat
```

### 2. 配置 MCP 客户端

在您的 MCP 客户端配置文件中添加：

```json
{
  "mcpServers": {
    "xcsc-tushare": {
      "url": "http://localhost:8000/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_API_KEY_HERE"
      }
    }
  }
}
```

### 3. 重启 MCP 客户端

重启您的 AI 助手客户端以加载新配置。

---

## 各平台配置文件位置

### Claude Desktop

**macOS**:
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Windows**:
```
%APPDATA%\Claude\claude_desktop_config.json
```

**Linux**:
```
~/.config/Claude/claude_desktop_config.json
```

### Cursor / Windsurf

在设置中找到 MCP 配置部分添加配置。

---

## 完整示例

### stdio 模式完整配置

```json
{
  "mcpServers": {
    "xcsc-tushare": {
      "command": "uvx",
      "args": [
        "xcsc-tushare-mcp-http"
      ],
      "env": {
        "XCSC_TUSHARE_TOKEN": "your_actual_token_here",
        "XCSC_TUSHARE_SERVER": "http://tushare.xcsc.com:7172",
        "MCP_LOG_LEVEL": "INFO"
      }
    }
  }
}
```

---

## 环境变量说明

| 环境变量 | 描述 | 默认值 |
|---------|------|--------|
| `XCSC_TUSHARE_TOKEN` | XCSC Tushare API Token | 无（必填） |
| `XCSC_TUSHARE_SERVER` | XCSC Tushare 服务器地址 | `http://tushare.xcsc.com:7172` |
| `XCSC_ENV` | 运行环境 | `prd` |
| `MCP_TRANSPORT` | 传输方式，`stdio` 或 `http` | `stdio` |
| `MCP_HOST` | 服务器监听地址（仅 HTTP） | `0.0.0.0` |
| `MCP_PORT` | 服务器监听端口（仅 HTTP） | `8000` |
| `MCP_PATH` | MCP 服务路径（仅 HTTP） | `/mcp` |
| `MCP_API_KEY` | API 认证密钥（仅 HTTP） | 自动生成 |
| `MCP_AUTH_ENABLED` | 是否启用认证（仅 HTTP） | `true` |
| `MCP_LOG_LEVEL` | 日志级别 | `INFO` |

---

## 验证配置

配置完成后，您可以在 AI 助手中尝试：

1. **查看可用 API**
   ```
   有哪些金融数据可以查询？
   ```

2. **查询股票数据**
   ```
   获取平安银行的基本信息
   ```

3. **获取行情数据**
   ```
   查询上证指数最近的行情数据
   ```

---

## 提供的示例文件

在 `examples/` 目录下提供了以下文件：

- `mcp-config-stdio.json` - stdio 模式配置模板（使用 UVX）
- `mcp-config-stdio-local.json` - stdio 模式配置模板（使用已安装的包）
- `mcp-config.json` - HTTP 模式配置模板
- `start-with-uvx.sh` - macOS/Linux 启动脚本（支持两种模式）
- `start-with-uvx.bat` - Windows 启动脚本（支持两种模式）
- `UVX_SETUP_GUIDE.md` - 本使用指南

---

## 快速开始（推荐 stdio 模式）

### 最简单的方式（3 步）：

1. **编辑您的 MCP 客户端配置文件**，添加：
   ```json
   {
     "mcpServers": {
       "xcsc-tushare": {
         "command": "uvx",
         "args": [
           "xcsc-tushare-mcp-http"
         ],
         "env": {
           "XCSC_TUSHARE_TOKEN": "your_token_here"
         }
       }
     }
   }
   ```

2. **替换 `your_token_here`** 为您的实际 Token

3. **重启您的 AI 助手客户端**

就这么简单！

---

## 两种模式对比

| 特性 | stdio 模式（推荐） | HTTP 模式 |
|------|-------------------|----------|
| 配置复杂度 | 简单 | 中等 |
| 是否需要单独启动 | 不需要 | 需要 |
| 适合场景 | 本地使用 | 远程部署、多客户端共享 |
| 认证 | 不需要 | API Key 认证 |
| UVX 支持 | 完美支持 | 支持 |
