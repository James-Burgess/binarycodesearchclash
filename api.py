import json

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import HTTPException
from pydantic import BaseModel

from db import load_db, games
from main import run, Capturing


database = load_db()
app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get('/question/{question_name}/', response_class=HTMLResponse)
async def question(request: Request, question_name):
    try:
        with open(f"./questions/{question_name}.json", 'r') as f:
            question = json.loads(f.read())
        del question['large_question']
        return templates.TemplateResponse("question.html", {"request": request, "question": question})
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Item not found")


class Answer(BaseModel):
    username: str
    language: str
    code: str


@app.post('/question/{question_name}/test/')
async def test_result(question_name, answer: Answer):
    output = run(question_name, answer.code, answer.language)
    return {"STDOUT": output}


@app.post('/question/{question_name}/submit/')
async def submit_result(question_name, answer: Answer):
    output = run(question_name, answer.code, answer.language)
    passed = output[0] == "SUCCESS"
    if passed:
        time = output[1]
        query = games.insert().values(game=question_name, time=time, code=answer.code, language=answer.language, user=answer.username, success=passed)
    else:
        query = games.insert().values(game=question_name, time='99', code=answer.code, language=answer.language, user=answer.username, success=passed)

    last_record_id = await database.execute(query)
    return {**answer.dict(), "id": last_record_id}


@app.get('/question/{question_name}/leaderboard/', response_class=HTMLResponse)
async def leaderboard(request: Request, question_name):
    query = games.select().filter_by(game=question_name).order_by("time")
    resp = await database.fetch_all(query)
    return templates.TemplateResponse("leaderboard.html",
                                      {"request": request, "results": resp})
