from fastapi import APIRouter

from app.api.common import DbDep, ParentDep, dump, parent_brief, success
from app.core.config import get_settings
from app.schemas import LoginRequest, ParentOut, SignupRequest
from app.services import auth_service


router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.post("/signup", status_code=201)
def signup(payload: SignupRequest, db: DbDep) -> dict:
    result = auth_service.signup(db, payload, get_settings().admin_email_set)
    return success(dump(result))


@router.post("/login")
def login(payload: LoginRequest, db: DbDep) -> dict:
    return success(dump(auth_service.login(db, payload)))


@router.get("/me")
def me(parent: ParentDep) -> dict:
    result = ParentOut(id=parent_brief(parent).id, email=parent.email, created_at=parent.created_at)
    return success(dump(result))
