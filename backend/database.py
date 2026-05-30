
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# load the variables in the environement
load_dotenv()
# create the base
Base = declarative_base()

# create the db through my terminal -- C:\ProgramData\Microsoft\Windows\Start Menu\Programs\PostgreSQL 18\

# create the db connection
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL not in .env")

engine = create_engine(DATABASE_URL

                       )

# create the session

SessionLocal = sessionmaker(bind=engine,
                            autoflush=False,
                            autocommit=False)

# testing if connection to db is wired -- uv run python -c "from database import engine; conn = engine.connect(); print('connected'); conn.close()"


def get_db():
    """FastAPI dependency that provides a database session per request.

    Opens a new SQLAlchemy session, yields it to the route handler,
    then closes it when the request finishes : whether it succeeded or raised.

    Usage:
        @router.get("/example")
        def example(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
