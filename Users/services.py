import jwt as _jwt
import sqlalchemy.orm as _orm
import passlib.hash as _hash
import email_validator as _email_check
import fastapi as _fastapi
import fastapi.security as _security

from . import schemas as _schemas
from . import models as _models
from database import get_db

_JWT_SECRET = "eventmanagementbackend"
oauth2_scheme = _security.OAuth2PasswordBearer(tokenUrl="/api/token")


async def get_user_by_email(db: _orm.Session, email: str):
    return db.query(_models.User).filter(_models.User.email == email).first()


async def create_user(db: _orm.Session, user: _schemas.UserCreate):
    try:
        valid_email = _email_check.validate_email(email=user.email)
        email = valid_email.email
    except _email_check.EmailNotValidError as e:
        raise _fastapi.HTTPException(status_code=400, detail=str(e))

    user_obj = _models.User(email=email, hashed_password=_hash.bcrypt.hash(user.password), full_name=user.full_name)
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj


async def create_token(user: _models.User):
    user_obj = _schemas.User.from_orm(user)
    user_dict = user_obj.dict()
    del user_dict["date_created"]
    token = _jwt.encode(user_dict, _JWT_SECRET)
    return _schemas.AccessToken(access_token=token, token_type="bearer")


async def authenticate_user(email: str, password: str, db: _orm.Session):
    user = await get_user_by_email(db=db, email=email)
    if not user:
        return False
    if not user.verify_password(password):
        return False
    return user


async def get_current_user(db: _orm.Session = _fastapi.Depends(get_db),
                           token: str = _fastapi.Depends(oauth2_scheme)):
    try:
        payload = _jwt.decode(token, _JWT_SECRET, algorithms=["HS256"])
        user = db.get(_models.User, payload["id"])
    except _fastapi.HTTPException:
        raise _fastapi.HTTPException(status_code=401, detail="Invalid Email or Password")

    return _schemas.User.from_orm(user)


async def get_users(db: _orm.Session, skip: int = 0, limit: int = 100):
    return db.query(_models.User).offset(skip).limit(limit).all()
