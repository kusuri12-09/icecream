# 아이쑥크림 데이터베이스 설계 명세

## 공통 규칙

### 식별자 전략
- 내부 PK: `id BIGINT AUTO_INCREMENT` (조인·성능·관리 단순화)
- 외부 응답 ID: `{resource}_{id}` 접두어 형식으로 인코딩 (예: `child_123`, `measurement_4567`). API 경계에서만 인코딩/디코딩하고 DB·내부 로직은 순수 bigint 사용
- 순차 ID 노출이 민감한 리소스(`parent`)는 `public_id UUID`를 별도 컬럼으로 두어 외부 식별에 사용

### 공통 컬럼 (모든 테이블)
| 컬럼 | 타입 | 제약 | 설명 |
| :--- | :--- | :--- | :--- |
| `id` | BIGINT | PK, AUTO_INCREMENT | 내부 기본키 |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT now() | 생성 시각 |
| `updated_at` | TIMESTAMP | NOT NULL, DEFAULT now() ON UPDATE now() | 최종 수정 시각 |

### Enum 정의
| Enum | 값 | 사용처 |
| :--- | :--- | :--- |
| `gender` | `male`, `female` | child.gender |
| `measurement_type` | `official`(정식), `self`(자가 참고용) | measurement.type |
| `grade` | `seed`(씨앗), `sprout`(새싹), `flower`(꽃), `fruit`(열매) | measurement.grade, measurement_item.item_grade |
| `item_key` | `cardio`, `grip`, `muscular_end`, `flexibility`, `agility`, `power`, `coordination`, `bmi` | measurement_item.item_key |
| `fitness_element` | `cardio`, `grip`, `muscular_end`, `flexibility`, `agility`, `power`, `coordination` | activity_video.fitness_element |

> Enum은 애플리케이션 레벨(Python Enum + Pydantic)에서 검증. DB에는 값 추가 가능성이 있는 `item_key`·`fitness_element`는 VARCHAR + CHECK, 그 외는 네이티브 ENUM 또는 VARCHAR + CHECK로 저장.

## 1. parent (학부모 계정)
| 컬럼 | 타입 | 제약 | 설명 |
| :--- | :--- | :--- | :--- |
| `id` | BIGINT | PK, AUTO_INCREMENT | 내부 기본키 |
| `public_id` | UUID | UNIQUE, NOT NULL, DEFAULT gen_random_uuid() | 외부 노출용 식별자 |
| `email` | VARCHAR(255) | UNIQUE, NOT NULL | 로그인 ID |
| `password_hash` | VARCHAR(255) | NOT NULL | Argon2id/bcrypt 해시 |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT now() | 생성 시각 |
| `updated_at` | TIMESTAMP | NOT NULL, DEFAULT now() | 최종 수정 시각 |

> 센터 API(15114286)의 실제 응답은 `center_nm`·`center_addr1` 기준 센터별 월별(`test_ym`) 측정건수 행이다. 시군구·위도·경도 필드는 제공되지 않으므로 기본 주소 앞 두 토큰으로 `sido_sigungu`를 파생하고, 센터명·기본 주소의 안정적인 해시를 `ext_center_id`로 사용한다. 동기화 시 모든 월의 `test_cnt`를 센터별로 합산해 `measure_count`에 저장한다.

### 인덱스
| 이름 | 컬럼 | 종류 | 목적 |
| :--- | :--- | :--- | :--- |
| `uq_parent_email` | email | UNIQUE | 로그인 조회·중복 방지 |
| `uq_parent_public_id` | public_id | UNIQUE | 외부 ID 조회 |

## 2. child (자녀 프로필)
| 컬럼 | 타입 | 제약 | 설명 |
| :--- | :--- | :--- | :--- |
| `id` | BIGINT | PK, AUTO_INCREMENT | 내부 기본키 |
| `parent_id` | BIGINT | FK → parent.id, NOT NULL | 소유 학부모 |
| `nickname` | VARCHAR(50) | NOT NULL | 자녀 애칭 |
| `gender` | VARCHAR(10) | NOT NULL, CHECK(male/female) | 기준표 조회 키 |
| `birth_year_month` | DATE | NOT NULL | 생년월(개월수 계산용, 일자는 01 고정) |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT now() | 생성 시각 |
| `updated_at` | TIMESTAMP | NOT NULL, DEFAULT now() | 최종 수정 시각 |

### 인덱스
| 이름 | 컬럼 | 종류 | 목적 |
| :--- | :--- | :--- | :--- |
| `ix_child_parent_id` | parent_id | INDEX | 학부모별 자녀 목록 조회 |

