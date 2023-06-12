import sqlalchemy as _sql
import sqlalchemy.orm as _orm
import datetime as _dt
from database import Base

class Event(Base):
    __tablename__ = 'events'

    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    name = _sql.Column(_sql.String)
    date = _sql.Column(_sql.Date)
    details = _sql.Column(_sql.String)
    start_time = _sql.Column(_sql.Time)
    end_time = _sql.Column(_sql.Time)
    date_created = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)

    owner_id = _sql.Column(_sql.Integer, _sql.ForeignKey('users.id'))
    venue_id = _sql.Column(_sql.Integer, _sql.ForeignKey('venues.id'))

    owner = _orm.relationship('User', back_populates='events')
    venue = _orm.relationship('Venue')
    attendances = _orm.relationship('Attendance', back_populates='event')
