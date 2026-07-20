# GET /api/v1/children/{childId}

## 설명

로그인한 학부모의 자녀 정보를 단건 조회합니다.

## REQUEST

`Authorization: Bearer {accessToken}` 헤더가 필요합니다. 경로 파라미터 `childId`는 자녀 ID입니다.

## RESPONSE

상태 코드 `200`이며, 자녀 등록 응답과 같은 구조의 `data`를 반환합니다.

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
| `CHILD_ACCESS_DENIED` | 해당 자녀에 접근할 수 없습니다. | 다른 학부모의 자녀에 접근, 403 |
| `CHILD_NOT_FOUND` | 자녀 정보를 찾을 수 없습니다. | 자녀가 존재하지 않음, 404 |
