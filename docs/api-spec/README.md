# API Specification

## API 요약

| 메서드 | 경로 | 기능 | 인증 | 우선순위 | 문서 |
| --- | --- | --- | --- | --- | --- |
| POST | `/api/v1/auth/signup` | 가입 | - | P0 | [상세](./post-v1-auth-signup.md) |
| POST | `/api/v1/auth/login` | 로그인 | - | P0 | [상세](./post-v1-auth-login.md) |
| GET | `/api/v1/auth/me` | 내 정보 | 🔒 | P0 | [상세](./get-v1-auth-me.md) |
| POST | `/api/v1/children` | 자녀 등록 | 🔒 | P0 | [상세](./post-v1-children.md) |
| GET | `/api/v1/children` | 자녀 목록 | 🔒 | P0 | [상세](./get-v1-children.md) |
| GET | `/api/v1/children/{childId}` | 자녀 조회 | 🔒 | P0 | [상세](./get-v1-children-childId.md) |
| PATCH | `/api/v1/children/{childId}` | 자녀 수정 | 🔒 | P0 | [상세](./patch-v1-children-childId.md) |
| DELETE | `/api/v1/children/{childId}` | 자녀 삭제 | 🔒 | P1 | [상세](./delete-v1-children-childId.md) |
| POST | `/api/v1/children/{childId}/measurements` | 측정 및 판정 | 🔒 | P0 | [상세](./post-v1-children-childId-measurements.md) |
| GET | `/api/v1/children/{childId}/measurements` | 측정 기록 목록 | 🔒 | P0 | [상세](./get-v1-children-childId-measurements.md) |
| GET | `/api/v1/measurements/{measurementId}` | 측정 상세 | 🔒 | P0 | [상세](./get-v1-measurements-measurementId.md) |
| DELETE | `/api/v1/measurements/{measurementId}` | 측정 삭제 | 🔒 | P1 | [상세](./delete-v1-measurements-measurementId.md) |
| GET | `/api/v1/children/{childId}/growth` | 성장 추이 | 🔒 | P0 | [상세](./get-v1-children-childId-growth.md) |
| GET | `/api/v1/centers` | 센터 검색 | 🔒 | P0 | [상세](./get-v1-centers.md) |
| GET | `/api/v1/activities` | 활동 추천 | 🔒 | P0 | [상세](./get-v1-activities.md) |
| GET | `/api/v1/insights/regional` | 지역 통찰 카드 | 🔒 | P0 | [상세](./get-v1-insights-regional.md) |
| GET | `/api/v1/insights/regional/map` | 지역 지도 및 랭킹 | 🔒 | P1 | [상세](./get-v1-insights-regional-map.md) |
| POST | `/api/v1/internal/sync` | 데이터 동기화 | 🔒 관리자 | P0(운영) | [상세](./post-v1-internal-sync.md) |

---

## 공통 규약

### Base URL

```text
/api/v1
```

### 공통 요청 헤더

```text
Content-Type: application/json
Authorization: Bearer {accessToken}
Trace-Id: {traceId}
```

`Authorization`은 인증이 필요한 API에서만 사용합니다.

### 인증

- 인증 필요 API는 `Authorization: Bearer {accessToken}`을 요구합니다.
- 인증 주체(`parentId`)는 토큰에서 추출하며, 클라이언트가 보낸 사용자 ID는 신뢰하지 않습니다.
- 미인증 또는 만료 시 `AUTH_UNAUTHORIZED`(401)를 반환합니다.
- 다른 사용자의 리소스에 접근하면 해당 리소스의 `*_ACCESS_DENIED`(403)를 반환합니다.
- 외부 운영 API인 `/internal/sync`는 관리자 권한이 필요합니다.

### 리소스 ID 접두사

| 리소스 | 접두사 |
| --- | --- |
| Parent | `parent_` |
| Child | `child_` |
| Measurement | `measurement_` |
| Center | `center_` |
| ActivityVideo | `video_` |

외부 노출 ID는 DB Auto Increment를 그대로 사용하지 않고 접두사를 붙여 반환합니다. `parent`는 필요할 때 UUID `publicId`를 사용할 수 있습니다.

### 공통 응답 형식

성공 응답은 `success`와 `data`로 래핑합니다.

단건:

```json
{
  "success": true,
  "data": { "id": "child_123", "nickname": "콩이" }
}
```

목록:

```json
{
  "success": true,
  "data": {
    "items": [],
    "page": 1,
    "size": 20,
    "totalElements": 100,
    "totalPages": 5
  }
}
```

실패 응답은 `success`와 `error`로 래핑하고 `timestamp`를 포함합니다.

```json
{
  "success": false,
  "error": {
    "code": "CHILD_NOT_FOUND",
    "message": "자녀 정보를 찾을 수 없습니다.",
    "status": 404
  },
  "timestamp": "2026-07-19T10:00:00Z"
}
```

요청·응답 필드는 camelCase이며, 시간은 UTC ISO-8601 형식을 사용합니다.

### 페이지네이션 및 정렬

- `page`는 1부터 시작합니다.
- `size` 기본값은 20, 최대값은 100입니다.
- 정렬은 `sort={field},{direction}` 형식을 사용합니다. 예: `sort=measuredAt,desc`

### 공통 Enum

| Enum | 값 |
| --- | --- |
| `gender` | `MALE`, `FEMALE` |
| `measurementType` | `OFFICIAL`, `SELF` |
| `grade` | `SEED`, `SPROUT`, `FLOWER`, `FRUIT` |
| `itemKey` | `CARDIO`, `GRIP`, `MUSCULAR_END`, `FLEXIBILITY`, `AGILITY`, `POWER`, `COORDINATION`, `BMI` |
| `fitnessElement` | `CARDIO`, `GRIP`, `MUSCULAR_END`, `FLEXIBILITY`, `AGILITY`, `POWER`, `COORDINATION` |

### 공통 에러 코드

| errorcode | 메시지 | 설명 |
| --- | --- | --- |
| `INVALID_REQUEST_BODY` | 입력값이 올바르지 않습니다. | 입력 검증 실패, 422 |
| `AUTH_UNAUTHORIZED` | 인증이 필요합니다. | 인증 실패 또는 만료, 401 |
| `AUTH_INVALID_CREDENTIALS` | 이메일 또는 비밀번호가 올바르지 않습니다. | 인증 정보 불일치, 401 |
| `PARENT_ALREADY_EXISTS` | 이미 가입된 이메일입니다. | 이메일 중복, 409 |
| `CHILD_NOT_FOUND` | 자녀 정보를 찾을 수 없습니다. | 자녀 없음, 404 |
| `CHILD_ACCESS_DENIED` | 해당 자녀에 접근할 수 없습니다. | 다른 학부모 자녀 접근, 403 |
| `MEASUREMENT_NOT_FOUND` | 측정 기록을 찾을 수 없습니다. | 측정 없음, 404 |
| `MEASUREMENT_ACCESS_DENIED` | 해당 측정 기록에 접근할 수 없습니다. | 다른 자녀의 측정 접근, 403 |
| `CENTER_NOT_FOUND` | 센터를 찾을 수 없습니다. | 센터 없음, 404 |
| `EXTERNAL_API_UNAVAILABLE` | 외부 데이터를 일시적으로 사용할 수 없습니다. | 공공 API 장애, 503 |

FastAPI 자동 OpenAPI 문서(`/docs`)에서 실제 스키마와 예시를 확인할 수 있습니다.
