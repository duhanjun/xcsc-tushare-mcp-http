"""
认证中间件模块

该模块提供 API Key 认证功能，支持多种认证方式：
1. Bearer Token 认证（标准方式）
2. Basic 认证（支持从密码中提取 Token）
3. 简单 Token 认证（直接传递 Token）

认证流程：
1. 检查是否启用了认证（未启用则跳过）
2. 从请求头中获取 Authorization 信息
3. 验证 Token 是否有效
4. 通过验证后放行请求
"""

import base64
from typing import Optional
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse


class AuthMiddleware(BaseHTTPMiddleware):
    """
    认证中间件类
    
    用于验证客户端请求的合法性，支持 Bearer Token 和 Basic 认证方式。
    """
    
    def __init__(self, app, api_key: str, auth_enabled: bool = True):
        """
        初始化认证中间件
        
        Args:
            app: ASGI 应用实例
            api_key: 有效的 API Key
            auth_enabled: 是否启用认证
        """
        super().__init__(app)
        self.api_key = api_key
        self.auth_enabled = auth_enabled

    async def dispatch(self, request: Request, call_next):
        """
        处理每个请求的认证逻辑
        
        Args:
            request: HTTP 请求对象
            call_next: 下一个处理函数
        
        Returns:
            JSONResponse: 认证失败时返回错误响应，或者继续处理请求
        """
        if not self.auth_enabled:
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        
        if not auth_header:
            return JSONResponse(
                {"error": "缺少 Authorization 请求头"},
                status_code=401,
                headers={"WWW-Authenticate": "Bearer"}
            )

        token = self._extract_token(auth_header)
        
        if token is None:
            return JSONResponse(
                {"error": "无效的 Authorization 请求头格式"},
                status_code=401,
                headers={"WWW-Authenticate": "Bearer"}
            )

        if not self._verify_token(token):
            return JSONResponse(
                {"error": "无效的 API Key"},
                status_code=403,
                headers={"WWW-Authenticate": "Bearer"}
            )

        return await call_next(request)

    def _extract_token(self, auth_header: str) -> Optional[str]:
        """
        从 Authorization 请求头中提取 Token
        
        支持三种格式：
        1. Bearer Token: "Bearer <token>"
        2. Basic 认证: "Basic <base64(username:password)>"，提取密码部分作为 Token
        3. 简单 Token: 直接传递 "<token>"
        
        Args:
            auth_header: Authorization 请求头内容
        
        Returns:
            Optional[str]: 提取的 Token，如果格式无效返回 None
        """
        parts = auth_header.split()
        
        if len(parts) == 2:
            scheme, token = parts
            if scheme.lower() == "bearer":
                return token
            elif scheme.lower() == "basic":
                try:
                    decoded = base64.b64decode(token).decode("utf-8")
                    if ":" in decoded:
                        _, password = decoded.split(":", 1)
                        return password
                except Exception:
                    pass
        
        if len(parts) == 1:
            return parts[0]
        
        return None

    def _verify_token(self, token: str) -> bool:
        """
        验证 Token 是否有效
        
        Args:
            token: 待验证的 Token
        
        Returns:
            bool: Token 是否有效
        """
        return token == self.api_key


def create_auth_middleware(app, api_key: str, auth_enabled: bool = True):
    """
    创建认证中间件的工厂函数
    
    Args:
        app: ASGI 应用实例
        api_key: 有效的 API Key
        auth_enabled: 是否启用认证
    
    Returns:
        AuthMiddleware: 配置好的认证中间件
    """
    return AuthMiddleware(app, api_key, auth_enabled)
