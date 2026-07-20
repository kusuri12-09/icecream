# GET /api/v1/insights/regional/map

## 설명

시군구별 참여율 지도와 랭킹 데이터를 조회합니다(INS-02, P1). 데이터가 없으면 `fallback: true`를 반환하며, 클라이언트는 지역 통찰 카드(INS-01)로 축소해 표시합니다.

## REQUEST

`Authorization: Bearer {accessToken}` 헤더가 필요합니다. 별도 요청 파라미터와 본문은 없습니다.

## RESPONSE

상태 코드 `200`

```json
{
  "success": true,
  "data": {
    "regions": [
      {
        "sidoSigungu": "서울 OO구",
        "measureCount": 152,
        "participationRate": 0.42
      }
    ],
    "fallback": false
  }
}
```

## ERRORCODE

| errorcode | 메시지 | 설명 |
| --- | --- | --- |
| `AUTH_UNAUTHORIZED` | 인증이 필요합니다. | 토큰이 없거나 만료됨, 401 |
