from typing import List
import fastapi as _fastapi
import sqlalchemy.orm as _orm
from . import services as _services
from . import schemas as _schemas
from main import app
from Users import schemas as _user_schemas
from .services import _user_services


@app.post("/api/create_event", response_model=_schemas.Event)
async def create_event(event: _schemas.EventCreate, db: _orm.Session = _fastapi.Depends(_services.get_db),
                       current_user: _user_schemas.User = _fastapi.Depends(_user_services.get_current_user)
                       ):
    return await _services.create_event(db=db, event=event, owner_id=current_user.id)


# update event
@app.put("/api/event/{event_id}", response_model=_schemas.Event)
async def update_event(event_id: int, event: _schemas.EventUpdate,
                       db: _orm.Session = _fastapi.Depends(_services.get_db),
                       current_user: _user_schemas.User = _fastapi.Depends(_user_services.get_current_user)
                       ):
    #     update an event only if the user is the owner
    db_event = await _services.get_event_by_id(db=db, event_id=event_id)
    if not db_event:
        raise _fastapi.HTTPException(status_code=404, detail="Event not found")
    if db_event.owner_id != current_user.id:
        raise _fastapi.HTTPException(status_code=403, detail="Not enough permissions")

    return await _services.update_event(db=db, event=event, db_event=db_event)


@app.get("/api/all_events", response_model=List[_schemas.Event])
async def get_all_events(db: _orm.Session = _fastapi.Depends(_services.get_db)):
    return [_schemas.Event.from_orm(event) for event in await _services.get_all_events(db=db)]


# get events by owner
@app.get("/api/events/me", response_model=List[_schemas.Event])
async def get_events_by_owner(db: _orm.Session = _fastapi.Depends(_services.get_db),
                              current_user: _user_schemas.User = _fastapi.Depends(_user_services.get_current_user)
                              ):
    return [_schemas.Event.from_orm(event) for event in
            await _services.get_events_by_owner(db=db, owner_id=current_user.id)]


@app.get("/api/event/{event_id}", response_model=_schemas.Event)
async def get_event_by_id(event_id: int, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    event = await _services.get_event_by_id(db=db, event_id=event_id)
    if not event:
        raise _fastapi.HTTPException(status_code=404, detail="Event not found")
    return event


@app.get("/eventByDate")
async def get_event_by_date(date: str, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    return await _services.get_event_by_date(db=db, date=date)
