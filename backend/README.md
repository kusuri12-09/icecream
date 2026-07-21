# 아이쑥크림 백엔드

FastAPI + SQLAlchemy 기반 API 서버입니다. PostgreSQL을 기본 데이터베이스로 사용하며, 테스트에서는 SQLite를 사용합니다.

로컬 PostgreSQL 접속 정보는 `.env`의 `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`로 설정합니다. `DATABASE_URL`을 지정하면 해당 URL을 우선 사용하므로, 개별 DB 변수를 사용하려면 `DATABASE_URL`을 제거하거나 주석 처리합니다.

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
