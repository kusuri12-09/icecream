# GET /api/v1/children

## 설명

로그인한 학부모가 등록한 자녀 목록을 조회합니다.

## REQUEST

`Authorization: Bearer {accessToken}` 헤더가 필요합니다. 별도 요청 파라미터와 본문은 없습니다.

## RESPONSE

상태 코드 `200`

```json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": "child_123",
        "nickname": "콩이",
        "gender": "MALE",
        "ageMonths": 62,
        "inTargetRange": true
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
