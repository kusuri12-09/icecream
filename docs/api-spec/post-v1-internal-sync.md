# POST /api/v1/internal/sync

## 설명

공공데이터 배치 동기화를 수동으로 트리거합니다(SYNC-01). 관리자 인증이 필요하며, `extId` 기준으로 upsert하고 센터 주소에서 `sidoSigungu`를 파싱합니다. 기준표 JSON은 동기화 대상이 아니며 앱 기동 시 로드합니다.

`page_size`를 생략하면 외부 API를 페이지당 100개씩 조회합니다. 활동 데이터처럼 원본 행이 많은 경우 `page`를 지정하면 해당 활동 API 페이지만 처리하고 즉시 커밋할 수 있습니다. 페이지 단위 동기화는 `targets: ["ACTIVITIES"]`에서만 지원합니다.

## REQUEST

관리자 권한이 있는 `Authorization: Bearer {accessToken}` 헤더가 필요합니다.

| 쿼리 파라미터 | 설명 |
| --- | --- |
| `page_size` | 외부 API 페이지 크기, 기본 100·최대 1000 |
| `page` | 활동 데이터 처리 페이지. 지정 시 해당 페이지만 저장 |

```json
{
  "targets": ["CENTERS", "ACTIVITIES"]
}
```

## RESPONSE

상태 코드 `200`

```json
{
  "success": true,
  "data": {
    "synced": {
      "centers": 75,
      "activities": 210
    },
    "pageSize": 100,
    "syncedAt": "2026-07-19T03:00:00Z"
  }
}
```

## ERRORCODE

| errorcode | 메시지 | 설명 |
| --- | --- | --- |
| `AUTH_UNAUTHORIZED` | 인증이 필요합니다. | 토큰이 없거나 관리자 인증이 되지 않음, 401 |
| `EXTERNAL_API_UNAVAILABLE` | 외부 데이터를 일시적으로 사용할 수 없습니다. | 공공 API 장애, 503 |
| `INVALID_REQUEST_BODY` | 입력값이 올바르지 않습니다. | 요청 본문 검증 실패, 422 |
| `SYNC_IN_PROGRESS` | 동기화가 이미 실행 중입니다. | 다른 동기화가 실행 중임, 409 |
