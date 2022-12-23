import os

import dotenv

dotenv.load_dotenv(".env", override=True)
dotenv.load_dotenv(".env.local", override=True)

import uvicorn
import fastapi.middleware.cors as cors
from balocco.server.app import app

app.add_middleware(
    cors.CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

uvicorn.run(app, port=int(os.environ["IS_WEB_PORT"]), host="0.0.0.0")
