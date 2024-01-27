from fastapi import FastAPI
from dotenv import load_dotenv
import uvicorn
from lib.fetcher import scrape

load_dotenv()

app = FastAPI()


@app.get("/")
async def read_root(word: str = ""):
    if(word == ""):
        return "get lost!"
    return scrape(word)

if __name__ == '__main__':
    uvicorn.run(app, port=8888, host='127.0.0.1')