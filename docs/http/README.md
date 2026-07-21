# API HTTP 테스트

로컬 서버를 실행한 뒤 각 도메인별 `.http` 파일의 요청 왼쪽에 있는 실행 버튼을 눌러 테스트합니다.

```powershell
cd D:\lecture\icecream\backend
uv run uvicorn app.main:app --reload
```

기본 변수는 각 파일 상단의 `baseUrl`, `accessToken`, 리소스 ID를 수정합니다.

- `auth.http`의 로그인 요청은 JetBrains HTTP Client 기준으로 `accessToken`을 자동 저장합니다.
- 자동 저장이 되지 않는 클라이언트에서는 로그인 응답의 `data.accessToken`을 각 파일의 `accessToken` 변수에 직접 입력합니다.
- 자녀·측정·센터·동영상 ID는 앞선 생성/동기화 응답의 `data.id`로 교체합니다.
