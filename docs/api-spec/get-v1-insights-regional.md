# GET /api/v1/insights/regional

## 설명

우리 동네의 유아 체력측정 참여 현황과 전국 평균 대비 수준을 조회합니다(INS-01). `center`의 `sidoSigungu`별 측정 횟수를 집계하며, 표본이 부족하면 참여 유도 메시지를 반환합니다.

## REQUEST

`Authorization: Bearer {accessToken}` 헤더가 필요합니다.

Query: `?sidoSigungu=서울 OO구`

생략하면 기본 지역 또는 전국을 기준으로 조회합니다.

## RESPONSE

상태 코드 `200`

```json
{
  "success": true,
  "data": {
    "region": "서울 OO구",
    "regionMeasureCount": 152,
    "nationalAvg": 320,
    "relativeLevel": "BELOW_AVG",
    "percentile": 28,
    "message": "OO구의 유아 체력측정 참여는 전국 평균보다 낮은 편이에요. 가까운 센터에서 무료로 측정해보세요.",
    "cta": { "type": "CENTER_CONNECT", "label": "근처 센터 찾기" }
  }
}
```

`relativeLevel`은 `ABOVE_AVG | AROUND_AVG | BELOW_AVG | INSUFFICIENT` 중 하나입니다.

## ERRORCODE

| errorcode | 메시지 | 설명 |
| --- | --- | --- |
| `AUTH_UNAUTHORIZED` | 인증이 필요합니다. | 토큰이 없거나 만료됨, 401 |
| `INVALID_REQUEST_BODY` | 요청 파라미터가 올바르지 않습니다. | 지역 조건 검증 실패, 422 |
