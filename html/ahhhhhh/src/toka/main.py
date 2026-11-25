from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

folder = Path(__file__).resolve().parent

app = FastAPI()
app.mount("/static", StaticFiles(directory=str(folder / "static")), name="static")
templates = Jinja2Templates(directory=str(folder / "templates"))

@app.get("/", response_class=HTMLResponse)
def Homescreen(request: Request):
    return templates.TemplateResponse(request=request, name="Homescreen.html", context={"project_name": "Toka"})

@app.get("/plans", response_class=HTMLResponse)
def plans(request: Request):
    return templates.TemplateResponse(request=request, name="plans.html", context={"project_name": "Toka"})

@app.get("/our_content", response_class=HTMLResponse)
def content(request: Request):
    return templates.TemplateResponse(request=request, name="Our_content.html", context={"project_name": "Toka"})

@app.get("/social", response_class=HTMLResponse)
def social(request: Request):
    return templates.TemplateResponse(request=request, name="social.html", context={"project_name": "Toka"})

@app.get("/account_page", response_class=HTMLResponse)
def account_page(request: Request):
    return templates.TemplateResponse(request=request, name="our_content.html", context={"project_name": "Toka"})