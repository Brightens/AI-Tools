from fastapi import (
    APIRouter,
    Depends,
    Form,
    Request
)
from fastapi.responses import (
    RedirectResponse
)

import pandas as pd

from sqlmodel import (
    or_,
    select
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

import requests

from database import get_session

from settings import TEMPLATES


router = APIRouter(prefix="/ai", tags=["base"])

@router.get("/")
async def ai_home(
    request: Request,
    db: AsyncSession = Depends(get_session),
):
    """
    Docstring for ai_home.
    """

    return TEMPLATES.TemplateResponse(
        "pages/ai/home.html",
        {
            "request": request,
        },
    )


@router.post("/transform")
async def transform_to_table(
    request: Request,
    url_page: str = Form(...),
):
    """
    URL JSON format to Table.
    """
    json_data = requests.get(url_page).json()
    first_key = next(iter(json_data))
    data = json_data[first_key]
    df = pd.DataFrame(data)
    df = df.astype(str).replace({r"[\[\]\{\}'\"]": ""}, regex=True)
    request.session["table_data"] = df.to_dict()

    return RedirectResponse(url="/ai/transform", status_code=303)


@router.get("/transform")
async def transform_to_table(
    request: Request,
    db: AsyncSession = Depends(get_session),
):
    """
    Display URL JSON format to Table.
    """
    import ipdb; ipdb.set_trace()

    return TEMPLATES.TemplateResponse(
        "pages/ai/home.html",
        {
            "request": request,
        },
    )