from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from utils.templates import templates

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def show_home(request: Request):
        context = {
            "request": request,
        }
        return templates.TemplateResponse("inicio.html", context)



