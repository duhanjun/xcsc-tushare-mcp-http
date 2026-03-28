"""
认证中间件模块

提供 API Key 认证功能，支持 Bearer Token 和 Basic 认证方式。

使用示例：
    >>> from xcsc_tushare_mcp_http.auth import create_auth_middleware
    >>> app = create_auth_middleware(app, api_key="your_key", auth_enabled=True)

支持的认证方式：
1. Bearer Token: Authorization: Bearer your_api_key
2. Basic Auth: Authorization: Basic base64(username:password)
3. 纯 Token: Authorization: your_api_key
"""

import base64
from typing import Optional
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse


class AuthMiddleware(BaseHTTPMiddleware):
    """
    认证中间件类
    
    该类继承自 Starlette 的 BaseHTTPMiddleware，用于验证请求的 API Key。
    支持 Bearer Token、Basic Auth 和纯 Token 三种认证方式。
    
    Attributes:
        api_key: 有效的 API Key
        auth_enabled: 是否启用认证
    
    使用示例：
        >>> from starlette.applications import Starlette
        >>> app = Starlette()
        >>> app.add_middleware(AuthMiddleware, api_key="secret", auth_enabled=True)
    """
    
    def __init__(self, app, api_key: str, auth_enabled: bool = True):
        """
        初始化认证中间件
        
        Args:
            app: Starlette/FastAPI 应用实例
            api_key: 有效的 API Key
            auth_enabled: 是否启用认证，默认为 True
        """
        super().__init__(app)
        self.api_key = api_key
        self.auth_enabled = auth_enabled

    async def dispatch(self, request: Request, call_next):
        """
        处理请求并进行认证
        
        Args:
            request: HTTP 请求对象
            call_next: 下一个中间件或路由处理函数
        
        Returns:
            Response: HTTP 响应对象
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
        
        支持以下格式：
        - Bearer Token: "Bearer your_token"
        - Basic Auth: "Basic base64(username:password)"
        - 纯 Token: "your_token"
        
        Args:
            auth_header: Authorization 请求头的值
        
        Returns:
            Optional[str]: 提取到的 Token，如果格式无效则返回 None
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
    
    这是一个便捷函数，用于创建并返回 AuthMiddleware 实例。
    
    Args:
        app: Starlette/FastAPI 应用实例
        api_key: 有效的 API Key
        auth_enabled: 是否启用认证，默认为 True
    
    Returns:
        AuthMiddleware: 认证中间件实例
    
    使用示例：
        >>> from starlette.applications import Starlette
        >>> app = Starlette()
        >>> app = create_auth_middleware(app, api_key="secret")
    """
    return AuthMiddleware(app, api_key, auth_enabled)
