import sqlalchemy as _sql
import datetime as _dt
from database import Base


class Venue(Base):
    __tablename__ = 'venues'

    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    location = _sql.Column(_sql.String)
    description = _sql.Column(_sql.String)
    pictures = _sql.Column(_sql.String)
    name = _sql.Column(_sql.String)
    price_per_hour = _sql.Column(_sql.Float)
    dimension = _sql.Column(_sql.String)
    capacity = _sql.Column(_sql.Integer)
    date_created = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)

    owner_id = _sql.Column(_sql.Integer, _sql.ForeignKey('users.id'))
