# DELETE /api/v1/children/{childId}

## 설명

자녀를 삭제합니다. 해당 자녀의 측정 기록도 CASCADE로 삭제됩니다.

## REQUEST

`Authorization: Bearer {accessToken}` 헤더가 필요합니다. 경로 파라미터 `childId`는 자녀 ID입니다.

## RESPONSE

상태 코드 `200`

```json
{
  "success": true,
  "data": {
    "id": "child_123",
    "deleted": true
  }
}
```

## ERRORCODE

| errorcode | 메시지 | 설명 |
| --- | --- | --- |
| `AUTH_UNAUTHORIZED` | 인증이 필요합니다. | 토큰이 없거나 만료됨, 401 |
| `CHILD_ACCESS_DENIED` | 해당 자녀에 접근할 수 없습니다. | 다른 학부모의 자녀에 접근, 403 |
| `CHILD_NOT_FOUND` | 자녀 정보를 찾을 수 없습니다. | 자녀가 존재하지 않음, 404 |
