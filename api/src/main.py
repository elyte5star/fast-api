from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError
import logging
from starlette.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, PlainTextResponse

# from starlette.middleware.sessions import SessionMiddleware
from fastapi.logger import logger
from modules.settings.config import Settings
from modules.utils.base_functions import Utilities
from modules.crud.crud_users import Users
from modules.auth.crud_auth import Auth
from modules.crud.crud_products import Products
from modules.crud.crud_bookings import Bookings
from modules.crud.jobs import DbJobs

from modules.queue.booking_queue import QBookingHandler
from modules.routers import auth, users, products, booking, q_booking, job
import time


cfg = Settings().from_toml_file().from_env_file()


logging.basicConfig(encoding=cfg.encoding, level=cfg.log_type)

db = Utilities(cfg)
db.async_session_generator()

routes = (users, auth, products, booking, q_booking, job)
crud_operations = (
    Users(cfg),
    Auth(cfg),
    Products(cfg),
    Bookings(cfg),
    QBookingHandler(cfg),
    DbJobs(cfg),
)


app = FastAPI(
    debug=cfg.debug,
    title=cfg.name,
    description=cfg.description,
    version=cfg.version,
    terms_of_service=cfg.terms,
    contact=cfg.contacts,
    license_info=cfg.license,
    swagger_ui_parameters={
        "syntaxHighlight.theme": "tomorrow-night",
        "tryItOutEnabled": True,
        "displayRequestDuration": True,
    },
)


ALLOWED_HOSTS = ["*"]

if cfg.origins:
    ALLOWED_HOSTS = [str(origin) for origin in cfg.origins]
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    max_age=3600,
)

# Include Session
# app.add_middleware(SessionMiddleware, secret_key=cfg.secret_key, max_age=1500)
app.mount("/static", StaticFiles(directory="./modules/static"), name="static")


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    logger.warning(f"{repr(exc.detail)}!!")
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder(
            {"data": {"message": str(exc.detail), "success": False}}
        ),
    )


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
    response.headers["root_path"] = request.scope.get('root_path')
    return response


# Override request validation exceptions
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=400)


@app.on_event("startup")
async def startup_event() -> None:
    await db.create_all()
    logger.info(f"{cfg.name} v{cfg.version} is starting.")


@app.on_event("shutdown")
async def shuttdown() -> None:
    await db._engine.dispose()
    logger.info(f"{cfg.name} v{cfg.version} is shutting down.")