> 개월수는 조회/측정 시점에 `birth_year_month` 기준으로 계산하며 저장하지 않는다(시간에 따라 변하므로).

## 3. measurement (측정 세션)
| 컬럼 | 타입 | 제약 | 설명 |
| :--- | :--- | :--- | :--- |
| `id` | BIGINT | PK, AUTO_INCREMENT | 내부 기본키 |
| `child_id` | BIGINT | FK → child.id, NOT NULL | 대상 자녀 |
| `center_id` | BIGINT | FK → center.id, NULLABLE | 측정 센터(정식만, 자가는 NULL) |
| `type` | VARCHAR(10) | NOT NULL, CHECK(official/self) | 측정 유형 |
| `grade` | VARCHAR(10) | NULLABLE, CHECK(seed/sprout/flower/fruit) | 종합 등급(측정 당시 기준으로 판정·보존) |
| `age_months_at_measure` | SMALLINT | NOT NULL | 측정 시점 개월수(판정 재현·감사용 스냅샷) |
| `measured_at` | DATE | NOT NULL | 측정일 |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT now() | 생성 시각 |
| `updated_at` | TIMESTAMP | NOT NULL, DEFAULT now() | 최종 수정 시각 |

### 인덱스
| 이름 | 컬럼 | 종류 | 목적 |
| :--- | :--- | :--- | :--- |
| `ix_measurement_child_measured` | (child_id, measured_at DESC) | 복합 INDEX | 자녀별 최신순 기록·추이 조회 |
| `ix_measurement_center_id` | center_id | INDEX | 센터별 집계(선택) |

> `grade`·`age_months_at_measure`는 비정규화 스냅샷. 기준표가 개정돼도 "측정 당시 판정 등급"을 보존하기 위함. 판정 로직은 앱 메모리의 기준표 JSON을 참조.

## 4. measurement_item (항목별 측정값, long 구조)
| 컬럼 | 타입 | 제약 | 설명 |
| :--- | :--- | :--- | :--- |
| `id` | BIGINT | PK, AUTO_INCREMENT | 내부 기본키 |
| `measurement_id` | BIGINT | FK → measurement.id, NOT NULL | 소속 측정 세션 |
| `item_key` | VARCHAR(20) | NOT NULL, CHECK(8종) | 측정 항목 |
| `value` | NUMERIC(6,2) | NOT NULL | 측정 원점수 |
| `item_grade` | VARCHAR(10) | NULLABLE, CHECK(seed~fruit) | 항목별 판정(강·약 프로파일용) |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT now() | 생성 시각 |
| `updated_at` | TIMESTAMP | NOT NULL, DEFAULT now() | 최종 수정 시각 |

### 인덱스
| 이름 | 컬럼 | 종류 | 목적 |
| :--- | :--- | :--- | :--- |
| `uq_item_per_measurement` | (measurement_id, item_key) | UNIQUE | 세션당 항목 1개 보장 |
| `ix_item_key_measurement` | (item_key, measurement_id) | INDEX | 항목별 시계열 추이 조회 |

> long 구조 채택 이유: 미입력 항목은 행 부재로 자연 처리, 항목 추가 시 스키마 무변경, 항목별 추이 쿼리 단순.

## 5. center (체력인증센터, 공공 API 캐시)
| 컬럼 | 타입 | 제약 | 설명 |
| :--- | :--- | :--- | :--- |
| `id` | BIGINT | PK, AUTO_INCREMENT | 내부 기본키 |
| `ext_center_id` | VARCHAR(50) | UNIQUE, NOT NULL | 원본 센터 식별자(동기화 중복 방지) |
| `name` | VARCHAR(100) | NOT NULL | 센터명 |
| `address` | VARCHAR(255) | NOT NULL | 기본 주소 |
| `sido_sigungu` | VARCHAR(50) | NULLABLE | 주소 파싱한 시도·시군구(지역 인사이트 키) |
| `latitude` | NUMERIC(9,6) | NULLABLE | 위도 |
| `longitude` | NUMERIC(9,6) | NULLABLE | 경도 |
| `measure_count` | INTEGER | NOT NULL, DEFAULT 0 | 측정건수(지역 참여율 집계용) |
| `synced_at` | TIMESTAMP | NOT NULL | 마지막 동기화 시각 |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT now() | 생성 시각 |
| `updated_at` | TIMESTAMP | NOT NULL, DEFAULT now() | 최종 수정 시각 |

