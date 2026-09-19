# from fastapi import FastAPI
# from starlette.responses import RedirectResponse
# from fastapi.responses import Response
# import os

# from textsummarizer.pipeline.prediction_pipeline import predict


# app = FastAPI()


# @app.get("/", tags=["authentication"])
# async def index():
#     return RedirectResponse(url="/docs")


# @app.get("/train")
# async def training():
#     try:
#         os.system("python main.py")
#         return Response("Training successful")

#     except Exception as e:
#         return Response(f"error occurred {e}")


# @app.post("/predict")
# async def prediction(text: str):
#     try:
#         data = predict(text)
#         return Response(data)

#     except Exception as e:
#         return Response(f"Error occurred {e}")


from fastapi import FastAPI
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

from textsummarizer.pipeline.prediction_pipeline import predict


app = FastAPI()


# Serve CSS and JavaScript
app.mount("/static", StaticFiles(directory="static"), name="static")


# HTML templates
templates = Jinja2Templates(directory="templates")


# Home page
@app.get("/", response_class=HTMLResponse)
async def index():
    with open("templates/index.html", "r", encoding="utf-8") as file:
        return HTMLResponse(content=file.read())


# Training endpoint
@app.get("/train")
async def training():
    try:
        os.system("python main.py")
        return Response("Training successful")
    except Exception as e:
        return Response(f"Error occurred {e}")


# Prediction endpoint
@app.post("/predict")
async def prediction(text: str):
    try:
        data = predict(text)
        return Response(data)
    except Exception as e:
        return Response(f"Error occurred {e}")