#!/usr/bin/env python3
"""
简单测试脚本：验证两种运行模式
"""

import os
import sys
import subprocess
import time
import json
from pathlib import Path

# 设置测试环境
os.environ["XCSC_TUSHARE_TOKEN"] = "test_token"

print("=== 开始测试 ===")
print(f"Python 版本: {sys.version}")
print(f"当前目录: {os.getcwd()}")

# 测试 1: 直接运行服务器，验证 stdio 模式
print("\n1. 测试 stdio 模式 (默认)")
print("-" * 50)

try:
    # 运行服务器并检查输出
    result = subprocess.run(
        [sys.executable, "-m", "xcsc_tushare_mcp_http"],
        capture_output=True,
        text=True,
        timeout=5
    )
    
    if "传输方式: stdio" in result.stdout:
        print("✓ stdio 模式启动成功")
        print(f"  输出: {result.stdout.strip()[:100]}...")
    else:
        print("✗ stdio 模式启动失败")
        print(f"  错误: {result.stderr}")
        
except subprocess.TimeoutExpired:
    print("✓ stdio 模式启动成功 (运行中)")
except Exception as e:
    print(f"✗ stdio 模式启动失败: {e}")

# 测试 2: 测试 HTTP 模式
print("\n2. 测试 HTTP 模式")
print("-" * 50)

server_process = None
try:
    # 启动 HTTP 服务器
    server_process = subprocess.Popen(
        [sys.executable, "-m", "xcsc_tushare_mcp_http"],
        env={**os.environ, "MCP_TRANSPORT": "http"},
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # 等待服务器启动
    time.sleep(2)
    
    # 读取启动输出
    stdout, stderr = server_process.communicate(timeout=2)
    
    if "传输方式: http" in stdout:
        print("✓ HTTP 模式启动成功")
        print(f"  服务地址: http://localhost:8000/mcp")
        print(f"  输出: {stdout.strip()[:150]}...")
    else:
        print("✗ HTTP 模式启动失败")
        print(f"  错误: {stderr}")
        
except subprocess.TimeoutExpired:
    print("✓ HTTP 模式启动成功 (运行中)")
except Exception as e:
    print(f"✗ HTTP 模式启动失败: {e}")
finally:
    # 停止服务器
    if server_process and server_process.poll() is None:
        server_process.terminate()
        try:
            server_process.wait(timeout=3)
        except subprocess.TimeoutExpired:
            server_process.kill()

# 测试 3: 验证 API 元数据
print("\n3. 验证 API 元数据")
print("-" * 50)

sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    from xcsc_tushare_mcp_http.metadata import load_api_metadata
    
    metadata = load_api_metadata()
    total_apis = metadata.get("total_apis", 0)
    api_list = list(metadata.get("apis", {}).keys())
    
    print(f"✓ API 元数据加载成功")
    print(f"  总 API 数量: {total_apis}")
    print(f"  前 5 个 API: {api_list[:5]}")
    
except Exception as e:
    print(f"✗ API 元数据加载失败: {e}")

print("\n=== 测试完成 ===")
