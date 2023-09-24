from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def test():
    return "Hello, World!"
