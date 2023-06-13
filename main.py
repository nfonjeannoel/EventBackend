import fastapi as _fastapi
import database as _database
from Events.events import router as _events_router
from Users.users import router as _users_router
from Venues.venues import router as _venues_router
from Attendances.attendances import router as _attendances_router

app = _fastapi.FastAPI()

app.include_router(_events_router, tags=["Events"])
app.include_router(_users_router, tags=["Users"])
app.include_router(_venues_router, tags=["Venues"])
app.include_router(_attendances_router, tags=["Attendances"])


@app.get("/")
async def read_root():
    return {"msg": "Event Manager API. See /docs for more info. see /redoc for more info."}

# # Files needed to be imported so that the endpoints are registered
# # ************* User *************
# import Users.users as _users
# # ************* Event *************
# import Events.events as _events
# # ************* Venue *************
# import Venues.venues as _venues
# # ************* Attendance *************
# import Attendances.attendances as _attendances
