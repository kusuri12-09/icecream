# POST /api/v1/children

## 설명

로그인한 학부모에게 자녀를 등록합니다. `birthYearMonth`는 유아 대상 서비스 정책에 따라 2019년 1월부터 현재 연도 전년 12월까지만 허용합니다. `ageMonths`는 현재 시점에 계산되며, 48~83개월 밖이면 `inTargetRange`가 `false`가 됩니다.

## REQUEST

`Authorization: Bearer {accessToken}` 헤더가 필요합니다.

```json
{
  "nickname": "콩이",
  "gender": "MALE",
  "birthYearMonth": "2021-05"
}
```

## RESPONSE

상태 코드 `201`

```json
{
  "success": true,
  "data": {
    "id": "child_123",
    "nickname": "콩이",
    "gender": "MALE",
    "birthYearMonth": "2021-05",
    "ageMonths": 62,
    "inTargetRange": true,
    "createdAt": "2026-07-19T10:00:00Z"
  }
}
```

## ERRORCODE

| errorcode | 메시지 | 설명 |
| --- | --- | --- |
| `AUTH_UNAUTHORIZED` | 인증이 필요합니다. | 토큰이 없거나 만료됨, 401 |
| `INVALID_REQUEST_BODY` | 입력값이 올바르지 않습니다. | 요청 본문 검증 실패, 422 |
