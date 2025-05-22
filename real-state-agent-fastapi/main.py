from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from auth.router import router as auth_router
from property.router import router as property_router
from agent.router import router as agent_router
from real_state_agent.router import router as real_state_agent_router

load_dotenv()

def create_app() -> FastAPI:
    app = FastAPI(title="Real Estate Agent AI", version="1.0.0")

    configure_cors(app)
    configure_routes(app)
    configure_openapi(app)

    return app

def configure_cors(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"], 
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

def configure_routes(app: FastAPI) -> None:
    app.include_router(auth_router, tags=["auth"])
    app.include_router(property_router, tags=["properties"])
    app.include_router(agent_router, tags=["agents"])
    app.include_router(real_state_agent_router, tags=["real_state_agents"])

    @app.get("/", tags=["health"])
    def root():
        return {"message": "Real Estate Agent API is running"}

def configure_openapi(app: FastAPI) -> None:
    security_scheme = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema

        openapi_schema = get_openapi(
            title=app.title,
            version=app.version,
            description="API para corretor inteligente com autenticação",
            routes=app.routes,
        )
        openapi_schema["components"]["securitySchemes"] = security_scheme
        for path in openapi_schema["paths"].values():
            for operation in path.values():
                operation.setdefault("security", [{"BearerAuth": []}])

        app.openapi_schema = openapi_schema
        return openapi_schema

    app.openapi = custom_openapi

app = create_app()
