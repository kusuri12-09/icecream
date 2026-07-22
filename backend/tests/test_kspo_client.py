import httpx

from app.external.kspo_client import KspoClient, _resource_url


def test_resource_url_normalizes_http_media_url_to_https():
    assert _resource_url("http://openapi.kspo.or.kr/web/video/", "sample.mp4") == (
        "https://openapi.kspo.or.kr/web/video/sample.mp4"
    )


def test_get_requests_json_response(monkeypatch):
    captured: dict[str, object] = {}

    class FakeResponse:
        def raise_for_status(self):
            return None

        def json(self):
            return {"response": {"body": {}}}

    def fake_get(url, params, timeout):
        captured.update({"url": url, "params": params, "timeout": timeout})
        return FakeResponse()

    monkeypatch.setattr(httpx, "get", fake_get)

    KspoClient("test-key")._get("https://example.com/api")

    assert captured["params"] == {
        "serviceKey": "test-key",
        "pageNo": 1,
        "numOfRows": 100,
        "resultType": "json",
    }


def test_fetch_centers_aggregates_monthly_measure_counts(monkeypatch):
    payload = {
        "response": {
            "body": {
                "totalCount": 3,
                "items": {
                    "item": [
                        {
                            "center_nm": "청주",
                            "center_addr1": "청주시 서원구 사직대로 229",
                            "center_addr2": "1층 청주체력인증센터",
                            "test_ym": "201702",
                            "test_cnt": 195,
                        },
                        {
                            "center_nm": "청주",
                            "center_addr1": "청주시 서원구 사직대로 229",
                            "center_addr2": "1층 청주체력인증센터",
                            "test_ym": "202009",
                            "test_cnt": 8,
                        },
                        {
                            "center_nm": "오산",
                            "center_addr1": "경기도 오산시 경기동로 33",
                            "center_addr2": "오산스포츠센터 1층",
                            "test_ym": "201811",
                            "test_cnt": 859,
                        },
                    ]
                },
            }
        }
    }

    client = KspoClient("test-key")
    monkeypatch.setattr(client, "_get", lambda url, page_no=1, num_of_rows=1000: payload)

    records = client.fetch_centers("https://example.com/api")

    assert len(records) == 2
    cheongju = next(record for record in records if record.name == "청주")
    assert cheongju.measure_count == 203
    assert cheongju.sido_sigungu == "청주시 서원구"
    assert cheongju.ext_center_id.startswith("kspo_center_")


def test_fetch_activities_maps_trng_guide_fields_and_deduplicates_frames(monkeypatch):
    payload = {
        "response": {
            "body": {
                "totalCount": 2,
                "items": {
                    "item": [
                        {
                            "file_nm": "video-001.mp4",
                            "file_url": "https://example.com/video/",
                            "img_file_nm": "video-001.jpeg",
                            "img_file_url": "https://example.com/image/",
                            "vdo_ttl_nm": "팔 굽혀 펴기",
                            "vdo_desc": "유소년 근력 운동",
                            "ftns_fctr_nm": "근력/근지구력",
                            "ftns_lvl_nm": "중급",
                            "tool_nm": "매트",
                            "trng_plc_nm": "실내",
                            "trng_mscl_part": "가슴",
                            "vdo_len": "91",
                            "aggrp_nm": "유소년",
                        },
                        {
                            "file_nm": "video-001.mp4",
                            "file_url": "https://example.com/video/",
                            "img_file_nm": "video-001.jpeg",
                            "img_file_url": "https://example.com/image/",
                            "vdo_ttl_nm": "팔 굽혀 펴기",
                            "ftns_fctr_nm": "근력/근지구력",
                            "aggrp_nm": "유소년",
                        },
                    ]
                },
            }
        }
    }

    client = KspoClient("test-key")
    monkeypatch.setattr(client, "_get", lambda url, page_no=1, num_of_rows=1000: payload)

    records = client.fetch_activities("https://example.com/api")

    assert len(records) == 1
    record = records[0]
    assert record.ext_video_id == "video-001.mp4"
    assert record.url == "https://example.com/video/video-001.mp4"
    assert record.thumbnail_url == "https://example.com/image/video-001.jpeg"
    assert record.fitness_elements == ("GRIP", "MUSCULAR_END")
    assert record.fitness_element == "GRIP"
    assert record.age_group == "PRESCHOOL"
    assert record.duration_seconds == 91
    assert record.equipment == "매트"
