from fastapi import (
    APIRouter, 
    Depends, 
    Form, 
    Request
)
from fastapi.responses import (
    RedirectResponse, 
)
from sqlmodel import (
    or_,
    select
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from datetime import datetime

from database import get_session
from models.models import (
    Card,
    Era,
    Rarity,
    Set,
)
from settings import TEMPLATES


router = APIRouter(prefix="/pokemon", tags=["Pokemon card API"])

@router.get("/")
async def list_series(
    request: Request,
    db: AsyncSession = Depends(get_session)
):
    """
    list of pokemon card sets
    """
    query = await db.execute(select(Set).options(selectinload(Set.era)))
    sets = query.scalars().all()

    return TEMPLATES.TemplateResponse(
        "pages/pokemon/home.html",
        {
            "request": request,
            "sets": sets,
        },
    )


@router.get("/{gen}/{id}")
async def list_sets(
    request: Request,
    gen: str,
    id: int,
    db: AsyncSession = Depends(get_session)
):
    """
    List the cards of the set (API is set to "Era/Series/Set".)
    """
    query = await db.execute(select(Set))
    sets = query.scalars().all()

    return TEMPLATES.TemplateResponse(
        "pages/pokemon/home.html",
        {
            "request": request,
            "sets": sets,
        },
    )


@router.get("/register")
async def registration_form(
    request: Request,
    db: AsyncSession = Depends(get_session)
):
    """
    Form in adding new set for pokemon.
    """
    query = await db.execute(select(Era))
    eras = query.scalars().all()

    return TEMPLATES.TemplateResponse(
        "pages/pokemon/register.html",
        {
            "request": request,
            "eras": eras,
        },
    )


@router.post("/register")
async def submit_registration_form(
    request: Request, 
    era_id: int = Form(...), 
    set_name: str = Form(...), 
    set_code: str = Form(...), 
    release_date: str = Form(...),
    db: AsyncSession = Depends(get_session)
):
    """
    Submits the form to add new set for pokemon on database.
    """
    query = await db.execute(
        select(Set).where(
            Set.name == set_name
        )
    )
    exists = query.scalar_one_or_none()
    if exists:
        return RedirectResponse(
            url="/pokemon/register?msg=Already%Exist",
            status_code=303
        )
    
    release_date_obj = datetime.strptime(release_date, "%m/%d/%Y").date()

    new_set = Set(
        era_id = era_id,
        name = set_name,
        code = set_code,
        release_date=release_date_obj
    )
    db.add(new_set)
    await db.commit()

    return RedirectResponse (url="/pokemon", status_code=303)