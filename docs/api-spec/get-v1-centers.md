# GET /api/v1/centers

## 설명

근처 또는 지역 기준으로 체력인증센터를 검색합니다. 공공 API(15114286)의 캐시를 조회하며, 외부 장애 시 캐시 데이터가 있으면 `stale: true`로 반환합니다. 캐시도 없으면 오류를 반환합니다.

## REQUEST

`Authorization: Bearer {accessToken}` 헤더가 필요합니다.

| 파라미터 | 설명 |
| --- | --- |
| `lat`, `lng`, `radiusKm` | 좌표 기반 근처 검색(거리순) |
| `sido` | 시·도 단위 지역 필터(예: `경기도`) |
| `sidoSigungu` | 시·도·시군구 단위 지역 필터 |
| `page`, `size` | 페이지네이션 |

## RESPONSE

상태 코드 `200`

```json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": "center_45",
        "name": "OO체력인증센터",
        "address": "서울 OO구 ...",
        "sido": "서울특별시",
        "sidoSigungu": "서울 OO구",
        "latitude": 37.5,
        "longitude": 127.0,
        "distanceKm": 1.2,
        "reservationUrl": "https://nfa.kspo.or.kr/reserve/...",
        "stale": false
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
| `CENTER_NOT_FOUND` | 체력인증센터를 찾을 수 없습니다. | 조건에 맞는 센터 캐시 데이터가 없음, 404 |
| `INVALID_REQUEST_BODY` | 요청 파라미터가 올바르지 않습니다. | 검색 조건 검증 실패, 422 |
