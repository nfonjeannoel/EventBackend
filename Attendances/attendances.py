from main import app
from typing import List
import fastapi as _fastapi
import sqlalchemy.orm as _orm
from . import services as _services
from . import schemas as _schemas
from Users import schemas as _user_schemas
from Users import services as _user_services
from Events import services as _event_services


@app.post("/api/create_rsvp", response_model=_schemas.Rsvp)
async def create_attendance(rsvp: _schemas.RsvpCreate, db: _orm.Session = _fastapi.Depends(_services.get_db),
                            current_user: _user_schemas.User = _fastapi.Depends(_user_services.get_current_user)
                            ):
    # check if the event exists
    event = await _event_services.get_event_by_id(db=db, event_id=rsvp.event_id)
    if not event:
        raise _fastapi.HTTPException(status_code=404, detail="Event not found")

    # check if the user has already rsvp'd
    if await _services.get_rsvp_by_user_and_event(db=db, user_id=current_user.id, event_id=rsvp.event_id):
        raise _fastapi.HTTPException(status_code=400, detail="User has already RSVP'd")

    return await _services.create_rsvp(db=db, rsvp=rsvp, user_id=current_user.id)


# get user's rsvp's
@app.get("/api/my_rsvps", response_model=List[_schemas.Rsvp])
async def get_my_rsvps(db: _orm.Session = _fastapi.Depends(_services.get_db),
                       current_user: _user_schemas.User = _fastapi.Depends(_user_services.get_current_user)
                       ):
    return await _services.get_rsvps_by_user(db=db, user_id=current_user.id)
