# 배포 절차

## Vercel 백엔드

Vercel 프로젝트의 Root Directory를 `backend`로 설정한다. FastAPI 진입점은 `backend/index.py`의 `app` 객체이며, Python 버전은 `backend/pyproject.toml`의 `requires-python`에 맞춰 3.12를 사용한다.

Vercel 설정값은 다음과 같다.

- Install Command: 비워 둔다. `pyproject.toml`과 `uv.lock`을 기준으로 의존성을 자동 설치한다.
- Build Command: 비워 둔다. FastAPI는 별도 정적 빌드 산출물이 없다.
- Output Directory: 비워 둔다. Python Function으로 배포한다.

### 환경변수

Vercel Production 환경에 다음 값을 등록한다.

- `DATABASE_URL`: Neon PostgreSQL URL. `sslmode=require` 포함
- `JWT_SECRET_KEY`: 운영용 무작위 시크릿
- `ADMIN_EMAILS`: 관리자 이메일 목록
- `KSPO_API_KEY`: 공공데이터포털 서비스키
- `KSPO_CENTER_URL`: 센터 API 엔드포인트 전체 URL
- `KSPO_ACTIVITY_URL`: `TODZ_VDO_TRNG_GUIDE_I` 엔드포인트 전체 URL
- `CRON_SECRET`: Vercel Cron Authorization 검증용 무작위 시크릿

## 데이터베이스 마이그레이션

배포 전에 Neon 연결 문자열을 사용해 마이그레이션을 실행한다.

```powershell
cd backend
$env:DATABASE_URL = 'Neon 연결 문자열'
uv run alembic upgrade head
```

애플리케이션 시작 시 `Base.metadata.create_all`은 개발 편의를 위해 유지하지만, 운영 스키마 변경은 반드시 Alembic으로 적용한다.

## Vercel Cron

`backend/vercel.json`에 센터와 활동 동기화를 매일 한국시간 03:00, 03:30에 실행하도록 등록했다. Vercel Cron 스케줄은 UTC 기준이다.

- `/api/v1/internal/cron-sync/centers`
- `/api/v1/internal/cron-sync/activities`

Production 배포 후 Vercel Cron 실행 이력, `CRON_SECRET` 인증, 중복 실행 응답, 외부 API 실패·재시도 로그를 확인한다.
