from app.core.errors import AppError


def encode_id(resource: str, value: int | str) -> str:
    return f"{resource}_{value}"


def decode_id(value: str, resource: str) -> int:
    prefix = f"{resource}_"
    if not value.startswith(prefix):
        raise AppError("INVALID_REQUEST_BODY", "리소스 ID 형식이 올바르지 않습니다.", 422)
    try:
        return int(value[len(prefix) :])
    except ValueError as exc:
        raise AppError("INVALID_REQUEST_BODY", "리소스 ID 형식이 올바르지 않습니다.", 422) from exc
