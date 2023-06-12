import datetime as _dt
import pydantic as _pydantic


class _BaseRsvp(_pydantic.BaseModel):
    event_id: int

    class Config:
        orm_mode = True


class RsvpCreate(_BaseRsvp):
    pass


class Rsvp(_BaseRsvp):
    id: int
    user_id: int
    event_id: int
    date_created: _dt.datetime

    class Config:
        orm_mode = True
