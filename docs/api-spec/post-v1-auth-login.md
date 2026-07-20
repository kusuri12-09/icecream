# POST /api/v1/auth/login

## 설명

이메일과 비밀번호로 로그인하고 액세스 토큰을 발급합니다.

## REQUEST

```json
{
  "email": "parent@example.com",
  "password": "string"
}
```

## RESPONSE

상태 코드 `200`

```json
{
  "success": true,
  "data": {
    "parent": { "id": "parent_a1b2c3", "email": "parent@example.com" },
    "accessToken": "eyJhbGci...",
    "tokenType": "bearer"
  }
}
```

## ERRORCODE

| errorcode | 메시지 | 설명 |
| --- | --- | --- |
| `AUTH_INVALID_CREDENTIALS` | 이메일 또는 비밀번호가 올바르지 않습니다. | 인증 정보 불일치, 401 |
| `INVALID_REQUEST_BODY` | 입력값이 올바르지 않습니다. | 요청 본문 검증 실패, 422 |
