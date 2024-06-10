import time

import uvicorn
from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from cor_auth.routes import auth
from cor_auth.database.db import get_db
from cor_auth.routes import auth, users, record

app = FastAPI()
app.mount("/static", StaticFiles(directory="cor_auth/static"), name="static")

origins = ["http://localhost:3000",
    "http://192.168.153.21:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    """
    The startup function is called when the application starts up.
    It's a good place to initialize things that are needed by your app, like database connections or caches.

    :return: A list of coroutines
    """
    print("------------- STARTUP --------------")


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """
    The add_process_time_header function adds a header to the response called My-Process-Time.
    The value of this header is the time it took for the request to be processed by all middleware and routes.

    :param request: Request: Access the request object
    :param call_next: Call the next function in the pipeline
    :return: A response object
    """
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["My-Process-Time"] = str(process_time)
    return response


@app.get("/", name="Корень")
def read_root():
    """
    The read_root function is a view function that returns the root of the API.
    It's purpose is to provide a simple way for users to test if their connection
    to the API is working properly.

    :return: A dictionary
    """
    return FileResponse("cor_auth/static/login.html")


@app.get("/api/healthchecker")
def healthchecher(db: Session = Depends(get_db)):
    """
    The healthchecher function is used to check the health of the application.
    It returns a message if everything is ok, or an error otherwise.

    :param db: Session: Pass the database connection to the function
    :return: A dict with a message
    """
    try:
        result = db.execute(text("SELECT 1")).fetchone()
        print(result)
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database is not configured correctly",
            )
        return {"message": "Welcome to FastApi, database work correctly"}
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error connecting to the database",
        )


app.include_router(auth.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(record.router, prefix="/api")


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", reload=True)
