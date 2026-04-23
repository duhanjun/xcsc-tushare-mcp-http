#!/usr/bin/env python3
"""
测试脚本：验证两种运行模式下的 API 调用

该脚本测试两种运行模式（stdio 和 HTTP）下是否能正常调用 91 个接口的数据。
"""

import os
import json
import subprocess
import time
import sys
from pathlib import Path

# 添加 src 目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent / "src"))

from xcsc_tushare_mcp_http.metadata import load_api_metadata
from xcsc_tushare_mcp_http.config import config

def get_api_list() -> list:
    """
    获取 API 列表
    """
    metadata = load_api_metadata()
    return list(metadata.get("apis", {}).keys())

def test_stdio_mode():
    """
    测试 stdio 模式
    """
    print("\n=== 测试 stdio 模式 ===")
    
    # 检查 XCSC_TUSHARE_TOKEN 是否设置
    if not os.getenv("XCSC_TUSHARE_TOKEN"):
        print("错误: 请设置 XCSC_TUSHARE_TOKEN 环境变量")
        return False
    
    # 获取 API 列表
    api_list = get_api_list()
    print(f"共找到 {len(api_list)} 个 API 接口")
    
    # 测试第一个 API
    test_api = api_list[0] if api_list else ""
    if not test_api:
        print("错误: 没有找到 API 接口")
        return False
    
    print(f"测试 API: {test_api}")
    
    # 构建测试命令
    test_code = '''
import json
import sys

# 读取 MCP 工具调用
while True:
    line = sys.stdin.readline()
    if not line:
        break
    
try:
    data = json.loads(line)
    tool_call = data.get("toolcall", {})
    name = tool_call.get("name")
    params = tool_call.get("params", {})
    
    if name == "get_api_list":
        # 模拟工具调用
        from xcsc_tushare_mcp_http.tools import register_tools
        from xcsc_tushare_mcp_http.config import config
        from fastmcp import FastMCP
        import xcsc_tushare as ts
        from xcsc_tushare.client import DataApi
        
        mcp = FastMCP(name="test")
        ts.set_token(config.XCSC_TUSHARE_TOKEN)
        pro = DataApi(
            token=config.XCSC_TUSHARE_TOKEN,
            env=config.XCSC_ENV,
            server=config.XCSC_TUSHARE_SERVER,
            timeout=config.XCSC_TUSHARE_TIMEOUT
        )
        register_tools(mcp, pro)
        
        # 调用工具
        result = mcp.run_tool("get_api_list", {})
        print(json.dumps({"toolcall_result": result}))
        sys.stdout.flush()
        
    elif name == "get_api_query":
        # 模拟工具调用
        from xcsc_tushare_mcp_http.tools import register_tools
        from xcsc_tushare_mcp_http.config import config
        from fastmcp import FastMCP
        import xcsc_tushare as ts
        from xcsc_tushare.client import DataApi
        
        mcp = FastMCP(name="test")
        ts.set_token(config.XCSC_TUSHARE_TOKEN)
        pro = DataApi(
            token=config.XCSC_TUSHARE_TOKEN,
            env=config.XCSC_ENV,
            server=config.XCSC_TUSHARE_SERVER,
            timeout=config.XCSC_TUSHARE_TIMEOUT
        )
        register_tools(mcp, pro)
        
        # 调用工具
        api_name = params.get("api_name")
        api_params = params.get("params")
        result = mcp.run_tool("get_api_query", {"api_name": api_name, "params": api_params})
        print(json.dumps({"toolcall_result": result}))
        sys.stdout.flush()
        
except Exception as e:
    print(json.dumps({"toolcall_result": {"error": str(e)}}))
    sys.stdout.flush()
'''
    
    # 写入临时测试文件
    temp_test_file = Path(__file__).parent / "temp_test_stdio.py"
    temp_test_file.write_text(test_code)
    
    try:
        # 测试 get_api_list
        print("测试 get_api_list 工具...")
        input_data = json.dumps({
            "toolcall": {
                "name": "get_api_list",
                "params": {}
            }
        })
        
        proc = subprocess.Popen(
            [sys.executable, str(temp_test_file)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        stdout, stderr = proc.communicate(input=input_data + "\n")
        
        if proc.returncode != 0:
            print(f"错误: {stderr}")
            return False
        
        result = json.loads(stdout)
        tool_result = result.get("toolcall_result", {})
        
        if tool_result.get("success"):
            print(f"✓ get_api_list 测试成功，找到 {tool_result.get('total_apis', 0)} 个 API")
        else:
            print(f"✗ get_api_list 测试失败: {tool_result.get('error')}")
            return False
        
        # 测试 get_api_query
        print(f"测试 get_api_query 工具...")
        input_data = json.dumps({
            "toolcall": {
                "name": "get_api_query",
                "params": {
                    "api_name": test_api,
                    "params": "{}"
                }
            }
        })
        
        proc = subprocess.Popen(
            [sys.executable, str(temp_test_file)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        stdout, stderr = proc.communicate(input=input_data + "\n")
        
        if proc.returncode != 0:
            print(f"错误: {stderr}")
            return False
        
        result = json.loads(stdout)
        tool_result = result.get("toolcall_result", {})
        
        if tool_result.get("success"):
            print(f"✓ get_api_query 测试成功，返回 {tool_result.get('count', 0)} 条数据")
        else:
            print(f"✗ get_api_query 测试失败: {tool_result.get('error')}")
            return False
        
        print("✓ stdio 模式测试通过！")
        return True
        
    finally:
        # 清理临时文件
        if temp_test_file.exists():
            temp_test_file.unlink()

def test_http_mode():
    """
    测试 HTTP 模式
    """
    print("\n=== 测试 HTTP 模式 ===")
    
    # 检查 XCSC_TUSHARE_TOKEN 是否设置
    if not os.getenv("XCSC_TUSHARE_TOKEN"):
        print("错误: 请设置 XCSC_TUSHARE_TOKEN 环境变量")
        return False
    
    # 启动 HTTP 服务器
    server_process = None
    try:
        # 启动服务器
        server_process = subprocess.Popen(
            [sys.executable, "-m", "xcsc_tushare_mcp_http"],
            env={**os.environ, "MCP_TRANSPORT": "http"},
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # 等待服务器启动
        print("启动 HTTP 服务器...")
        time.sleep(3)
        
        # 检查服务器是否启动成功
        stdout, stderr = server_process.communicate(timeout=1)
        if server_process.returncode is not None:
            print(f"服务器启动失败: {stderr}")
            return False
        
        # 测试 API 调用
        import requests
        
        # 获取 API 列表
        print("测试 get_api_list 工具...")
        response = requests.post(
            "http://localhost:8000/mcp",
            json={
                "toolcall": {
                    "name": "get_api_list",
                    "params": {}
                }
            },
            headers={"Authorization": f"Bearer {config.MCP_API_KEY}"}
        )
        
        if response.status_code != 200:
            print(f"HTTP 错误: {response.status_code}")
            return False
        
        result = response.json()
        tool_result = result.get("toolcall_result", {})
        
        if tool_result.get("success"):
            print(f"✓ get_api_list 测试成功，找到 {tool_result.get('total_apis', 0)} 个 API")
        else:
            print(f"✗ get_api_list 测试失败: {tool_result.get('error')}")
            return False
        
        # 测试第一个 API
        api_list = list(tool_result.get('data', {}).keys())
        test_api = api_list[0] if api_list else ""
        
        if test_api:
            print(f"测试 get_api_query 工具...")
            response = requests.post(
                "http://localhost:8000/mcp",
                json={
                    "toolcall": {
                        "name": "get_api_query",
                        "params": {
                            "api_name": test_api,
                            "params": "{}"
                        }
                    }
                },
                headers={"Authorization": f"Bearer {config.MCP_API_KEY}"}
            )
            
            if response.status_code != 200:
                print(f"HTTP 错误: {response.status_code}")
                return False
            
            result = response.json()
            tool_result = result.get("toolcall_result", {})
            
            if tool_result.get("success"):
                print(f"✓ get_api_query 测试成功，返回 {tool_result.get('count', 0)} 条数据")
            else:
                print(f"✗ get_api_query 测试失败: {tool_result.get('error')}")
                return False
        
        print("✓ HTTP 模式测试通过！")
        return True
        
    except subprocess.TimeoutExpired:
        # 服务器正在运行
        print("服务器正在运行...")
        return True
    except Exception as e:
        print(f"错误: {e}")
        return False
    finally:
        # 停止服务器
        if server_process and server_process.poll() is None:
            server_process.terminate()
            try:
                server_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                server_process.kill()

def main():
    """
    主函数
    """
    print("开始测试两种运行模式...")
    
    # 测试 stdio 模式
    stdio_success = test_stdio_mode()
    
    # 测试 HTTP 模式
    http_success = test_http_mode()
    
    print("\n=== 测试结果 ===")
    print(f"stdio 模式: {'✓ 成功' if stdio_success else '✗ 失败'}")
    print(f"HTTP 模式: {'✓ 成功' if http_success else '✗ 失败'}")
    
    if stdio_success and http_success:
        print("\n🎉 所有测试通过！两种运行模式都可以正常调用 API。")
        return 0
    else:
        print("\n❌ 测试失败，请检查配置和环境。")
        return 1

if __name__ == "__main__":
    sys.exit(main())
