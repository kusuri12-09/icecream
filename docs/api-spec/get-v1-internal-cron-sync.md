# GET /api/v1/internal/cron-sync/{target}

## 설명

Vercel Cron이 호출하는 공공데이터 캐시 동기화 엔드포인트입니다. `centers`와 `activities`를 분리해 한 번의 실행 시간을 줄입니다.

## 인증

Vercel 프로젝트의 `CRON_SECRET` 환경변수와 다음 헤더가 일치해야 합니다.

```http
Authorization: Bearer {CRON_SECRET}
```

## 경로

- `/api/v1/internal/cron-sync/centers`: 체력인증센터 동기화
- `/api/v1/internal/cron-sync/activities`: 운동처방 동영상 동기화

## 응답

```json
{
  "success": true,
  "data": {
    "targets": ["CENTERS"],
    "synced": {"centers": 138, "activities": 0},
    "syncedAt": "2026-07-22T18:00:00+00:00"
  }
}
```

동일한 배치가 실행 중이면 `409 SYNC_IN_PROGRESS`를 반환하며, 인증 실패는 `401`, 환경변수 누락은 `503`으로 처리합니다.
