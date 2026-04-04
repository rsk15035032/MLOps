from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
from contextlib import asynccontextmanager

# -------------------------------------------------------------------
# Database Configuration
# -------------------------------------------------------------------

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

# Required for SQLite to allow multi-threaded access
connect_args = {"check_same_thread": False}

# Create database engine
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables() -> None:
    """
    Initialize database and create all tables.

    This function uses SQLModel metadata to create tables
    if they do not already exist.
    """
    SQLModel.metadata.create_all(engine)


def get_session():
    """
    Dependency that provides a database session.

    Yields:
        Session: SQLModel database session

    Ensures:
        - Session is properly opened and closed
        - Safe for use in FastAPI dependency injection
    """
    with Session(engine) as session:
        yield session


# Dependency type alias for cleaner endpoint signatures
SessionDep = Annotated[Session, Depends(get_session)]


# -------------------------------------------------------------------
# Models (Schemas + Database Tables)
# -------------------------------------------------------------------

class HeroBase(SQLModel):
    """
    Base schema for Hero entity.

    Attributes:
        name (str): Name of the hero (indexed for faster search)
        age (Optional[int]): Age of the hero (nullable, indexed)
    """
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)


class Hero(HeroBase, table=True):
    """
    Database model representing the Hero table.

    Inherits:
        HeroBase: Common attributes

    Attributes:
        id (Optional[int]): Primary key
        secret_name (str): Hidden identity of the hero
    """
    id: int | None = Field(default=None, primary_key=True)
    secret_name: str


class HeroPublic(HeroBase):
    """
    Public response schema for Hero.

    Excludes sensitive fields like secret_name.
    """
    id: int


class HeroCreate(HeroBase):
    """
    Schema used when creating a new Hero.

    Includes all required fields for creation.
    """
    secret_name: str


class HeroUpdate(HeroBase):
    """
    Schema used for updating an existing Hero.

    All fields are optional to allow partial updates (PATCH).
    """
    name: str | None = None
    age: int | None = None
    secret_name: str | None = None


# -------------------------------------------------------------------
# Application Startup Event
# -------------------------------------------------------------------


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan handler.

    Runs once at startup and once at shutdown.
    """
    # Startup logic
    create_db_and_tables()
    
    yield  # Application runs here

    # Shutdown logic (optional)
    # e.g., close connections, cleanup resources


# Initialize FastAPI app
app = FastAPI(lifespan=lifespan)


# -------------------------------------------------------------------
# CRUD Endpoints
# -------------------------------------------------------------------

@app.post("/heroes/", response_model=HeroPublic, status_code=201)
def create_hero(hero: HeroCreate, session: SessionDep):
    """
    Create a new hero.

    Args:
        hero (HeroCreate): Input data for hero creation
        session (Session): Database session dependency

    Returns:
        HeroPublic: Created hero (without secret_name)
    """
    db_hero = Hero.model_validate(hero)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero


@app.get("/heroes/", response_model=list[HeroPublic])
def read_heroes(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    """
    Retrieve a list of heroes with pagination.

    Args:
        session (Session): Database session
        offset (int): Number of records to skip
        limit (int): Maximum number of records to return (<=100)

    Returns:
        List[HeroPublic]: List of heroes
    """
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes


@app.get("/heroes/{hero_id}", response_model=HeroPublic)
def read_hero(hero_id: int, session: SessionDep):
    """
    Retrieve a single hero by ID.

    Args:
        hero_id (int): ID of the hero
        session (Session): Database session

    Raises:
        HTTPException: If hero is not found

    Returns:
        HeroPublic: Requested hero
    """
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero


@app.patch("/heroes/{hero_id}", response_model=HeroPublic)
def update_hero(hero_id: int, hero: HeroUpdate, session: SessionDep):
    """
    Update an existing hero (partial update).

    Args:
        hero_id (int): ID of the hero
        hero (HeroUpdate): Fields to update
        session (Session): Database session

    Raises:
        HTTPException: If hero is not found

    Returns:
        HeroPublic: Updated hero
    """
    hero_db = session.get(Hero, hero_id)
    if not hero_db:
        raise HTTPException(status_code=404, detail="Hero not found")

    # Only update fields that were provided in request
    hero_data = hero.model_dump(exclude_unset=True)

    # Apply updates to database object
    hero_db.sqlmodel_update(hero_data)

    session.add(hero_db)
    session.commit()
    session.refresh(hero_db)
    return hero_db


@app.delete("/heroes/{hero_id}", status_code=204)
def delete_hero(hero_id: int, session: SessionDep):
    """
    Delete a hero by ID.

    Args:
        hero_id (int): ID of the hero
        session (Session): Database session

    Raises:
        HTTPException: If hero is not found

    Returns:
        None: No content response (204)
    """
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")

    session.delete(hero)
    session.commit()
    return