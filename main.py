from fastapi import FastAPI, status
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
from routes import auth_routes, ad_type_routes, ad_routes, home_routes, user_routes


app = FastAPI()
app.include_router(auth_routes.auth_router)
app.include_router(ad_type_routes.ad_type_router)
app.include_router(ad_routes.ad_router)
app.include_router(home_routes.home_router)
app.include_router(user_routes.user_router)

origins = {
    "http://localhost"
}

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def home():
    return RedirectResponse(url="/docs")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)
