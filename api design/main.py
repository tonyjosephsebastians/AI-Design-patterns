from fastapi import FastAPI

app = FastAPI(title = " a samll fastapi")

@app.get("/")
def read_root():
    return {"message":"Hello from fastapi"}

@app.get("/health")
def health():
    return {"status":"ok"}