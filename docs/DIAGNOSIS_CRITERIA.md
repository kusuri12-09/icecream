# 진단 기준표 개정·재로딩 절차

진단 기준표는 `backend/data/fitness_grade_criteria.json`으로 관리한다. 측정 결과에는 판정 당시 등급이 저장되므로 기준표 개정 이후에도 기존 측정 결과를 다시 판정하지 않는다.

## 개정 절차

1. 공식 기준표를 검토하고 JSON의 `meta.version`, 출처, 변경 내용을 갱신한다.
2. `backend/tests/test_criteria_loader.py`와 진단 엔진 테스트를 실행한다.

   ```powershell
   uv run pytest tests/test_criteria_loader.py tests/test_api.py
   ```

3. 전체 백엔드 검증을 실행한다.

   ```powershell
   uv run pytest
   uv run ruff check app tests alembic
   uv run mypy app
   ```

4. 검증을 통과한 기준표와 코드 변경을 함께 배포한다.

## 재로딩 동작

`app.services.diagnosis_engine.reload_criteria()`는 새 파일을 먼저 검증한다. 검증에 실패하면 기존 캐시를 유지하고, 검증에 성공한 경우에만 캐시를 비운 뒤 다음 진단부터 개정 기준표를 사용한다.

Vercel에서는 파일을 런타임에 수정하지 않고 새 기준표를 포함한 배포를 수행한다. 새 인스턴스는 기준표를 최초 요청 시 읽는다. 로컬처럼 장시간 실행 중인 프로세스에서 파일을 교체한 경우에만 `reload_criteria()`를 호출한다.
