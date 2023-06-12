import datetime as _dt
import pydantic as _pydantic


class _EventBase(_pydantic.BaseModel):
    name: str
    date: _dt.date
    details: str
    start_time: _dt.time | None
    end_time: _dt.time | None

    class Config:
        orm_mode = True


class Event(_EventBase):
    id: int
    date_created: _dt.datetime
    owner_id: int
    venue_id: int | None

    class Config:
        orm_mode = True


class EventCreate(_EventBase):
    pass

    class Config:
        orm_mode = True


class EventUpdate(_EventBase):
    pass

    class Config:
        orm_mode = True
