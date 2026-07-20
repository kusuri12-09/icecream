# POST /api/v1/children/{childId}/measurements

## 설명

자녀의 측정 세션을 생성하고 즉시 등급을 판정합니다(DIA-01/02/03/04, SLF-01). 서버가 측정 시점의 개월 수를 스냅샷으로 저장하고 기준표 JSON으로 판정합니다.

`type=SELF`이면 `centerId`는 무시되어 `null`로 저장됩니다. `items`는 일부만 입력할 수 있으며, 미입력 항목은 저장·판정에서 제외됩니다.

## REQUEST

`Authorization: Bearer {accessToken}` 헤더가 필요합니다. 경로 파라미터 `childId`는 자녀 ID입니다.

```json
{
  "type": "OFFICIAL",
  "measuredAt": "2026-07-19",
  "centerId": "center_45",
  "items": [
    { "itemKey": "CARDIO", "value": 63 },
    { "itemKey": "GRIP", "value": 53.8 },
    { "itemKey": "MUSCULAR_END", "value": 9 },
    { "itemKey": "FLEXIBILITY", "value": 12 },
    { "itemKey": "AGILITY", "value": 9.46 },
    { "itemKey": "POWER", "value": 105 },
    { "itemKey": "COORDINATION", "value": 23.21 },
    { "itemKey": "BMI", "value": 16.0 }
  ]
}
```

등급은 `FRUIT → FLOWER → SPROUT` 순으로 필수 항목을 모두 충족하는 첫 등급을 부여하며, 미충족 시 `SEED`가 됩니다. 특정 등급의 필수 항목이 입력되지 않으면 `undecidableGrades`에 표시하고 다음 등급을 판정합니다.

## RESPONSE

상태 코드 `201`

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
    "items": [
      { "itemKey": "CARDIO", "label": "심폐지구력", "value": 63, "itemGrade": "FRUIT", "isWeak": false },
      { "itemKey": "POWER", "label": "순발력", "value": 105, "itemGrade": "FRUIT", "isWeak": false }
    ],
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
| `CHILD_NOT_FOUND` | 자녀 정보를 찾을 수 없습니다. | 자녀가 존재하지 않음, 404 |
| `CHILD_ACCESS_DENIED` | 해당 자녀에 접근할 수 없습니다. | 다른 학부모의 자녀에 접근, 403 |
| `CENTER_NOT_FOUND` | 센터를 찾을 수 없습니다. | 지정한 센터가 존재하지 않음, 404 |
| `INVALID_REQUEST_BODY` | 입력값이 올바르지 않습니다. | 요청 본문 검증 실패, 422 |
