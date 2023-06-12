import fastapi as _fastapi
import database as _database

app = _fastapi.FastAPI()


@app.get("/")
async def read_root():
    return {"msg": "Event Manager API. See /docs for more info. see /redoc for more info."}


def get_db():
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Files needed to be imported so that the endpoints are registered
# ************* User *************
import Users.users as _users
# ************* Event *************
import Events.events as _events
# ************* Venue *************
import Venues.venues as _venues
# ************* Attendance *************
import Attendances.attendances as _attendances
