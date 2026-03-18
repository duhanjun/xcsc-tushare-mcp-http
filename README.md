# xcsc-tushare-mcp-http

基于 [XCSC Tushare](http://tushare.xcsc.com:7173/document/1) 的 MCP 服务器，提供 HTTP 传输协议支持，让 AI 助手能够通过 MCP 协议获取湘财证券金融数据。

## 项目简介

xcsc-tushare-mcp-http 是一个基于 FastMCP 框架开发的 MCP（Model Context Protocol）服务器，通过 HTTP 协议为 AI 助手提供湘财证券 Tushare 金融数据接口。该项目支持多种金融数据的查询，包括沪深股票、指数、公募基金、共同基金、期货、期权、债券等。

## 特性

- 🚀 **HTTP 传输协议** - 支持 streamable-http 传输，适合远程部署
- 🔐 **API Key 认证** - 支持 Bearer Token 认证，保护 API 安全
- 📊 **丰富的数据类型** - 覆盖沪深股票、指数、公募基金、共同基金、期货、期权、债券等
- 🔧 **模块化设计** - 清晰的代码结构，按数据类型分离模块
- 🛠️ **通用查询接口** - 通过 `xcsc_query` 工具可调用任意 XCSC Tushare API
- 📚 **完整的接口文档** - 内置 API 列表和文档查询工具

## 项目结构

```
xcsc-tushare-mcp-http/
├── xcsc_tushare_mcp_http/      # 主包目录
│   ├── __init__.py            # 包初始化文件
│   ├── __main__.py            # 命令行入口
│   ├── server.py              # 服务器主模块
│   ├── auth.py                # 认证中间件模块
│   ├── config.py              # 配置管理模块
│   ├── py.typed               # 类型提示标记文件
│   └── tools/                 # 工具模块目录
│       ├── __init__.py        # 工具模块初始化
│       ├── base.py            # 基础工具（格式化函数）
│       ├── common.py          # 通用工具
│       ├── stock.py           # 股票基础数据工具
│       ├── stock_quote.py     # 股票行情数据工具
│       ├── stock_finance.py   # 股票财务数据工具
│       ├── stock_market.py    # 股票市场参考数据工具
│       ├── index.py           # 指数工具
│       ├── fund.py            # 公募基金工具
│       ├── mutual_fund.py     # 共同基金工具
│       ├── futures.py         # 期货工具
│       ├── option.py          # 期权工具
│       └── bond.py            # 债券工具
├── pyproject.toml             # 项目配置文件
├── requirements.txt           # 依赖列表
└── README.md                  # 项目文档
```

## 安装

### 通过 pip 安装

**Linux/macOS/Windows PowerShell/Windows CMD:**
```bash
pip install xcsc-tushare-mcp-http
```

### 从源码安装

**Linux/macOS/Windows PowerShell/Windows CMD:**
```bash
git clone https://github.com/duhanjun/xcsc-tushare-mcp-http.git
cd xcsc-tushare-mcp-http
pip install -e .
```

## 配置

### 1. 获取 XCSC Tushare Token

到[湘财证券](https://www.xcsc.com/)开户，找客户经理开通 XCSC Tushare 服务，获取 API token。

### 2. 配置环境变量

```bash
# Linux/macOS
export XCSC_TUSHARE_TOKEN="your_token_here"
export XCSC_TUSHARE_SERVER="http://tushare.xcsc.com:7172"

# Windows PowerShell
$env:XCSC_TUSHARE_TOKEN = "your_token_here"
$env:XCSC_TUSHARE_SERVER = "http://tushare.xcsc.com:7172"

# Windows CMD
set XCSC_TUSHARE_TOKEN=your_token_here
set XCSC_TUSHARE_SERVER=http://tushare.xcsc.com:7172
```

### 3. 认证配置（可选）

服务器默认启用 API Key 认证，未自定义 API Key 时，启动时会自动生成一个随机 API Key。

**自定义 API Key（推荐）:**

**Linux/macOS:**
```bash
export MCP_API_KEY="your_secure_api_key_here"
```

**Windows PowerShell:**
```powershell
$env:MCP_API_KEY = "your_api_key_here"
```

**Windows CMD:**
```cmd
set MCP_API_KEY=your_api_key_here
```

**禁用认证（不推荐，仅限内网测试）:**

**Linux/macOS:**
```bash
export MCP_AUTH_ENABLED=false
```

**Windows PowerShell:**
```powershell
$env:MCP_AUTH_ENABLED = "false"
```

**Windows CMD:**
```cmd
set MCP_AUTH_ENABLED=false
```

### 4. 其他配置（可选）

**Linux/macOS:**
```bash
export MCP_HOST=0.0.0.0           # 服务地址，默认 0.0.0.0
export MCP_PORT=8000              # 服务端口，默认 8000
export MCP_PATH=/mcp              # 服务路径，默认 /mcp
export XCSC_ENV=prd               # 环境配置，默认 prd
```

**Windows PowerShell:**
```powershell
$env:MCP_HOST = "0.0.0.0"         # 服务地址，默认 0.0.0.0
$env:MCP_PORT = "8000"            # 服务端口，默认 8000
$env:MCP_PATH = "/mcp"            # 服务路径，默认 /mcp
$env:XCSC_ENV = "prd"             # 环境配置，默认 prd
```

**Windows CMD:**
```cmd
set MCP_HOST=0.0.0.0              # 服务地址，默认 0.0.0.0
set MCP_PORT=8000                 # 服务端口，默认 8000
set MCP_PATH=/mcp                 # 服务路径，默认 /mcp
set XCSC_ENV=prd                  # 环境配置，默认 prd
```

## 使用方法

### 启动服务器

**Linux/macOS:**
```bash
xcsc-tushare-mcp-http
```

**Windows PowerShell:**
```powershell
xcsc-tushare-mcp-http
```

**Windows CMD:**
```cmd
xcsc-tushare-mcp-http
```

启动后会显示：

```
正在启动 xcsc-tushare-mcp-http...
XCSC Tushare Token: your_toke***
环境: prd
服务器地址: http://0.0.0.0:8000/mcp
认证: 已启用
API Key: xxxxxxxx...xxxx
```

> ⚠️ **重要**：请妥善保管启动时显示的 API Key，客户端连接时需要使用。

### MCP 客户端配置

将以下配置添加到您的 MCP 客户端：

**带认证的配置（推荐）**：

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

**无认证的配置**（需设置 `MCP_AUTH_ENABLED=false`）：

```json
{
  "mcpServers": {
    "xcsc-tushare": {
      "url": "http://localhost:8000/mcp"
    }
  }
}
```

## 可用工具

### 通用工具

| 工具名               | 描述                       |
| ----------------- | ------------------------ |
| `xcsc_query`      | 通用 XCSC Tushare API 查询接口 |
| `get_api_list`    | 获取支持的 API 接口列表           |
| `get_api_doc`     | 获取指定 API 的文档说明           |
| `test_connection` | 测试 XCSC Tushare API 连接状态 |

### 股票基础数据工具

| 工具名                       | 描述          |
| ------------------------- | ----------- |
| `get_stock_basic`         | 获取中国A股基本资料  |
| `get_name_change`         | 获取中国A股证券曾用名 |
| `get_stock_company`       | 获取中国A股公司简介  |
| `get_stk_managers`        | 获取上市公司管理层   |
| `get_stk_managers_salary` | 获取管理层薪酬和持股  |
| `get_trade_calendar`      | 获取各大交易所交易日历 |

### 股票行情数据工具

| 工具名                    | 描述            |
| ---------------------- | ------------- |
| `get_daily_quote`      | 获取中国A股日行情     |
| `get_weekly_quote`     | 获取A股周线行情      |
| `get_monthly_quote`    | 获取A股月线行情      |
| `get_min_quote`        | 获取分钟数据        |
| `get_daily_basic`      | 获取每日指标（基本面指标） |
| `get_suspend_info`     | 获取A股停复牌信息     |
| `get_stk_limit`        | 获取每日涨跌停价格     |
| `get_adj_factor`       | 获取股票复权因子      |
| `get_limit_list`       | 获取涨跌停和炸板数据    |
| `get_moneyflow`        | 获取个股资金流向      |
| `get_ggt_top10`        | 获取港股通十大成交股    |
| `get_ggt_daily`        | 获取港股通(沪)每日成交  |
| `get_ggt_daily_stat`   | 获取港股通每日成交统计   |
| `get_ggt_monthly_stat` | 获取港股通每月成交统计   |
| `get_hk_hold`          | 获取沪深港股通持股明细   |
| `get_ggt_moneyflow`    | 获取沪深港通资金流向    |
| `get_sggt_top10`       | 获取沪深股通十大成交股   |

### 股票财务数据工具

| 工具名                  | 描述       |
| -------------------- | -------- |
| `get_income`         | 获取利润表    |
| `get_balancesheet`   | 获取资产负债表  |
| `get_cashflow`       | 获取现金流量表  |
| `get_fina_indicator` | 获取重要财务指标 |
| `get_forecast`       | 获取业绩预告   |
| `get_express`        | 获取业绩快报   |
| `get_dividend`       | 获取分红送股   |
| `get_fina_mainbz`    | 获取主营业务构成 |
| `get_fina_audit`     | 获取财务审计意见 |
| `get_report_rcd`     | 获取财报披露计划 |

### 股票市场参考数据工具

| 工具名                      | 描述         |
| ------------------------ | ---------- |
| `get_top10_holders`      | 获取前十大股东    |
| `get_top10_floatholders` | 获取前十大流通股东  |
| `get_stk_holdernumber`   | 获取股东人数     |
| `get_stk_sharechange`    | 获取股东增减持    |
| `get_share_float`        | 获取股权质押明细数据 |
| `get_share_float_stat`   | 获取股权质押统计数据 |
| `get_repurchase`         | 获取股票回购     |
| `get_block_trade`        | 获取大宗交易     |
| `get_concept`            | 获取概念股分类表   |
| `get_concept_detail`     | 获取概念股明细列表  |
| `get_margin_detail`      | 获取融资融券交易明细 |
| `get_margin`             | 获取融资融券交易汇总 |
| `get_top_list`           | 获取龙虎榜每日明细  |
| `get_top_inst`           | 获取龙虎榜机构明细  |
| `get_stk_account`        | 获取股票开户数据   |

### 指数工具

| 工具名                    | 描述           |
| ---------------------- | ------------ |
| `get_index_daily`      | 获取A股指数日行情    |
| `get_index_weekly`     | 获取指数周线行情     |
| `get_index_monthly`    | 获取指数月线行情     |
| `get_index_weight`     | 获取指数成分和权重    |
| `get_index_basic`      | 获取A股指数成份股    |
| `get_index_dailybasic` | 获取大盘指数每日指标   |
| `get_daily_info`       | 获取市场每日交易统计   |
| `get_sz_daily_info`    | 获取深圳市场每日交易概况 |

### 公募基金工具

| 工具名                  | 描述      |
| -------------------- | ------- |
| `get_fund_basic`     | 获取基金列表  |
| `get_fund_nav`       | 获取基金净值  |
| `get_fund_daily`     | 获取基金行情  |
| `get_fund_div`       | 获取基金分红  |
| `get_fund_portfolio` | 获取基金持仓  |
| `get_fund_manager`   | 获取基金经理  |
| `get_fund_company`   | 获取基金管理人 |
| `get_fund_share`     | 获取基金规模  |

### 共同基金工具

| 工具名                          | 描述                |
| ---------------------------- | ----------------- |
| `get_fund_description`       | 获取中国共同基金基本资料      |
| `get_mf_nav`                 | 获取中国共同基金净值        |
| `get_mf_manager`             | 获取中国共同基金基金经理      |
| `get_mf_benchmark`           | 获取中国共同基金业绩比较基准行情  |
| `get_mf_stock_portfolio`     | 获取中国共同基金投资组合-持股明细 |
| `get_mf_bond_portfolio`      | 获取中国共同基金投资组合-持券明细 |
| `get_mf_asset_allocation`    | 获取中国共同基金投资组合-资产配置 |
| `get_mf_industry_allocation` | 获取中国共同基金投资组合-行业配置 |
| `get_mf_other_portfolio`     | 获取中国共同基金投资组合-其他证券 |
| `get_mf_wind_classify`       | 获取中国Wind基金分类      |

### 期货工具

| 工具名               | 描述          |
| ----------------- | ----------- |
| `get_fut_basic`   | 获取期货合约信息    |
| `get_fut_daily`   | 获取期货日线行情    |
| `get_fut_holding` | 获取每日持仓排名    |
| `get_fut_settle`  | 获取每日结算参数    |
| `get_fut_mapping` | 获取期货主力与连续合约 |
| `get_fut_wsr`     | 获取仓单日报      |

### 期权工具

| 工具名             | 描述       |
| --------------- | -------- |
| `get_opt_basic` | 获取期权合约信息 |
| `get_opt_daily` | 获取期权日线行情 |

### 债券工具

| 工具名                 | 描述                |
| ------------------- | ----------------- |
| `get_cb_basic`      | 获取可转债基本信息         |
| `get_cb_daily`      | 获取可转债行情           |
| `get_cb_issue`      | 获取可转债发行           |
| `get_cb_call`       | 获取可转债有条件赎回价格和触发比例 |
| `get_cb_put`        | 获取可转债有条件回售价格和触发比例 |
| `get_cb_force_call` | 获取可转债强制赎回信息       |
| `get_bond_basic`    | 获取中国债券基本资料        |

## 交互示例

安装并配置后，您可以通过 MCP 客户端用自然语言与 AI 助手交互：

**获取股票数据**：

```
获取平安银行最近 30 天的股价数据
```

**财务分析**：

```
查看招商银行最近的财务报表，分析营收和净利润
```

**指数数据**：

```
获取上证指数最近的行情数据
```

**基金数据**：

```
查询某只基金的净值和持仓情况
```

**通用查询**：

```
使用 xcsc_query 查询期货合约信息
```

## 参数格式说明

- **日期格式**：YYYYMMDD（如 20241231）
- **股票代码**：ts\_code 格式（如 000001.SZ, 600000.SH）
- **返回格式**：JSON 格式，包含 success、data、count、columns 字段

## 开发指南

### 本地开发

```bash
# 克隆项目
git clone https://github.com/duhanjun/xcsc-tushare-mcp-http.git
cd xcsc-tushare-mcp-http

# 安装开发依赖
pip install -e ".[dev]"

# 运行服务
python -m xcsc_tushare_mcp_http.server
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

## 环境变量

| 变量名                   | 描述                     | 默认值                            |
| --------------------- | ---------------------- | ------------------------------ |
| `XCSC_TUSHARE_TOKEN`  | XCSC Tushare API token | 必填                             |
| `XCSC_TUSHARE_SERVER` | XCSC Tushare 服务器地址     | `http://tushare.xcsc.com:7172` |
| `XCSC_ENV`            | 环境配置（prd/dev）          | `prd`                          |
| `MCP_HOST`            | 服务器监听地址                | `0.0.0.0`                      |
| `MCP_PORT`            | 服务器监听端口                | `8000`                         |
| `MCP_PATH`            | MCP 服务路径               | `/mcp`                         |
| `MCP_NAME`            | 服务名称                   | `xcsc-tushare-mcp-http`        |
| `MCP_API_KEY`         | API 认证密钥               | 自动生成 32 位随机密钥或默认值 `xiaodudu`   |
| `MCP_AUTH_ENABLED`    | 是否启用认证（true/false）     | `true`                         |

## 相关链接

- [XCSC Tushare 官网](http://tushare.xcsc.com:7173/document/1)
- [XCSC Tushare API 文档](http://tushare.xcsc.com:7173/document/2)
- [MCP 协议文档](https://modelcontextprotocol.io/)
- [FastMCP 框架](https://github.com/jlowin/fastmcp)

## 许可证

MIT License

## 注意事项

- 本项目仅供学习和研究使用
- API 调用有频率限制，请合理使用
- 数据来源于 XCSC Tushare，请勿用于商业用途

