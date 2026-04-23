# 通过 UVX 使用 XCSC Tushare MCP 服务器

## 概述

由于本项目使用 **HTTP 传输**，配置流程分为两步：
1. 通过 UVX 启动 MCP 服务器
2. 在 MCP 客户端中配置 HTTP 连接

## 第一步：启动服务器

### 方式 1：使用提供的启动脚本（推荐）

#### macOS / Linux

```bash
# 1. 设置您的 XCSC Tushare Token
export XCSC_TUSHARE_TOKEN="your_token_here"

# 2. 使用启动脚本
cd /workspace/examples
chmod +x start-with-uvx.sh
./start-with-uvx.sh
```

#### Windows

```cmd
# 1. 设置您的 XCSC Tushare Token
set XCSC_TUSHARE_TOKEN=your_token_here

# 2. 使用启动脚本
cd \workspace\examples
start-with-uvx.bat
```

### 方式 2：手动启动

```bash
# 设置必要的环境变量
export XCSC_TUSHARE_TOKEN="your_token_here"
export MCP_API_KEY="your_custom_api_key"  # 可选，不设置会自动生成

# 使用 UVX 启动服务器
uvx xcsc-tushare-mcp-http
```

## 第二步：配置 MCP 客户端

### 基础配置

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

### 各平台配置位置

#### Claude Desktop

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

#### Cursor / Windsurf

在设置中找到 MCP 配置部分，添加相同的 HTTP 配置。

## 完整示例

### 1. 启动服务器（终端 1）

```bash
export XCSC_TUSHARE_TOKEN="your_actual_token"
export MCP_API_KEY="my_secure_api_key_123"
uvx xcsc-tushare-mcp-http
```

您会看到类似输出：
```
正在启动 xcsc-tushare-mcp-http...
版本: 1.0.2
XCSC Tushare Token: your_actua***
运行环境: prd
服务地址: http://0.0.0.0:8000/mcp
认证状态: 已启用
API Key: my_secu...key_123
```

### 2. 配置客户端

编辑您的 MCP 配置文件：

```json
{
  "mcpServers": {
    "xcsc-tushare": {
      "url": "http://localhost:8000/mcp",
      "headers": {
        "Authorization": "Bearer my_secure_api_key_123"
      }
    }
  }
}
```

### 3. 重启 MCP 客户端

重启您的 AI 助手客户端（如 Claude Desktop）以加载新配置。

## 环境变量说明

| 环境变量 | 说明 | 默认值 |
|---------|------|--------|
| `XCSC_TUSHARE_TOKEN` | XCSC Tushare API Token | 无（必填） |
| `MCP_API_KEY` | API 认证密钥 | 自动生成 |
| `MCP_AUTH_ENABLED` | 是否启用认证 | `true` |
| `MCP_HOST` | 服务器监听地址 | `0.0.0.0` |
| `MCP_PORT` | 服务器监听端口 | `8000` |
| `MCP_PATH` | MCP 服务路径 | `/mcp` |

## 禁用认证（仅用于测试）

如果您想在本地测试时禁用认证：

```bash
export XCSC_TUSHARE_TOKEN="your_token"
export MCP_AUTH_ENABLED="false"
uvx xcsc-tushare-mcp-http
```

此时客户端配置可以简化为：

```json
{
  "mcpServers": {
    "xcsc-tushare": {
      "url": "http://localhost:8000/mcp"
    }
  }
}
```

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

## 故障排查

### 问题 1：连接被拒绝

**原因**：服务器未启动或端口被占用

**解决**：
- 确认服务器正在运行
- 检查端口 8000 是否被其他程序占用
- 尝试更改端口：`export MCP_PORT=8080`

### 问题 2：认证失败

**原因**：API Key 不匹配

**解决**：
- 确认服务器启动时显示的 API Key
- 在客户端配置中使用完全相同的 API Key
- 或者禁用认证进行测试

### 问题 3：XCSC Tushare Token 错误

**原因**：Token 无效或未设置

**解决**：
- 确认已正确设置 `XCSC_TUSHARE_TOKEN`
- 检查 Token 是否有效
- 确认您有访问 XCSC Tushare 的权限

## 文件说明

在 `examples/` 目录下提供了以下文件：

- `mcp-config.json` - MCP 客户端配置模板
- `start-with-uvx.sh` - macOS/Linux 启动脚本
- `start-with-uvx.bat` - Windows 启动脚本
- `UVX_SETUP_GUIDE.md` - 本使用指南

## 快速开始（3 步）

1. **设置 Token 并启动**
   ```bash
   export XCSC_TUSHARE_TOKEN="your_token"
   cd /workspace/examples
   ./start-with-uvx.sh
   ```

2. **复制显示的配置**
   启动脚本会自动显示完整的 MCP 配置

3. **粘贴到客户端配置**
   将配置复制到您的 MCP 客户端配置文件中

就这么简单！
