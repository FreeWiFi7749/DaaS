"""
基本的なセキュリティ機能を提供するモジュール
このファイルはOSSとして公開されます
"""

from datetime import datetime, timedelta
from collections import defaultdict
from pathlib import Path
from typing import Dict
from fastapi import Request
from fastapi.responses import JSONResponse

class SecurityLite:
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.ip_data_dir = data_dir / "ip_data"
        self.banned_ips_file = data_dir / "banned_ips.json"
        self.ip_requests = defaultdict(lambda: defaultdict(list))
        self.blocked_ips = {}
        self.ip_data_dir.mkdir(parents=True, exist_ok=True)

    def is_rate_limited(self, ip: str, path: str) -> bool:
        """基本的なレートリミット"""
        now = datetime.now()
        duration = timedelta(minutes=5)
        max_requests = 100 if path == "/docs" else 10
        
        self.ip_requests[ip][path] = [
            t for t in self.ip_requests[ip][path]
            if now - t < duration
        ]
        
        if len(self.ip_requests[ip][path]) >= max_requests:
            return True
        
        self.ip_requests[ip][path].append(now)
        return False

    async def protect(self, request: Request, call_next) -> JSONResponse:
        """基本的なセキュリティミドルウェア"""
        client_ip = request.client.host
        path = request.url.path

        # レートリミットのみをチェック
        if self.is_rate_limited(client_ip, path):
            return JSONResponse(
                status_code=429,
                content={"detail": "Too many requests"}
            )

        return await call_next(request)
