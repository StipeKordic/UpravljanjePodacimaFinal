from fastapi import APIRouter, Depends, Request, Cookie, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

home_router = APIRouter(
    prefix="/home",
    tags=["Home"]
)

templates = Jinja2Templates(directory="templates")

@home_router.get("/")
def home(request: Request, access_token: str = Cookie(None)):
    if access_token is None:
        return RedirectResponse(url="/auth/login", status_code=status.HTTP_303_SEE_OTHER)
    return templates.TemplateResponse("home.html", {"request": request})