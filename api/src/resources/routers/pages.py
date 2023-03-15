from fastapi import APIRouter, Form, Depends
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.requests import Request
from resources.schemas.requests.auth import JWTcredentials
from resources.auth.dependency import security


router = APIRouter(prefix="", tags=["HTML"])


@router.get("/favicon.ico", include_in_schema=False)
def favicon():
    return StaticFiles(directory="./resources/static")


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    user_info = None
    if "user" in request.session:
        user_info = request.session.get("user")
    return await handler.index_page(
        {"request": request, "userinfo": user_info}
    )


@router.get("/news", response_class=HTMLResponse)
async def news(request: Request):
    user_info = None
    if "user" in request.session:
        user_info = request.session.get("user")
    return await handler._news({"request": request, "userinfo": user_info})


@router.get("/game", response_class=HTMLResponse)
async def game(request: Request):
    user_info = None
    if "user" in request.session:
        user_info = request.session.get("user")
    return await handler._game({"request": request, "userinfo": user_info})


@router.get("/map", response_class=HTMLResponse)
async def map(request: Request):
    user_info = None
    if "user" in request.session:
        user_info = request.session.get("user")
    return await handler._map({"request": request, "userinfo": user_info})


@router.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return await handler._login({"request": request})


@router.get("/admin", response_class=HTMLResponse)
async def admin(request: Request):
    return await handler._admin({"request": request})


@router.get("/{pid}", response_class=HTMLResponse)
async def one_product(pid: str, request: Request):
    user_info = None
    if "user" in request.session:
        user_info = request.session.get("user")
    return await handler._one_product(
        {"pid": pid, "request": request, "userinfo": user_info}
    )


# Sort Items
@router.get("/sort/", response_class=HTMLResponse)
async def sort_items(sort_key: str, request: Request):
    user_info = None
    if "user" in request.session:
        user_info = request.session.get("user")
    return await handler._sort_items_(
        {"sort_key": sort_key, "request": request, "userinfo": user_info}
    )


@router.post("/create_booking", response_class=HTMLResponse)
async def booking(
    request: Request,
    pid: str = Form(default=None),
    volume: str = Form(default=None),
    unit_price: str = Form(default=None),
):
    return await handler._create_booking(
        {
            "pid": pid,
            "request": request,
            "volume": volume,
            "unit_price": unit_price,
        }
    )
