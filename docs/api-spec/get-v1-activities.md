# GET /api/v1/activities

## 설명

자녀의 약점 체력 요소에 맞는 운동 콘텐츠를 추천합니다. 공공 API(15108846)의 캐시를 조회하며, `measurementId`가 지정되면 해당 측정의 `weaknesses`를 기준으로 필터링합니다.

## REQUEST

`Authorization: Bearer {accessToken}` 헤더가 필요합니다.

| 파라미터 | 설명 |
| --- | --- |
| `fitnessElement` | 대상 체력 요소. 콤마로 여러 요소 지정 가능 |
| `measurementId` | 해당 측정의 약점 요소를 자동 추출하는 대안 조건 |
| `ageGroup` | 연령 그룹. 기본값 `PRESCHOOL` |
| `page`, `size` | 페이지네이션 |

## RESPONSE

상태 코드 `200`

```json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": "video_88",
        "title": "순발력 키우기 점프 놀이",
        "fitnessElement": "POWER",
        "ageGroup": "PRESCHOOL",
        "url": "https://.../video"
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
| `MEASUREMENT_ACCESS_DENIED` | 해당 측정 기록에 접근할 수 없습니다. | 다른 자녀의 측정으로 추천 요청, 403 |
| `MEASUREMENT_NOT_FOUND` | 측정 기록을 찾을 수 없습니다. | 지정한 측정 기록이 존재하지 않음, 404 |
| `EXTERNAL_API_UNAVAILABLE` | 외부 데이터를 일시적으로 사용할 수 없습니다. | 공공 API 장애 및 캐시 데이터 없음, 503 |
| `INVALID_REQUEST_BODY` | 요청 파라미터가 올바르지 않습니다. | 검색 조건 검증 실패, 422 |
