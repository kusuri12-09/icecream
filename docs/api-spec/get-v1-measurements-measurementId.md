# GET /api/v1/measurements/{measurementId}

## 설명

측정 기록을 단건 상세 조회합니다(REC-01).

## REQUEST

`Authorization: Bearer {accessToken}` 헤더가 필요합니다. 경로 파라미터 `measurementId`는 측정 ID입니다.

## RESPONSE

상태 코드 `200`이며, 측정 생성 응답과 동일한 구조의 `data`를 반환합니다.

```json
{
  "success": true,
  "data": {
    "id": "measurement_4567",
    "childId": "child_123",
    "type": "OFFICIAL",
    "measuredAt": "2026-07-19",
    "ageMonthsAtMeasure": 62,
    "grade": "FRUIT",
    "center": { "id": "center_45", "name": "OO체력인증센터" },
    "items": [],
    "profile": {
      "strengths": ["CARDIO", "POWER"],
      "weaknesses": [],
      "undecidableGrades": []
    },
    "createdAt": "2026-07-19T10:00:00Z"
  }
}
```

## ERRORCODE

| errorcode | 메시지 | 설명 |
| --- | --- | --- |
| `AUTH_UNAUTHORIZED` | 인증이 필요합니다. | 토큰이 없거나 만료됨, 401 |
| `MEASUREMENT_ACCESS_DENIED` | 해당 측정 기록에 접근할 수 없습니다. | 다른 자녀의 측정에 접근, 403 |
| `MEASUREMENT_NOT_FOUND` | 측정 기록을 찾을 수 없습니다. | 측정 기록이 존재하지 않음, 404 |
