# New Dicks as a Service (DaaS)
# 
# おちんぽを生成するための APIサービス。
# 様々なカテゴリ（asian, black, white, random）のおちんぽをASCIIアートとして生成します。
# 8=============D
# 
# エンドポイント:
#   - GET /dicks: おちんぽを生成 (クエリパラメータ: category, count)
#   - GET /stats: 生成統計を取得
#
# GitHub: https://github.com/FreeWiFi7749/DaaS

import os
import json
import random
import base64
import hashlib
import aiohttp
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List
from dotenv import load_dotenv

from fastapi import FastAPI, Query, Request, Response
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from starlette.middleware.base import BaseHTTPMiddleware

from internal._security import SecurityProvider

load_dotenv()

def _load_security() -> SecurityProvider:
    """セキュリティプロバイダーの初期化"""
    return SecurityProvider(Path(__file__).parent)

# セキュリティミドルウェアの設定
security = _load_security()

# FastAPIアプリケーションの初期化
app = FastAPI(
    title="Dicks as a Service",
    description="おちんぽ生成API",
    version="1.0.0",
    docs_url=None
)

# セキュリティミドルウェアを最初に追加
app.add_middleware(BaseHTTPMiddleware, dispatch=security.protect)

# 静的ファイルとテンプレートの設定
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# レスポンスモデルの定義
class DickResponse(BaseModel):
    category: str
    dicks: List[str]

class StatsResponse(BaseModel):
    random: int
    asian: int
    black: int
    white: int

class CaptchaResponse(BaseModel):
    token: str

def get_og_metadata(lang: str = "ja", page: str = "index") -> dict:
    metadata = {
        "index": {
            "ja": {
                "title": "8=D DICKS API - ASCIIアート革命",
                "description": "ASCIIアートの未来を体験せよ！アジアン、ブラック、ホワイト、ランダムなど、様々なスタイルのちんこを生成。満足したユーザー続出中！ 8====D"
            },
            "en": {
                "title": "8=D DICKS API - ASCII Art Revolution",
                "description": "Experience the future of ASCII art! Generate various styles of dicks - Asian, Black, White, Random, and more. Users can't get enough! 8====D"
            }
        },
        "docs": {
            "ja": {
                "title": "DICKS API - 今すぐ試そう！",
                "description": "たった1行でおちんぽ生成！ブラウザでお試しも、APIで本格導入もカンタン。さぁ、あなたも今すぐDICKS APIを体験してみよう！ 8====D"
            },
            "en": {
                "title": "DICKS API - Try it now!",
                "description": "Generate dicks with just one line of code! Easy to try in browser or integrate via API. Come experience DICKS API for yourself! 8====D"
            }
        }
    }
    return metadata.get(page, metadata["index"]).get(lang, metadata[page]["ja"])

def get_preferred_language(request: Request) -> str:
    accept_language = request.headers.get("accept-language", "")
    if accept_language:
        lang_code = accept_language.split(",")[0].split("-")[0].lower()
        if lang_code in ["ja", "en"]:
            return lang_code
    return "ja"

@app.get("/", response_class=HTMLResponse)
async def root(request: Request) -> HTMLResponse:
    """メインページの表示"""
    site_key = os.getenv("TURNSTILE_SITE_KEY")
    lang = get_preferred_language(request)
    og_data = get_og_metadata(lang, "index")
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "turnstile_site_key": site_key,
            "og_title": og_data["title"],
            "og_description": og_data["description"],
            "lang": lang
        }
    )

@app.get("/docs", response_class=HTMLResponse)
async def custom_docs(request: Request) -> HTMLResponse:
    """カスタムAPIドキュメントページの表示"""
    lang = get_preferred_language(request)
    og_data = get_og_metadata(lang, "docs")
    return templates.TemplateResponse(
        "custom_docs.html",
        {
            "request": request,
            "turnstile_site_key": os.getenv("TURNSTILE_SITE_KEY"),
            "og_title": og_data["title"],
            "og_description": og_data["description"],
            "lang": lang
        }
    )

@app.post("/verify-captcha")
async def verify_captcha(captcha: CaptchaResponse) -> Dict:
    """Cloudflare Turnstileの検証"""
    print(f"Verifying captcha token: {captcha.token}")  # デバッグ用
    secret_key = os.getenv("TURNSTILE_SECRET_KEY")
    print(f"Using secret key: {'[SET]' if secret_key else '[NOT SET]'}")  # デバッグ用
    
    # 開発環境では認証をスキップ
    if not secret_key:
        print("Development mode: skipping verification")  # デバッグ用
        return {"success": True}
        
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://challenges.cloudflare.com/turnstile/v0/siteverify",
                data={
                    "secret": secret_key,
                    "response": captcha.token
                }
            ) as response:
                result = await response.json()
                print(f"Cloudflare response: {result}")  # デバッグ用
                return {"success": result.get("success", False)}
    except Exception as e:
        print(f"Verification error: {e}")  # デバッグ用
        return {"success": False, "error": str(e)}

@app.get("/dicks", response_model=DickResponse)
async def get_dicks(
    category: Optional[str] = Query(
        None,
        description="おちんぽのカテゴリー"
    ),
    count: Optional[int] = Query(
        1,
        description="生成するおちんぽの数",
        ge=1,
        le=100
    ),
    response: Response = None
    
) -> DickResponse:

    """おちんぽの生成"""
    try:
        # カテゴリーの設定
        category = category or "random"
        if category not in ["random", "asian", "black", "white"]:
            category = "random"
            
        # カテゴリーごとの長さ範囲
        length_ranges = {
            "asian": (3, 7),    # 控えめサイズ
            "black": (8, 15),   # 迫力満点サイズ
            "white": (5, 10),   # 標準サイズ
            "random": (3, 15)   # ランダムサイズ
        }
        
        # おちんぽの生成（count分それぞれ異なる長さで生成）
        dicks = []
        for _ in range(count):
            length = random.randint(*length_ranges[category])
            shaft = "=" * length
            dicks.append(f"8{shaft}D")
        
        # 生成したおちんぽをランダムに並び替え
        random.shuffle(dicks)
        
        # 統計の更新
        stats_file = Path(__file__).parent / "data" / "stats.json"
        stats = {
            "random": 0,
            "asian": 0,
            "black": 0,
            "white": 0
        }
        
        if stats_file.exists():
            with open(stats_file) as f:
                data = json.load(f)
                if "categories" in data:
                    stats = data["categories"]
                else:
                    stats = data
        
        stats[category] += count
        
        os.makedirs(os.path.dirname(stats_file), exist_ok=True)
        with open(stats_file, "w") as f:
            json.dump(stats, f, indent=2)
            
        return DickResponse(
            category=category,
            dicks=dicks
        )
        
    except Exception as e:
        response.status_code = 500
        return DickResponse(
            category=category or "random",
            dicks=[f"Error: {str(e)}"]
        )

@app.get("/stats", response_model=StatsResponse)
async def get_stats() -> Dict:
    """統計情報の取得"""
    stats_file = Path(__file__).parent / "data" / "stats.json"
    stats = {
        "random": 0,
        "asian": 0,
        "black": 0,
        "white": 0
    }
    
    if stats_file.exists():
        with open(stats_file) as f:
            stats = json.load(f)
            
    return stats

@app.exception_handler(404)
async def custom_404_handler(request: Request, exc):
    """カスタム404ハンドラ"""
    return JSONResponse(
        status_code=404,
        content={
            "message": "このエンドポイントは存在しません。利用可能なエンドポイント: /dicks, /stats, /docs",
            "available_endpoints": ["/dicks", "/stats", "/docs"]
        }
    )
