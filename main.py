import logging
import asyncio

from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.staticfiles import StaticFiles
from starlette_admin.contrib.sqla import Admin
from starlette_admin.contrib.sqla import ModelView


from config import settings
from db import Base, engine, create_db_and_tables, User
from infrastructure.gui.index import router as router_index
from model import Student, Teacher
from provider import MyAuthProvider
from schemas import UserRead, UserUpdate, UserCreate
from users import auth_backend, fastapi_users
from utils.fastapi_app import get_application
from utils.logging_config import config_logging
from views import StudentView


app = get_application()
app.mount("/static", StaticFiles(directory="static"), name="static")
config_logging()
logger = logging.getLogger(__name__)

app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)

# Create admin
admin = Admin(
    engine,
    title="Example: Auth",
    base_url="/admin",
    statics_dir="static",
    login_logo_url="/admin/statics/img/logo.svg",  # base_url + '/statics/' + path_to_the_file
    auth_provider=MyAuthProvider(allow_paths=["/statics/img/logo.svg"]),
    middlewares=[Middleware(SessionMiddleware, secret_key=settings.secret_key)],
)


@app.on_event("startup")
async def on_startup():
    # Not needed if you setup a migration system like Alembic
    await create_db_and_tables()

# Add views
admin.add_view(StudentView(Student))
admin.add_view(ModelView(Teacher))
admin.add_view(ModelView(User))

# Mount admin
admin.mount_to(app)

# Rutas
app.include_router(router_index)
