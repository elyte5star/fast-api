from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging
from starlette.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from fastapi.exception_handlers import http_exception_handler
from fastapi.logger import logger
from modules.settings.config import Settings
from modules.database.db_session import AsyncDatabaseSession
from modules.utils.base_functions import Utilities
from modules.crud.crud_users import Users
from modules.auth.crud_auth import Auth
from modules.crud.crud_products import Products
from modules.crud.crud_bookings import Bookings

from modules.queue.booking_queue import QBookingHandler
from modules.routers import (
    auth,
    users,
    products,
    booking,
    q_booking,
)
import time


cfg = Settings().from_toml_file()


logging.basicConfig(encoding=cfg.coding, level=cfg.log_type)

db = Utilities(cfg)
db.async_session_generator()

routes = (users, auth, products, booking, q_booking)
crud_operations = (
    Users(cfg),
    Auth(cfg),
    Products(cfg),
    Bookings(cfg),
    QBookingHandler(cfg),
)


app = FastAPI(
    debug=cfg.debug,
    title=cfg.name,
    description=cfg.description,
    version=cfg.version,
    swagger_ui_parameters={
        "syntaxHighlight.theme": "tomorrow-night",
        "tryItOutEnabled": True,
        "displayRequestDuration": True,
    },
)


ALLOWED_HOSTS = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Session
app.add_middleware(SessionMiddleware, secret_key=cfg.secret_key, max_age=1500)
app.mount("/static", StaticFiles(directory="./modules/static"), name="static")


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    logger.warning(f"{repr(exc.detail)}!!")
    return await http_exception_handler(request, exc)


# Add Routes
for route, crud in zip(routes, crud_operations):
    route.logger = logger
    route.handler = crud
    app.include_router(route.router)


@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return StaticFiles(directory="./modules/static")


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.on_event("startup")
async def startup_event() -> None:
    await db.create_all()
    logger.info(f"{cfg.name} v{cfg.version} is starting.")


@app.on_event("shutdown")
async def shuttdown() -> None:
    await db._engine.dispose()
    logger.info(f"{cfg.name} v{cfg.version} is shutting down.")
