"""활동 데이터를 100개 페이지 단위로 내부 sync API에 저장한다.

사용 예:
    $env:ICECREAM_API_URL = "http://localhost:8000"
    $env:ADMIN_ACCESS_TOKEN = "<관리자 access token>"
    python script/sync_activities.py

Vercel 등 요청 시간 제한이 있는 환경에서 수천 건의 원본 행을 한 번에
처리하지 않도록 페이지별 요청과 커밋을 수행한다.
"""

import argparse
import json
import os
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


DEFAULT_PAGE_SIZE = 100
MAX_PAGE_SIZE = 1000


def sync_page(base_url: str, token: str, page: int, page_size: int, timeout: int) -> dict:
    query = urlencode({"page": page, "page_size": page_size})
    request = Request(
        f"{base_url.rstrip('/')}/api/v1/internal/sync?{query}",
        data=json.dumps({"targets": ["ACTIVITIES"]}).encode("utf-8"),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urlopen(request, timeout=timeout) as response:
            body = json.load(response)
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"sync API 요청 실패 status={exc.code} detail={detail}") from exc
    except URLError as exc:
        raise RuntimeError(f"sync API 연결 실패: {exc.reason}") from exc

    if body.get("success") is not True:
        raise RuntimeError(f"sync API 오류: {body}")
    return body.get("data", {})


def main() -> None:
    parser = argparse.ArgumentParser(description="활동 데이터를 페이지별로 동기화합니다.")
    parser.add_argument(
        "--base-url",
        default=os.getenv("ICECREAM_API_URL", "http://localhost:8000"),
        help="백엔드 기본 URL(기본값: ICECREAM_API_URL 또는 http://localhost:8000)",
    )
    parser.add_argument(
        "--token",
        default=os.getenv("ADMIN_ACCESS_TOKEN"),
        help="관리자 access token(기본값: ADMIN_ACCESS_TOKEN)",
    )
    parser.add_argument("--page-size", type=int, default=DEFAULT_PAGE_SIZE, help="페이지당 원본 행 수")
    parser.add_argument("--timeout", type=int, default=60, help="개별 API 요청 timeout(초)")
    args = parser.parse_args()

    if not args.token:
        parser.error("--token 또는 ADMIN_ACCESS_TOKEN이 필요합니다.")
    if not 1 <= args.page_size <= MAX_PAGE_SIZE:
        parser.error(f"--page-size는 1에서 {MAX_PAGE_SIZE} 사이여야 합니다.")

    page = 1
    while True:
        result = sync_page(args.base_url, args.token, page, args.page_size, args.timeout)
        total_pages = int(result.get("totalPages", page))
        print(f"활동 sync page={page}/{total_pages} 저장={result.get('synced', 0)}")
        if not result.get("hasNext", page < total_pages):
            break
        page += 1


if __name__ == "__main__":
    main()
