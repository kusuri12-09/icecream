# GET /api/v1/auth/me

## 설명

현재 로그인한 학부모의 정보를 조회합니다.

## REQUEST

요청 본문은 없습니다. `Authorization: Bearer {accessToken}` 헤더가 필요합니다.

## RESPONSE

상태 코드 `200`

```json
{
  "success": true,
  "data": {
    "id": "parent_a1b2c3",
    "email": "parent@example.com",
    "createdAt": "2026-07-19T10:00:00Z"
  }
}
```

## ERRORCODE

| errorcode | 메시지 | 설명 |
| --- | --- | --- |
| `AUTH_UNAUTHORIZED` | 인증이 필요합니다. | 토큰이 없거나 만료됨, 401 |
