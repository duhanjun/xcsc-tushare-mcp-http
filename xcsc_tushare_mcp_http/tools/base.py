"""
基础工具模块

该模块提供所有工具函数共用的基础功能：
1. format_dataframe: 格式化 XCSC Tushare 返回的 DataFrame 为标准 JSON 响应
2. format_error: 格式化异常信息为标准错误响应
3. format_response: 格式化通用响应
4. safe_str/safe_float/safe_int: 安全的类型转换函数

这些函数被所有数据查询工具模块使用，确保响应格式的一致性。
"""

import logging
from typing import Any, Dict, List, Optional

import pandas as pd

logger = logging.getLogger(__name__)


def format_dataframe(df: Optional[pd.DataFrame]) -> Dict[str, Any]:
    """
    格式化 XCSC Tushare 返回的 DataFrame 为标准 JSON 响应
    
    将 pandas DataFrame 转换为统一的响应格式，包含成功状态、
    数据列表、记录数和字段信息。同时处理 NaN 值和特殊数据类型。
    
    Args:
        df: XCSC Tushare API 返回的 DataFrame，可能为空或 None
    
    Returns:
        Dict[str, Any]: 标准化的响应字典，包含以下字段：
            - success: 请求是否成功
            - data: 数据列表（字典形式）
            - count: 记录数量
            - columns: 字段列表
    """
    if df is None or df.empty:
        return {
            "success": True,
            "data": [],
            "count": 0,
            "columns": [],
        }

    # 将 NaN 值替换为空字符串
    df = df.fillna("")

    # 转换为字典列表
    data = df.to_dict(orient="records")

    # 处理特殊数据类型（Timestamp、Tedelta 等）
    for record in data:
        for key, value in record.items():
            if pd.isna(value):
                record[key] = None
            elif hasattr(value, "item"):
                # 处理 numpy 标量类型
                record[key] = value.item()
            elif isinstance(value, (pd.Timestamp, pd.Timedelta)):
                # 将 pandas 时间类型转换为字符串
                record[key] = str(value)

    return {
        "success": True,
        "data": data,
        "count": len(data),
        "columns": list(df.columns),
    }


def format_error(error: Exception) -> Dict[str, Any]:
    """
    格式化异常信息为标准错误响应
    
    将发生的异常转换为统一的错误响应格式，并记录错误日志。
    
    Args:
        error: 发生的异常对象
    
    Returns:
        Dict[str, Any]: 标准化的错误响应字典，包含以下字段：
            - success: 固定为 False
            - error: 错误信息字符串
            - data: 固定为空列表
            - count: 固定为 0
            - columns: 固定为空列表
    """
    error_msg = str(error)
    logger.error(f"API 错误: {error_msg}")
    return {
        "success": False,
        "error": error_msg,
        "data": [],
        "count": 0,
        "columns": [],
    }


def format_response(
    success: bool,
    data: Optional[List[Dict[str, Any]]] = None,
    count: int = 0,
    columns: Optional[List[str]] = None,
    error: Optional[str] = None,
) -> Dict[str, Any]:
    """
    格式化通用响应
    
    根据传入参数构建标准化的响应字典。
    
    Args:
        success: 请求是否成功
        data: 数据列表
        count: 记录数量
        columns: 字段列表
        error: 错误信息（可选）
    
    Returns:
        Dict[str, Any]: 标准化的响应字典
    """
    return {
        "success": success,
        "data": data or [],
        "count": count,
        "columns": columns or [],
        "error": error,
    }


def safe_str(value: Any) -> Optional[str]:
    """
    安全地将值转换为字符串
    
    处理 None 和 NaN 值，避免转换错误。
    
    Args:
        value: 待转换的值
    
    Returns:
        Optional[str]: 转换后的字符串，如果值为 None 或 NaN 则返回 None
    """
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    return str(value)


def safe_float(value: Any) -> Optional[float]:
    """
    安全地将值转换为浮点数
    
    处理 None、NaN 值和转换错误。
    
    Args:
        value: 待转换的值
    
    Returns:
        Optional[float]: 转换后的浮点数，如果转换失败则返回 None
    """
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


def safe_int(value: Any) -> Optional[int]:
    """
    安全地将值转换为整数
    
    处理 None、NaN 值和转换错误。
    
    Args:
        value: 待转换的值
    
    Returns:
        Optional[int]: 转换后的整数，如果转换失败则返回 None
    """
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    try:
        return int(value)
    except (ValueError, TypeError):
        return None
