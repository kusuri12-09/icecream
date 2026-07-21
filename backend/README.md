# 아이쑥크림 백엔드

FastAPI + SQLAlchemy 기반 API 서버입니다. PostgreSQL을 기본 데이터베이스로 사용하며, 테스트에서는 SQLite를 사용합니다.

PostgreSQL 접속 정보는 `.env`의 `DB_HOST`, `DB_PORT`, `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`로 설정합니다. `DATABASE_URL`을 지정하면 해당 URL을 우선 사용하므로, 개별 DB 변수를 사용하려면 `DATABASE_URL`을 제거하거나 주석 처리합니다. 애플리케이션과 Docker Compose가 같은 `POSTGRES_*` 변수를 함께 사용합니다.

```powershell
uv sync --group dev
uv run alembic upgrade head
uv run uvicorn app.main:app --reload
uv run pytest
uv run ruff check app tests
uv run mypy app
```

로컬 PostgreSQL에 직접 연결할 때는 `DB_HOST=localhost`를 사용하고, PostgreSQL과 API를 Compose로 함께 실행할 때는 컨테이너 간 접속을 위해 `DB_HOST=postgres`로 설정한 뒤 `docker compose up --build`를 사용합니다.

API 문서는 서버 실행 후 `http://localhost:8000/docs`에서 확인합니다.
