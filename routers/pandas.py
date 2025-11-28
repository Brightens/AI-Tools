from fastapi import (
    APIRouter,
    Form,
    Request
)
from fastapi.responses import StreamingResponse

from bs4 import BeautifulSoup

import pandas as pd

import io
import requests

from settings import TEMPLATES

router = APIRouter(prefix="/pandas", tags=["pandas"])

@router.get("/web-scrape")
async def web_scrape_page(
    request: Request,
):
    """
    URL paste page.
    """
    return TEMPLATES.TemplateResponse(
        "pages/scrape/web-scrape.html",
        {
            "request": request,
        },
    )


@router.post("/web-scrape-to-csv")
async def web_scrape_export(
    request: Request,
    url_page: str = Form(...),
):
    """
    URL JSON format to CSV.
    """
    data = requests.get(url_page).json().get("products")
    df = pd.DataFrame(data)

    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)

    return StreamingResponse(
        io.BytesIO(csv_buffer.getvalue().encode("utf-8")),
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=output.csv"
        }
    )
