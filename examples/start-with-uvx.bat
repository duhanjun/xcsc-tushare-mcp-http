@echo off
REM XCSC Tushare MCP 服务器启动脚本（使用 UVX，Windows 版本）
REM 支持两种模式：stdio（默认）和 http
REM 使用方法:
REM   - stdio 模式: set XCSC_TUSHARE_TOKEN=your_token ^&^& start-with-uvx.bat
REM   - HTTP 模式: set XCSC_TUSHARE_TOKEN=your_token ^&^& set MCP_TRANSPORT=http ^&^& start-with-uvx.bat

REM 设置默认值
if "%XCSC_TUSHARE_TOKEN%"=="" (
    set "XCSC_TUSHARE_TOKEN="
)
if "%MCP_TRANSPORT%"=="" (
    set "MCP_TRANSPORT=stdio"
)
if "%MCP_API_KEY%"=="" (
    REM 生成随机 API Key（简单版本）
    for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /value') do set datetime=%%I
    set "MCP_API_KEY=%datetime:~0,16%"
)
if "%MCP_AUTH_ENABLED%"=="" set "MCP_AUTH_ENABLED=true"
if "%MCP_HOST%"=="" set "MCP_HOST=0.0.0.0"
if "%MCP_PORT%"=="" set "MCP_PORT=8000"

REM 检查是否设置了 XCSC_TUSHARE_TOKEN
if "%XCSC_TUSHARE_TOKEN%"=="" (
    echo 错误: 请设置 XCSC_TUSHARE_TOKEN 环境变量
    echo 使用方法: set XCSC_TUSHARE_TOKEN=your_token ^&^& start-with-uvx.bat
    exit /b 1
)

REM 显示启动信息
echo ==========================================
echo   XCSC Tushare MCP 服务器
echo ==========================================
echo.
echo 配置信息:
echo   传输方式: %MCP_TRANSPORT%

if "%MCP_TRANSPORT%"=="http" (
    echo   服务地址: http://%MCP_HOST%:%MCP_PORT%/mcp
    echo   认证状态: %MCP_AUTH_ENABLED%
    if "%MCP_AUTH_ENABLED%"=="true" (
        echo   API Key: %MCP_API_KEY:~0,8%...%MCP_API_KEY:~-4%
    )
    echo.
    echo MCP 客户端配置:
    echo {
    echo   "mcpServers": {
    echo     "xcsc-tushare": {
    echo       "url": "http://localhost:%MCP_PORT%/mcp",
    echo       "headers": {
    echo         "Authorization": "Bearer %MCP_API_KEY%"
    echo       }
    echo     }
    echo   }
    echo }
) else (
    echo.
    echo MCP 客户端配置:
    echo {
    echo   "mcpServers": {
    echo     "xcsc-tushare": {
    echo       "command": "uvx",
    echo       "args": [
    echo         "xcsc-tushare-mcp-http"
    echo       ],
    echo       "env": {
    echo         "XCSC_TUSHARE_TOKEN": "%XCSC_TUSHARE_TOKEN%"
    echo       }
    echo     }
    echo   }
    echo }
    echo.
    echo 提示: stdio 模式不需要单独启动服务器，直接配置 MCP 客户端即可！
    echo       本脚本主要用于 HTTP 模式。
    echo.
    set /p CONTINUE="是否继续在 stdio 模式下运行测试？(y/n): 
    if /i not "%CONTINUE%"=="y" (
        echo 已取消。
        exit /b 0
    )
)

echo.
echo ==========================================
echo   正在启动服务器...
echo ==========================================
echo.

REM 使用 UVX 启动服务器
set "XCSC_TUSHARE_TOKEN=%XCSC_TUSHARE_TOKEN%
set "MCP_TRANSPORT=%MCP_TRANSPORT%
set "MCP_API_KEY=%MCP_API_KEY%
set "MCP_AUTH_ENABLED=%MCP_AUTH_ENABLED%
set "MCP_HOST=%MCP_HOST%
set "MCP_PORT=%MCP_PORT%
uvx xcsc-tushare-mcp-http
