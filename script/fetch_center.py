"""
국민체력100 체력인증센터 측정건수 정보 API (15114286) 응답 저장 스크립트
표준 REST 방식 (apis.data.go.kr 계열, uddi 없음)
사용법(bash):
    pip install httpx
    export KSPO_SERVICE_KEY="발급받은_서비스키"
    python fetch_center.py
결과:
    ./kspo_responses/ 폴더에 center_measure_count.json 원본 저장
    + center_schema_summary.json (필드 키 요약, 지역 후보 필드 강조)
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
BASE = "https://apis.data.go.kr/B551014/SRVC_TODZ_NFA_TEST_CENTER_CNT"   # 활용신청 후 참고문서의 실제 값으로 교체
ENDPOINT = "TODZ_NFA_TEST_CENTER_CNT"                          # 실제 엔드포인트명으로 교체

OUT_DIR = Path("./kspo_responses")
NUM_OF_ROWS = 50
TIMEOUT = 15.0

# 지역 관련일 가능성이 있는 필드명 힌트 (요약 시 강조용)
REGION_HINTS = ["sido", "sgg", "sigungu", "addr", "지역", "시도", "시군구", "주소", "region", "area"]


# ── 메인 ────────────────────────────────────────────────
def main() -> int:
    if not SERVICE_KEY:
        print("환경변수 KSPO_SERVICE_KEY 를 설정하세요.")
        return 1

    key = normalize_key(SERVICE_KEY)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

        print(f"[요청] {BASE}/{ENDPOINT}")
    try:
        with httpx.Client(timeout=TIMEOUT) as client:
            payload = fetch(client, BASE, ENDPOINT, key, NUM_OF_ROWS)
    except httpx.HTTPStatusError as e:
        print(f"  ↳ HTTP {e.response.status_code}: {e.response.text[:300]}")
        return 1
    except httpx.HTTPError as e:
        print(f"  ↳ 네트워크 오류: {e}")
        return 1

    # 원본 저장
    out_file = OUT_DIR / "center_measure_count.json"
    out_file.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  ↳ 저장: {out_file}")

    # 스키마 요약
    items = extract_items(payload)
    if not items:
        print("  ↳ 아이템을 찾지 못함. 저장된 원본을 직접 확인하세요.")
        return 0

    fields = sorted(items[0].keys()) if isinstance(items[0], dict) else []
    region_fields = [f for f in fields if any(h in f.lower() for h in REGION_HINTS)]

    print(f"\n[요약] 아이템 {len(items)}개, 필드 {len(fields)}개")
    print(f"  필드: {fields}")
    print(f"  지역 관련 후보 필드: {region_fields if region_fields else '(없음 — 센터 단위만 제공될 수 있음)'}")
    print("\n  첫 아이템 샘플:")
    print(json.dumps(items[0], ensure_ascii=False, indent=2))

    summary = {
        "fetched_at": datetime.now().isoformat(),
        "base": BASE,
        "endpoint": ENDPOINT,
        "item_count": len(items),
        "fields": fields,
        "region_candidate_fields": region_fields,
    }
    (OUT_DIR / "center_schema_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"\n[완료] 요약: {OUT_DIR / 'center_schema_summary.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
