import sqlalchemy as _sql
import sqlalchemy.ext.declarative as _declarative
import sqlalchemy.orm as _orm

DATABASE_URL = "sqlite:///./database.db"

engine = _sql.create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = _orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = _declarative.declarative_base()

# Import all models here to ensure they are registered properly on the metadata
from Users.models import User
from Events.models import Event
from Venues.models import Venue
from Attendances.models import Attendance
