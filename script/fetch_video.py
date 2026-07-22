"""
국민체력100 동영상 정보 API (15108846) 응답 저장 스크립트
표준 REST 방식 (apis.data.go.kr 계열, uddi 없음)

사용법(bash):
    pip install httpx
    export KSPO_SERVICE_KEY="발급받은_서비스키"
    python fetch_video.py

결과:
    ./kspo_responses/ 폴더에 엔드포인트별 원본 JSON 저장
    + _schema_summary.json (각 응답의 필드 키 요약)
"""
import json
import os
import sys
from datetime import datetime
from pathlib import Path

import httpx

from kspo_common import extract_items, fetch, normalize_key

# ── 설정 ────────────────────────────────────────────────
SERVICE_KEY = os.environ.get("KSPO_SERVICE_KEY", "")

# 표준 REST base URL — 활용신청 후 참고문서의 실제 값으로 교체
#   예: https://apis.data.go.kr/B551014/nfa_video   (기관코드/서비스명 부분은 실제 값으로)
BASE = "https://apis.data.go.kr/B551014/SRVC_TODZ_VDO_PKG"  # ← 실제 값으로 교체

# 상세기능 7종 (엔드포인트명은 문서에서 확인됨)
ENDPOINTS = {
    "01_trng_guide": "TODZ_VDO_TRNG_GUIDE_I",    # 운동처방가이드
    "02_ftns_cert":  "TODZ_VDO_FTNS_CERT_I",     # 체력인증측정방법
    "03_trng_video": "TODZ_VDO_TRNG_VIDEO_I",    # 운동처방동영상
    "04_mscl_trng":  "TODZ_VDO_MSCL_TRNG_I",     # 근골격계운동
    "05_std_ftns":   "TODZ_VDO_STD_FTNS_I",      # 생애주기별표준운동
    "06_routine":    "TODZ_VDO_ROUTINE_I",       # 목적별루틴운동
    "07_view_all":   "TODZ_VDO_VIEW_ALL_LIST_I", # 동영상 목록 조회
}

OUT_DIR = Path("./kspo_responses")
NUM_OF_ROWS = 20   # 스키마 파악용이니 적게
TIMEOUT = 15.0


def summarize_fields(payload) -> dict:
    """표준 공공API 응답에서 아이템 리스트를 찾아 첫 아이템의 필드 키 추출."""
    items = extract_items(payload)
    if not items:
        return {"item_count": 0, "fields": [], "sample": None}
    first = items[0]
    return {
        "item_count": len(items),
        "fields": sorted(first.keys()) if isinstance(first, dict) else [],
        "sample": first,
    }


# ── 메인 ────────────────────────────────────────────────
def main() -> int:
    if not SERVICE_KEY:
        print("환경변수 KSPO_SERVICE_KEY 를 설정하세요.")
        return 1

    key = normalize_key(SERVICE_KEY)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    schema_summary = {"fetched_at": datetime.now().isoformat(), "base": BASE, "endpoints": {}}

    with httpx.Client(timeout=TIMEOUT) as client:
        for name, path in ENDPOINTS.items():
            print(f"[요청] {name}  {path}")
            try:
                payload = fetch(client, BASE, path, key, NUM_OF_ROWS)
            except httpx.HTTPStatusError as e:
                print(f"  ↳ HTTP {e.response.status_code}: {e.response.text[:200]}")
                schema_summary["endpoints"][name] = {"error": f"HTTP {e.response.status_code}"}
                continue
            except httpx.HTTPError as e:
                print(f"  ↳ 네트워크 오류: {e}")
                schema_summary["endpoints"][name] = {"error": str(e)}
                continue

            out_file = OUT_DIR / f"{name}.json"
            out_file.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

            summary = summarize_fields(payload)
            schema_summary["endpoints"][name] = {
                "path": path,
                "item_count": summary["item_count"],
                "fields": summary["fields"],
            }
            print(f"  ↳ 저장: {out_file}  (아이템 {summary['item_count']}개, 필드 {len(summary['fields'])}개)")

    summary_file = OUT_DIR / "_schema_summary.json"
    summary_file.write_text(json.dumps(schema_summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n[완료] 스키마 요약: {summary_file}")
    print("각 엔드포인트 fields 를 보고 모델·매핑을 확정하세요.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
