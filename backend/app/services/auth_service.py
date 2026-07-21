from sqlalchemy.orm import Session

from app.core.errors import AppError
from app.core.security import create_access_token, hash_password, verify_password
from app.models import Parent
from app.repositories import parent_repository
from app.schemas import AuthData, LoginRequest, SignupRequest


def signup(db: Session, payload: SignupRequest, admin_emails: set[str]) -> AuthData:
    email = str(payload.email).lower()
    if parent_repository.find_by_email(db, email):
        raise AppError("PARENT_ALREADY_EXISTS", "이미 가입된 이메일입니다.", 409)
    parent = parent_repository.save(
        db,
        Parent(email=email, password_hash=hash_password(payload.password), is_admin=email in admin_emails),
    )
    from app.api.common import parent_brief

    return AuthData(parent=parent_brief(parent), access_token=create_access_token(parent.id, parent.is_admin))


def login(db: Session, payload: LoginRequest) -> AuthData:
    parent = parent_repository.find_by_email(db, str(payload.email).lower())
    if parent is None or not verify_password(payload.password, parent.password_hash):
        raise AppError("AUTH_INVALID_CREDENTIALS", "이메일 또는 비밀번호가 올바르지 않습니다.", 401)
    from app.api.common import parent_brief

    return AuthData(parent=parent_brief(parent), access_token=create_access_token(parent.id, parent.is_admin))
