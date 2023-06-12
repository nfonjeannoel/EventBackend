import datetime as _dt
import pydantic as _pydantic


class _VenueBase(_pydantic.BaseModel):
    location: str
    description: str
    pictures: str
    name: str
    price_per_hour: float
    dimension: str
    capacity: int

    class Config:
        orm_mode = True


class VenueCreate(_VenueBase):
    pass


class Venue(_VenueBase):
    id: int
    date_created: _dt.datetime
    owner_id: int

    class Config:
        orm_mode = True
