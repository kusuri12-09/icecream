# 아이쑥크림 백엔드

FastAPI + SQLAlchemy 기반 API 서버입니다. 운영 환경은 PostgreSQL을 사용하고, 기본 개발 환경은 SQLite를 사용할 수 있습니다.

```powershell
uv sync --group dev
uv run alembic upgrade head
uv run uvicorn app.main:app --reload
uv run pytest
uv run ruff check app tests
uv run mypy app
```

PostgreSQL와 API를 함께 실행하려면 `docker compose up --build`를 사용합니다.

API 문서는 서버 실행 후 `http://localhost:8000/docs`에서 확인합니다.
