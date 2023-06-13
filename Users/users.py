from typing import List
import fastapi as _fastapi
import fastapi.security as _security

import sqlalchemy.orm as _orm

from . import services as _services
from . import schemas as _schemas
from fastapi import APIRouter

router = APIRouter()


@router.post("/api/create_user", response_model=_schemas.AccessToken)
async def create_user(user: _schemas.UserCreate, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    db_user = await _services.get_user_by_email(db, email=user.email)
    if db_user:
        raise _fastapi.HTTPException(status_code=400, detail="Email already registered")

    user = await _services.create_user(db=db, user=user)
    return await _services.create_token(user=user)


@router.post("/api/token", response_model=_schemas.AccessToken)
async def login(form_data: _security.OAuth2PasswordRequestForm = _fastapi.Depends(),
                db: _orm.Session = _fastapi.Depends(_services.get_db)):
    """
       Retrieve an access token.

       Parameters:
       - username: The user's email address is expected (Ignore field name).
       - password: The user's password.

       Returns:
       - access_token: The generated access token.
       - token_type: The token type.
       """
    user = await _services.authenticate_user(email=form_data.username, password=form_data.password, db=db)
    if not user:
        raise _fastapi.HTTPException(status_code=401, detail="Invalid Credentials")

    return await _services.create_token(user=user)


@router.get("/api/users", response_model=List[_schemas.User])
async def read_users(skip: int = 0, limit: int = 100, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    users = await _services.get_users(db=db, skip=skip, limit=limit)
    return users


@router.get("/api/users/me", response_model=_schemas.User)
async def read_users_me(current_user: _schemas.User = _fastapi.Depends(_services.get_current_user)):
    return current_user
