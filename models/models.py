from sqlmodel import (
    Field,
    Relationship,
    SQLModel,
)

from datetime import datetime
from typing import (
    List,
    Optional
)


class Era(SQLModel, table=True):
    __tablename__ = "eras"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100, index=True)
    
    # Relationships
    sets: List["Set"] = Relationship(back_populates="era")


class Set(SQLModel, table=True):
    __tablename__ = "sets"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    era_id: int = Field(foreign_key="eras.id", index=True)
    name: str = Field(max_length=100, index=True)
    code: str = Field(max_length=10, index=True)  # e.g., "MEW", "SVI"
    release_date: Optional[datetime] = None
    
    # Relationships
    era: Era = Relationship(back_populates="sets")
    cards: List["Card"] = Relationship(back_populates="set")


class Rarity(SQLModel, table=True):
    __tablename__ = "rarities"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    code: str = Field(max_length=10, unique=True)  # "C", "U", "R", "RH", "H", "IR", "SIR"
    name: str = Field(max_length=50)  # "Common", "Uncommon", etc.
    
    # Relationships
    cards: List["Card"] = Relationship(back_populates="rarity")


class Card(SQLModel, table=True):
    __tablename__ = "cards"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    set_id: int = Field(foreign_key="sets.id", index=True)
    card_number: str = Field(max_length=10, index=True)
    name: str = Field(max_length=100, index=True)
    rarity_id: int = Field(foreign_key="rarities.id", index=True)
    image_url: Optional[str] = Field(max_length=500, default=None)
    
    # Relationships
    set: Set = Relationship(back_populates="cards")
    rarity: Rarity = Relationship(back_populates="cards")
