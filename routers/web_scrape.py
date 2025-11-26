from fastapi import (
    APIRouter,
    Form,
    Request
)

from bs4 import BeautifulSoup

from settings import TEMPLATES

router = APIRouter(tags=["scraping"])

@router.get("/scrape")
async def home_page(
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


@router.post("/scrape/csv")
async def export_to_csv(
    request: Request,
    url_page: str = Form(...),
):
    """
    URL JSON format to CSV.
    """
    
    pass
