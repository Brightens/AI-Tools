from fastapi import (
    APIRouter, 
    Depends, 
    Form, 
    Request,
    Query
)
from fastapi.responses import (
    RedirectResponse, 
)

from scipy import stats

from sqlmodel import (
    or_,
    select
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from datetime import datetime
import random

from data import CARDS
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
    set_query = await db.execute(select(Set).options(selectinload(Set.era)))
    sets = set_query.scalars().all()

    era_query = await db.execute(select(Era))
    eras = era_query.scalars().all()

    return TEMPLATES.TemplateResponse(
        "pages/pokemon/home.html",
        {
            "request": request,
            "eras": eras,
            "sets": sets,
        },
    )


@router.get("/eras/{era}/{id}")
async def list_cards(
    request: Request,
    era: str,
    id: int,
    db: AsyncSession = Depends(get_session)
):
    """
    List the cards of the set (API is set to "Era/Series/Set".)
    """
    cards_query = await db.execute(select(Card).filter(Card.set_id == id)
        .options(selectinload(Card.rarity)))
    cards  = cards_query.scalars().all()

    return TEMPLATES.TemplateResponse(
        "pages/pokemon/set_cards.html",
        {
            "request": request,
            "cards": cards,
            "cards_count": len(cards),
            "id": id
        },
    )


@router.get("/cards/{id}/open")
async def open_pack(
    request: Request,
    id: int,
    quantity: int = Query(..., ge=1, le=5),
    db: AsyncSession = Depends(get_session)
):
    """
    Display obtained random cards
    """
    cards = []
    COMMONS = 7
    RARES = 3

    common_query = await db.execute(select(Card).filter(Card.set_id == id, Card.rarity_id <= 2)
        .options(selectinload(Card.rarity)))
    common_cards  = common_query.scalars().all()

    rare_query = await db.execute(select(Card).filter(Card.set_id == id, Card.rarity_id >= 3)
        .options(selectinload(Card.rarity)))
    rare_cards  = rare_query.scalars().all()

    for _ in range(quantity):
        # commons
        for _ in range(COMMONS):
            cards.append(random.choice(common_cards))

        # rares
        for _ in range(RARES):
            cards.append(random.choice(rare_cards))


    return TEMPLATES.TemplateResponse(
        "pages/pokemon/cards.html",
        {
            "request": request,
            "cards": cards
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
