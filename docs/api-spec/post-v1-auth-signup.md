# POST /api/v1/auth/signup

## 설명

학부모 회원을 가입시킵니다.

## REQUEST

```json
{
  "email": "parent@example.com",
  "password": "string(8-64)"
}
```

## RESPONSE

상태 코드 `201`

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
| `PARENT_ALREADY_EXISTS` | 이미 가입된 이메일입니다. | 이메일 중복, 409 |
| `INVALID_REQUEST_BODY` | 입력값이 올바르지 않습니다. | 요청 본문 검증 실패, 422 |
