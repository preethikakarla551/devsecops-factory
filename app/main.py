from fastapi import FastAPI

app = FastAPI(title="DevSecOps Factory", version="1.0.0")


@app.get("/")
def read_root() -> dict[str, str]:
    return {"service": "devsecops-factory", "status": "running"}


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "healthy"}
