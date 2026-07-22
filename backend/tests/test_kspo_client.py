from app.external.kspo_client import KspoClient


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
