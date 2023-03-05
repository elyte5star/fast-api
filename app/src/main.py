from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging
from starlette.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from fastapi.exception_handlers import http_exception_handler
from fastapi.logger import logger
from resources.settings.config import Settings
from resources.database.db_session import AsyncDatabaseSession
from resources.crud.crud_users import Users
from resources.auth.crud_auth import Auth
from resources.crud.crud_products import Products
from resources.crud.crud_bookings import Bookings
from resources.crud.crud_pages import PageHandler
from resources.queue.booking_queue import QBookingHandler
from resources.routers import (
    auth,
    users,
    products,
    booking,
    pages,
    q_booking,
    job,
)
import time


cfg = Settings().from_toml_file()


logging.basicConfig(encoding=cfg.coding, level=cfg.log_type)

db = AsyncDatabaseSession(cfg)
db.int_db()

routes = (users, auth, products, booking, pages, q_booking, job)
crud_operations = (
    Users(cfg),
    Auth(cfg),
    Products(cfg),
    Bookings(cfg),
    PageHandler(cfg),
    QBookingHandler(cfg),
)
# page_op = [pages for i in range(len(crud_operations))]


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
app.mount(
    "/static", StaticFiles(directory="./resources/static"), name="static"
)


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    request.session.pop("user", None)
    logger.warning(f"{repr(exc.detail)}!!")
    return await http_exception_handler(request, exc)


# Add Routes
for route, crud in zip(routes, crud_operations):
    route.logger = logger
    route.handler = crud
    app.include_router(route.router)


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
    db.close()
    logger.info(f"{cfg.name} v{cfg.version} is shutting down.")
