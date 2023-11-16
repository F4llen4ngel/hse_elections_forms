from functools import lru_cache

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

import config

import lib.database as db


app = FastAPI(
    title="Form app",
    version="1.0.0",
)
templates = Jinja2Templates(directory="templates")
# bot = telegram.Bot(token=config.TG_TOKEN)


@lru_cache(1)
def get_survey():
    with open("templates/test.json", encoding="utf-8") as f:
        data = f.read()
    return data.replace("\n", " ").replace("  ", " ")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"form_name": config.FORM_NAME, "surveyJSON": get_survey(), "request": request})


@app.post("/")
async def submit(request: Request):
    data = await request.json()
    message = f'<b>Новая заявка из формы "{config.FORM_NAME}"</b>\n\n'
    for key, value in data.items():
        # логика зависит от конкретной формы
        if key == 'chat':
            if 'vk' in value:
                message += f'<b>VK</b>: vk.com/{value["vk"][1:]}\n'
            if 'tg' in value:
                message += f'<b>TG</b>: {value["tg"]}\n'
        else:
            message += f"<b>{key}</b>: {value}\n"
    db.save(message)
    return {"ok": True}


if __name__ == "__main__":
    db.init_db(
        host=config.DB_HOST,
        dbname=config.DB_NAME,
        user=config.DB_USER,
        password=config.DB_PASSWORD
    )
    uvicorn.run(app, host="0.0.0.0", port=8080)