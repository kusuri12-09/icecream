# GET /api/v1/children/{childId}/growth

## 설명

자녀의 성장 추이를 조회합니다(REC-02). 서버는 정식 측정과 자가 측정을 구분할 수 있도록 각 시계열 데이터에 `type`을 포함합니다. 실선·점선 렌더링은 클라이언트가 처리합니다.

## REQUEST

`Authorization: Bearer {accessToken}` 헤더가 필요합니다. 경로 파라미터 `childId`는 자녀 ID입니다.

Query: `?itemKey=CARDIO`

`itemKey`는 선택 사항이며, 생략하면 전체 항목을 반환합니다.

## RESPONSE

상태 코드 `200`

```json
{
  "success": true,
  "data": {
    "childId": "child_123",
    "series": [
      {
        "itemKey": "CARDIO",
        "label": "심폐지구력",
        "unit": "회",
        "points": [
          { "measuredAt": "2026-01-10", "value": 40, "type": "SELF" },
          { "measuredAt": "2026-04-15", "value": 55, "type": "OFFICIAL" }
        ]
      }
    ],
    "gradeHistory": [
      { "measuredAt": "2026-04-15", "grade": "FLOWER" }
    ]
  }
}
```

## ERRORCODE

| errorcode | 메시지 | 설명 |
| --- | --- | --- |
| `AUTH_UNAUTHORIZED` | 인증이 필요합니다. | 토큰이 없거나 만료됨, 401 |
| `CHILD_ACCESS_DENIED` | 해당 자녀에 접근할 수 없습니다. | 다른 학부모의 자녀에 접근, 403 |
| `CHILD_NOT_FOUND` | 자녀 정보를 찾을 수 없습니다. | 자녀가 존재하지 않음, 404 |
| `INVALID_REQUEST_BODY` | 요청 파라미터가 올바르지 않습니다. | `itemKey` 검증 실패, 422 |
