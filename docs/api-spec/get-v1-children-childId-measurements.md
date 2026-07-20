# GET /api/v1/children/{childId}/measurements

## 설명

자녀의 측정 기록 목록을 조회합니다(REC-01).

## REQUEST

`Authorization: Bearer {accessToken}` 헤더가 필요합니다. 경로 파라미터 `childId`는 자녀 ID입니다.

Query: `?type=OFFICIAL&page=1&size=20&sort=measuredAt,desc`

`page`는 1부터 시작하고, `size`의 기본값은 20, 최대값은 100입니다.

## RESPONSE

상태 코드 `200`

```json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": "measurement_4567",
        "type": "OFFICIAL",
        "measuredAt": "2026-07-19",
        "grade": "FRUIT"
      }
    ],
    "page": 1,
    "size": 20,
    "totalElements": 1,
    "totalPages": 1
  }
}
```

## ERRORCODE

| errorcode | 메시지 | 설명 |
| --- | --- | --- |
| `AUTH_UNAUTHORIZED` | 인증이 필요합니다. | 토큰이 없거나 만료됨, 401 |
| `CHILD_ACCESS_DENIED` | 해당 자녀에 접근할 수 없습니다. | 다른 학부모의 자녀에 접근, 403 |
| `CHILD_NOT_FOUND` | 자녀 정보를 찾을 수 없습니다. | 자녀가 존재하지 않음, 404 |
| `INVALID_REQUEST_BODY` | 요청 파라미터가 올바르지 않습니다. | 조회 조건 검증 실패, 422 |
