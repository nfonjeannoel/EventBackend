import sqlalchemy as _sql
import sqlalchemy.orm as _orm
import datetime as _dt
from database import Base
import passlib.hash as _hash


class User(Base):
    __tablename__ = 'users'

    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    email = _sql.Column(_sql.String, unique=True, index=True)
    hashed_password = _sql.Column(_sql.String)
    full_name = _sql.Column(_sql.String)
    date_created = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)

    def verify_password(self, password: str):
        return _hash.bcrypt.verify(password, self.hashed_password)

    events = _orm.relationship('Event', back_populates='owner')
    attendances = _orm.relationship('Attendance', back_populates='user')
