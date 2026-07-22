"""국민체력100 공공 API 요청·응답 처리 공통 유틸리티."""

import json
from typing import Any
from urllib.parse import unquote

import httpx


def normalize_key(key: str) -> str:
    """퍼센트 인코딩된 서비스키를 API 요청에 사용할 형태로 되돌린다."""
    return unquote(key) if "%" in key else key


def extract_items(payload: Any) -> list[dict[str, Any]]:
    """표준 공공 API 또는 odcloud 응답에서 항목 목록을 추출한다."""
    if not isinstance(payload, dict):
        return []

    response = payload.get("response")
    body = response.get("body", {}) if isinstance(response, dict) else {}
    items = body.get("items") if isinstance(body, dict) else None
    if isinstance(items, dict):
        items = items.get("item")
    if isinstance(items, dict):
        return [items]
    if isinstance(items, list):
        return [item for item in items if isinstance(item, dict)]

    data = payload.get("data")
    if isinstance(data, list):
        return [item for item in data if isinstance(item, dict)]
    return []


def fetch(
    client: httpx.Client,
    base_url: str,
    endpoint: str,
    key: str,
    num_of_rows: int,
) -> dict[str, Any]:
    """지정한 국민체력100 엔드포인트에서 JSON 응답을 가져온다."""
    url = f"{base_url.rstrip('/')}/{endpoint.lstrip('/')}"
    params = {
        "serviceKey": key,
        "pageNo": 1,
        "numOfRows": num_of_rows,
        "resultType": "json",
    }
    response = client.get(url, params=params)
    response.raise_for_status()
    raw_text = response.text.strip()
    try:
        payload = json.loads(raw_text)
    except json.JSONDecodeError:
        return {"_raw_text": raw_text, "_note": "JSON 파싱 실패 — XML이거나 resultType 파라미터명이 다를 수 있음"}
    return payload if isinstance(payload, dict) else {"data": payload}
