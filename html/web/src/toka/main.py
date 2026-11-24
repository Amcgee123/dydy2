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
def root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={"project_name": "Toka"})
