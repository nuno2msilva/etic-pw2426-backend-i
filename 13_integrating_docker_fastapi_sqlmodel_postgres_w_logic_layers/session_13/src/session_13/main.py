from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import SQLModel, Field, create_engine, Session, select
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI()

# Define a sample model for an item
class Item(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    description: str = None

# Database connection string using Postgres container (host 'db' will be defined in docker-compose)
DATABASE_URL = "postgresql://postgres:password@db:5432/postgres"
engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

# ----- Logic Layer (Business Logic) -----

def create_item_logic(session: Session, item: Item) -> Item:
    logger.info("Creating a new item in the database")
    session.add(item)
    session.commit()
    session.refresh(item)
    return item

def update_item_logic(session: Session, item_id: int, new_item: Item) -> Item:
    logger.info(f"Updating item with id {item_id}")
    statement = select(Item).where(Item.id == item_id)
    existing_item = session.exec(statement).one_or_none()
    if not existing_item:
        raise HTTPException(status_code=404, detail="Item not found")
    existing_item.name = new_item.name
    existing_item.description = new_item.description
    session.add(existing_item)
    session.commit()
    session.refresh(existing_item)
    return existing_item

def delete_item_logic(session: Session, item_id: int) -> dict:
    logger.info(f"Deleting item with id {item_id}")
    statement = select(Item).where(Item.id == item_id)
    item = session.exec(statement).one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    session.delete(item)
    session.commit()
    return {"message": f"Item {item_id} deleted successfully"}

# ----- API Endpoints -----

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)
    logger.info("Database tables created")

@app.post("/items/", response_model=Item)
def create_item(item: Item, session: Session = Depends(get_session)):
    return create_item_logic(session, item)

@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int, session: Session = Depends(get_session)):
    statement = select(Item).where(Item.id == item_id)
    result = session.exec(statement)
    item = result.one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item: Item, session: Session = Depends(get_session)):
    return update_item_logic(session, item_id, item)

@app.delete("/items/{item_id}")
def delete_item(item_id: int, session: Session = Depends(get_session)):
    return delete_item_logic(session, item_id)