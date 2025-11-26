from fastapi import (
    APIRouter,
    Request
)

from settings import TEMPLATES

router = APIRouter(tags=["base"])

@router.get("/")
async def endorsement_page(
    request: Request,
):
    """
    Endorsement page.
    """
    return TEMPLATES.TemplateResponse(
        "pages/base/endorsement.html",
        {
            "request": request,
        },
    )


@router.get("/home")
async def home_page(
    request: Request,
):
    """
    Home page.
    """
    return TEMPLATES.TemplateResponse(
        "pages/base/home.html",
        {
            "request": request,
        },
    )