### 인덱스
| 이름 | 컬럼 | 종류 | 목적 |
| :--- | :--- | :--- | :--- |
| `uq_center_ext_id` | ext_center_id | UNIQUE | 동기화 upsert 키 |
| `ix_center_sido_sigungu` | sido_sigungu | INDEX | 지역별 참여율 집계 |
| `ix_center_lat_lng` | (latitude, longitude) | INDEX | 근처 센터 검색(선택, 소규모는 앱 계산 가능) |

## 6. activity_video (운동처방 동영상, 공공 API 캐시)
| 컬럼 | 타입 | 제약 | 설명 |
| :--- | :--- | :--- | :--- |
| `id` | BIGINT | PK, AUTO_INCREMENT | 내부 기본키 |
| `ext_video_id` | VARCHAR(50) | UNIQUE, NOT NULL | 원본 동영상 식별자 |
| `title` | VARCHAR(200) | NOT NULL | 콘텐츠 제목 |
| `fitness_element` | VARCHAR(20) | NULLABLE | 대표 정규화 체력요소(약점 매칭 호환 키) |
| `fitness_elements` | JSON | NULLABLE | 원본 체력요인에서 정규화한 복수 매칭 키 |
| `age_group` | VARCHAR(20) | NULLABLE | 정규화 대상 연령대(`유소년` → `PRESCHOOL`) |
| `url` | VARCHAR(500) | NOT NULL | 동영상 링크 |
| `description` | TEXT | NULLABLE | `vdo_desc` 운동 설명 |
| `thumbnail_url` | VARCHAR(500) | NULLABLE | `img_file_url`과 `img_file_nm`으로 조합한 썸네일 링크 |
| `fitness_level` | VARCHAR(20) | NULLABLE | `ftns_lvl_nm` 운동 난이도 |
| `equipment` | VARCHAR(100) | NULLABLE | `tool_nm` 사용 도구 |
| `training_place` | VARCHAR(50) | NULLABLE | `trng_plc_nm` 운동 장소 |
| `muscle_part` | VARCHAR(255) | NULLABLE | `trng_mscl_part` 운동 부위 |
| `duration_seconds` | INTEGER | NULLABLE | `vdo_len` 영상 길이(초) |
| `source_fitness_factor` | VARCHAR(50) | NULLABLE | 원본 `ftns_fctr_nm` 값 보존 |
| `source_age_group` | VARCHAR(20) | NULLABLE | 원본 `aggrp_nm` 값 보존 |
| `synced_at` | TIMESTAMP | NOT NULL | 마지막 동기화 시각 |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT now() | 생성 시각 |
| `updated_at` | TIMESTAMP | NOT NULL, DEFAULT now() | 최종 수정 시각 |

### 인덱스
| 이름 | 컬럼 | 종류 | 목적 |
| :--- | :--- | :--- | :--- |
| `uq_video_ext_id` | ext_video_id | UNIQUE | `file_nm` 기준 동기화 upsert 키 및 프레임 중복 제거 |
| `ix_video_element` | (fitness_element, age_group) | INDEX | 약점 요소별 콘텐츠 조회 |

> 동영상 API `01_trng_guide` 응답은 한 영상의 프레임마다 행이 반복된다. 동기화 시 `file_nm`을 영상 식별자로 사용해 하나의 영상만 저장하고, `file_url + file_nm` 및 `img_file_url + img_file_nm`으로 실제 리소스 URL을 조합한다.

## 캐싱 전략
| 대상 | 방식 | 주기/무효화 | 이유 |
| :--- | :--- | :--- | :--- |
| 판정 기준표(JSON) | 앱 메모리 로드(In-memory) | 앱 기동 시 1회, 고시 개정 시 재배포 | 정적 데이터, 매 진단마다 즉시 참조 필요 |
| center / activity_video | DB 캐시(공공 API → 테이블 저장) | 배치 동기화(일/주 단위), synced_at 기준 upsert | 준정적, 외부 API 장애 격리 |
| 지역별 참여율 집계 | 애플리케이션 캐시(선택, Redis/메모리) | 센터 동기화 후 재계산, TTL 수 시간 | 반복 조회되는 집계 결과, 실시간성 불필요 |
| 근처 센터 검색 | 앱 계산 또는 DB 인덱스 | 센터 수백 개 규모라 캐시 불필요 | 데이터 소규모 |

## 관계 요약
| 관계 | 카디널리티 | 삭제 정책 |
| :--- | :--- | :--- |
| parent → child | 1 : N | parent 삭제 시 child CASCADE |
| child → measurement | 1 : N | child 삭제 시 measurement CASCADE |
| measurement → measurement_item | 1 : N | measurement 삭제 시 item CASCADE |
| center → measurement | 0..1 : N | center 삭제 시 measurement.center_id SET NULL |
