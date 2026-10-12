from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/addition")
def addition(a: int, b: int):
    return {"result a+b": a + b, "developer": "Dev1"}