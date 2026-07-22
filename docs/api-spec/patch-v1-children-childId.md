# PATCH /api/v1/children/{childId}

## 설명

자녀의 `nickname`, `gender`, `birthYearMonth`를 부분 수정합니다. `birthYearMonth`는 2019년 1월부터 현재 연도 전년 12월까지만 허용합니다.

## REQUEST

`Authorization: Bearer {accessToken}` 헤더가 필요합니다. 경로 파라미터 `childId`는 자녀 ID입니다.

```json
{
  "nickname": "콩콩이",
  "gender": "MALE",
  "birthYearMonth": "2021-05"
}
```

수정할 필드만 보낼 수 있습니다.

## RESPONSE

상태 코드 `200`

```json
{
  "success": true,
  "data": {
    "id": "child_123",
    "nickname": "콩콩이",
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
| `CHILD_ACCESS_DENIED` | 해당 자녀에 접근할 수 없습니다. | 다른 학부모의 자녀에 접근, 403 |
| `CHILD_NOT_FOUND` | 자녀 정보를 찾을 수 없습니다. | 자녀가 존재하지 않음, 404 |
| `INVALID_REQUEST_BODY` | 입력값이 올바르지 않습니다. | 요청 본문 검증 실패, 422 |
