import json
from typing import Union

from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware

from thegreatsuspender import clean_data, SESSION_NAME_SUFFIX, EXTENSION_ID


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/heartbeat/")
async def root():
    """Heartbeat."""
    return {"message": "Heartbeat"}


@app.post("/clean-data/")
async def clean_json_data(
    data: Union[dict, str] = Body(
        ...,
        title="Data",
        description="Your tabs data exported with FreshStart - "
                    "Cross Browser Session Manager"
    ),
    session_name_suffix: str = Body(
        SESSION_NAME_SUFFIX,
        title="Session name suffix",
        description=f"Session name suffix. Defaults to "
                    f"`{SESSION_NAME_SUFFIX}`.",
        alias="sessionNameSuffix"
    ),
    extension_id: str = Body(
        None,
        title="ID of ``The Great Suspender`` extension.",
        description=f"Defaults to "
                    f"`{EXTENSION_ID}`.",
        alias="extensionId"
    ),
):
    """Clean tabs data exported with FreshStart - Cross Browser Session
    Manager.
    """
    if not isinstance(data, dict):
        data = json.loads(data)
    cleaned_data = clean_data(
        data,
        session_name_suffix=session_name_suffix,
        extension_id=extension_id,
    )
    return cleaned_data
