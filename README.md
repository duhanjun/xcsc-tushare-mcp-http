## 项目简介

xcsc-tushare-mcp-http 是一个基于 FastMCP 框架开发的 MCP（Model Context Protocol）服务器，支持 **stdio** 和 **HTTP** 两种传输方式，为 AI 助手提供湘财证券 [Tushare](http://tushare.xcsc.com:7173/document/1) 金融数据接口。

### 主要特性

- 🎯 **两种传输方式** - 支持 stdio（默认，推荐）和 HTTP 两种模式
- 🚀 **HTTP 传输协议** - 支持 streamable-http 传输，适合远程部署
- 🔐 **API Key 认证** - HTTP 模式支持 Bearer Token 认证，保护 API 安全
- 📊 **丰富的数据类型** - 覆盖沪深股票、指数、公募基金、共同基金、期货、期权、债券等
- 🔄 **动态元数据更新** - 自动检测 references/ 目录变化，重新生成 API 元数据
- 🔧 **3 个核心工具** - 简化设计，通过 get_api_list、get_api_doc、get_api_query 完成所有操作
- 📚 **完整的接口文档** - 内置 API 列表和文档查询工具

## 项目结构

```
xcsc-tushare-mcp-http/
├── src/
│   └── xcsc_tushare_mcp_http/      # 主包目录
│       ├── __init__.py            # 包初始化
│       ├── __main__.py            # 命令行入口
│       ├── server.py              # 服务器主模块
│       ├── tools.py               # 3 个核心工具
│       ├── config.py              # 配置管理
│       ├── auth.py                # 认证中间件
│       ├── metadata.py            # 元数据生成和加载
│       ├── api_metadata.json      # 缓存的 API 元数据
│       ├── py.typed               # 类型提示标记
│       └── references/            # API 文档源文件（约 90 个 .md）
│           ├── 债券/
│           ├── 公募基金/
│           ├── 共同基金/
│           ├── 指数/
│           ├── 期权/
│           ├── 期货/
│           └── 沪深股票/
├── pyproject.toml                 # 项目配置
├── requirements.txt               # 依赖列表
└── README.md                      # 项目文档
```

## 安装方法

### 通过 pip 安装

```bash
pip install xcsc-tushare-mcp-http
```

### 下载源码安装

```bash
git clone https://github.com/duhanjun/xcsc-tushare-mcp-http.git
cd xcsc-tushare-mcp-http
pip install -e .
```

## 配置说明

### 1. 获取 XCSC Tushare Token

到[湘财证券](https://www.xcsc.com/)开户，找客户经理开通 XCSC Tushare 服务，获取 API token。

### 2. 配置环境变量

```bash
# Linux/macOS
export XCSC_TUSHARE_TOKEN="your_token_here"

# Windows PowerShell
$env:XCSC_TUSHARE_TOKEN = "your_token_here"

# Windows CMD
set XCSC_TUSHARE_TOKEN=your_token_here
```

### 3. 传输方式配置（可选）

服务器默认使用 **stdio 模式**（推荐），也可以使用 HTTP 模式。

使用 stdio 模式（默认）：

```bash
# 无需额外配置，默认就是 stdio
```

使用 HTTP 模式：

```bash
# Linux/macOS
export MCP_TRANSPORT=http

# Windows PowerShell
$env:MCP_TRANSPORT = "http"

# Windows CMD
set MCP_TRANSPORT=http
```

### 4. HTTP 模式认证配置（仅 HTTP 模式需要）

HTTP 模式默认启用 API Key 认证，未自定义 API Key 时，启动时会自动生成一个随机 API Key。

自定义 API Key（推荐）:

```bash
# Linux/macOS
export MCP_API_KEY="your_api_key_here"

# Windows PowerShell
$env:MCP_API_KEY = "your_api_key_here"

# Windows CMD
set MCP_API_KEY=your_api_key_here
```

禁用认证（不推荐，仅限内网测试）:

```bash
# Linux/macOS
export MCP_AUTH_ENABLED=false

# Windows PowerShell
$env:MCP_AUTH_ENABLED = "false"

# Windows CMD
set MCP_AUTH_ENABLED=false
```

### 5. 其他配置（可选）

| 环境变量 | 描述 | 默认值 |
|---------|------|--------|
| `XCSC_TUSHARE_SERVER` | XCSC Tushare 服务器地址 | `http://tushare.xcsc.com:7172` |
| `XCSC_ENV` | 运行环境 | `prd` |
| `MCP_TRANSPORT` | 传输方式，`stdio` 或 `http` | `stdio` |
| `MCP_HOST` | 服务器监听地址（仅 HTTP） | `0.0.0.0` |
| `MCP_PORT` | 服务器监听端口（仅 HTTP） | `8000` |
| `MCP_PATH` | MCP 服务路径（仅 HTTP） | `/mcp` |
| `MCP_AUTH_ENABLED` | 是否启用认证（仅 HTTP） | `true` |
| `MCP_LOG_LEVEL` | 日志级别 | `INFO` |

## 使用方法

### 方式一：使用 stdio 模式（推荐，最简单）

这是最简单的方式，可以直接在 MCP 客户端配置中使用，无需单独启动服务器。

#### 1. 配置 MCP 客户端：

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

### 方式二：使用 HTTP 模式

如果需要远程部署或多个客户端共享，可以使用 HTTP 模式。

#### 1. 启动服务器：

```bash
# 设置必要的环境变量
export XCSC_TUSHARE_TOKEN="your_token_here"
export MCP_TRANSPORT=http

# 启动服务器
xcsc-tushare-mcp-http
```

启动后会显示：

```
正在启动 xcsc-tushare-mcp-http...
版本: 1.0.2
传输方式: http
XCSC Tushare Token: your_toke***
运行环境: prd
服务地址: http://0.0.0.0:8000/mcp
认证状态: 已启用
API Key: xxxxxxxx...xxxx
```

#### 2. 配置 MCP 客户端：

```json
{
  "mcpServers": {
    "xcsc-tushare": {
      "url": "http://localhost:8000/mcp",
      "headers": {
        "Authorization": "Bearer your_api_key_here"
      }
    }
  }
}
```

## 可用工具

本服务提供 **3 个核心工具**：

### 1. get_api_list()

获取所有可用 API 的简化列表（只包含名称和描述）。

**返回格式：**
```json
{
  "success": true,
  "total_apis": 91,
  "data": {
    "stock_basic": {
      "api_name": "stock_basic",
      "description": "获取中国A股基本资料",
      "category": "沪深股票_基础数据"
    },
    ...
  }
}
```

### 2. get_api_doc(api_name)

获取指定 API 的详细文档（参数、输出字段、示例）。

**参数：**
- `api_name`: API 名称，如 `"stock_basic"`

**返回格式：**
```json
{
  "success": true,
  "data": {
    "api_name": "stock_basic",
    "description": "获取中国A股基本资料",
    "category": "沪深股票_基础数据",
    "limit": "单次最大5000条",
    "permission": "基础权限",
    "input_params": [
      {"name": "ts_code", "type": "str", "required": false, "description": "股票代码"},
      ...
    ],
    "output_params": [
      {"name": "ts_code", "type": "str", "description": "股票代码"},
      ...
    ],
    "example": "get_api_query('stock_basic', '{\"ts_code\": \"000001.SZ\"}')"
  }
}
```

### 3. get_api_query(api_name, params)

通用查询接口，调用底层 XCSC Tushare API。

**参数：**
- `api_name`: API 名称，如 `"stock_basic"`
- `params`: JSON 格式的参数字符串，如 `'{"ts_code": "000001.SZ"}'`

**返回格式：**
```json
{
  "success": true,
  "data": [...],
  "count": 100,
  "columns": ["ts_code", "name", "industry", ...]
}
```

## 使用流程

1. **获取 API 列表**
   ```
   调用 get_api_list() 查看所有可用 API
   ```

2. **获取 API 文档**
   ```
   调用 get_api_doc("stock_basic") 获取参数说明
   ```

3. **执行查询**
   ```
   调用 get_api_query("stock_basic", '{"ts_code": "000001.SZ"}') 获取数据
   ```

## 交互示例

安装并配置后，您可以通过 MCP 客户端用自然语言与 AI 助手交互：

**获取股票数据：**
```
获取平安银行最近 30 天的股价数据
```

**财务分析：**
```
查看招商银行最近的财务报表，分析营收和净利润
```

**指数数据：**
```
获取上证指数最近的行情数据
```

**基金数据：**
```
查询某只基金的净值和持仓情况
```

## 参数格式

- **日期格式**：YYYYMMDD（如 20241231）
- **股票代码**：ts_code 格式（如 000001.SZ, 600000.SH）
- **返回格式**：JSON 格式，包含 success、data、count、columns 字段
- **params 格式**：JSON 字符串，如 `'{"ts_code": "000001.SZ", "trade_date": "20240101"}'`

## 接口更新

项目支持动态更新XCSC Tushare API 接口：

1. 修改 `references/` 目录中的 `.md` 文件
2. 重启服务器
3. 服务器会自动检测变化并重新生成 `api_metadata.json`

这样您可以：
- 添加新的 XCSC Tushare API 文档
- 修改现有 XCSC Tushare API 的描述或参数
- 无需修改代码即可更新 XCSC Tushare API 列表

## 开发指南

### 本地开发

```bash
# 克隆项目
git clone https://github.com/duhanjun/xcsc-tushare-mcp-http.git
cd xcsc-tushare-mcp-http

# 安装开发依赖
pip install -e ".[dev]"

# 运行服务
python -m xcsc_tushare_mcp_http
```

### 打包发布

```bash
# 安装打包工具
pip install build twine

# 打包
python -m build

# 上传到 PyPI
twine upload dist/*
```

## 相关链接

- [XCSC Tushare 官网](http://tushare.xcsc.com:7173/document/1)
- [XCSC Tushare API 文档](http://tushare.xcsc.com:7173/document/2)
- [MCP 协议文档](https://modelcontextprotocol.io/)
- [FastMCP 框架](https://github.com/jlowin/fastmcp)

## 许可证

MIT License

## 注意事项

- 本项目仅供学习和研究使用
- XCSC Tushare API 调用有频率限制，请合理使用
- 数据来源于 XCSC Tushare，请勿用于商业用途
