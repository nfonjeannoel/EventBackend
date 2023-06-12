import sqlalchemy as _sql
import sqlalchemy.orm as _orm
import datetime as _dt
from database import Base


class Attendance(Base):
    __tablename__ = 'attendance'

    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    user_id = _sql.Column(_sql.Integer, _sql.ForeignKey('users.id'))
    event_id = _sql.Column(_sql.Integer, _sql.ForeignKey('events.id'))
    date_created = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)

    user = _orm.relationship('User', back_populates='attendances')
    event = _orm.relationship('Event', back_populates='attendances')
