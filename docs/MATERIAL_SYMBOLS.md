# Material Symbols 사용 목록

화면 아이콘은 `frontend/src/components/Icon.tsx`의 공통 `Icon` 컴포넌트를 통해 사용한다. 페이지에서 Material Symbols의 ligature 이름을 직접 작성하지 않고, `Icon`의 의미 있는 공통 이름을 전달한다.

Material Symbols Rounded 폰트는 `frontend/src/main.tsx`에서 `material-symbols/rounded.css`로 로드한다. 폰트 파일은 `material-symbols` npm 패키지에 포함되어 Vite 빌드에 번들된다.

## 매핑 목록

| 공통 이름 | Material Symbols 이름 | 주요 사용처 |
| --- | --- | --- |
| `add` | `add` | 자녀 추가 |
| `add_task` | `add_task` | 활동 추가 |
| `analytics` | `analytics` | 통계/진단 |
| `arrow_back` | `arrow_back` | 뒤로가기 |
| `arrow_forward` | `arrow_forward` | 다음/전체보기 |
| `boy` | `boy` | 남아 프로필 |
| `call` | `call` | 센터 전화 |
| `chevron_right` | `chevron_right` | 목록 이동 |
| `child_care` | `child_care` | 유아 측정 |
| `directions_run` | `directions_run` | 활동 |
| `eco` | `eco` | 성장/브랜드 |
| `edit_note` | `edit_note` | 기록 수정 |
| `expand_more` | `expand_more` | 선택 메뉴 |
| `face` | `face` | 사용자 |
| `flashlight` | `flashlight_on` | 강조 팁 |
| `fitness_center` | `fitness_center` | 근력/운동 |
| `flag` | `flag` | 목표 |
| `girl` | `girl` | 여아 프로필 |
| `home` | `home` | 홈 탭 |
| `history` | `history` | 측정 기록 |
| `info` | `info` | 안내 |
| `lightbulb` | `lightbulb` | 팁 |
| `location_on` | `location_on` | 위치 |
| `map` | `map` | 지도 |
| `map_pin_2` | `location_on` | 지도 핀 |
| `menu` | `menu` | 메뉴 |
| `men` | `man` | 남성 |
| `my_location` | `my_location` | 내 위치 |
| `near_me` | `near_me` | 길찾기 |
| `nutrition` | `restaurant` | 영양 |
| `accessibility_new` | `accessibility_new` | 유연성/접근성 |
| `arrow_up_double` | `vertical_align_top` | 제자리멀리뛰기 |
| `chat` | `chat` | 상담 |
| `groups` | `groups` | 지역 참여 |
| `open_in_new` | `open_in_new` | 외부 링크 |
| `run` | `directions_run` | 달리기 |
| `schedule` | `schedule` | 시간 |
| `search` | `search` | 검색 |
| `seedling` | `eco` | 새싹 |
| `sparkling` | `auto_awesome` | 추천 |
| `sports_score` | `sports_score` | 활동 추천 |
| `straighten` | `straighten` | 신장 |
| `trending_up` | `trending_up` | 성장 추이 |
| `user_smile` | `face` | 프로필 |
| `women` | `woman` | 여성 |
| `footprint` | `footprint` | 걸음 |
| `tree` | `park` | 공원 |
| `home_4` | `fitness_center` | 체육관 |
| `community` | `groups` | 커뮤니티 |
| `football` | `sports_soccer` | 스포츠 |

## 상태와 크기

- 기본 아이콘은 `FILL 0`인 외곽선 스타일을 사용한다.
- 활성 하단 탭과 등급 배지는 `Icon`의 `filled` 속성으로 `FILL 1`을 사용한다.
- 탭 아이콘은 24px, 인라인 아이콘은 20px, 보조 아이콘은 16px을 기준으로 한다.
- 아이콘 버튼에는 아이콘만 보이더라도 명확한 `aria-label`을 제공한다.
