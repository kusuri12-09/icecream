---
name: icecream
colors:
  surface: '#faf9f5'
  surface-dim: '#dbdad6'
  surface-bright: '#faf9f5'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f4f4f0'
  surface-container: '#efeeea'
  surface-container-high: '#e9e8e4'
  surface-container-highest: '#e3e2df'
  on-surface: '#1b1c1a'
  on-surface-variant: '#404945'
  inverse-surface: '#2f312e'
  inverse-on-surface: '#f2f1ed'
  outline: '#707975'
  outline-variant: '#c0c9c4'
  surface-tint: '#366758'
  primary: '#366758'
  on-primary: '#ffffff'
  primary-container: '#b5ead7'
  on-primary-container: '#396b5c'
  inverse-primary: '#9dd1bf'
  secondary: '#874f4c'
  on-secondary: '#ffffff'
  secondary-container: '#ffb7b2'
  on-secondary-container: '#7b4542'
  tertiary: '#625f4e'
  on-tertiary: '#ffffff'
  tertiary-container: '#e4dfca'
  on-tertiary-container: '#666251'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#b9eedb'
  primary-fixed-dim: '#9dd1bf'
  on-primary-fixed: '#002018'
  on-primary-fixed-variant: '#1c4f41'
  secondary-fixed: '#ffdad7'
  secondary-fixed-dim: '#fcb4b0'
  on-secondary-fixed: '#360e0d'
  on-secondary-fixed-variant: '#6b3836'
  tertiary-fixed: '#e8e3cd'
  tertiary-fixed-dim: '#ccc7b2'
  on-tertiary-fixed: '#1e1c0f'
  on-tertiary-fixed-variant: '#4a4737'
  background: '#faf9f5'
  on-background: '#1b1c1a'
  surface-variant: '#e3e2df'
  # --- Grade (Growth Stage) colors ---
  # 항상 아이콘 + 텍스트 라벨과 함께 사용 (접근성).
  # seed/sprout/flower 는 기존 팔레트 토큰을 재사용(alias)합니다.
  # fruit(주황)만 기존 팔레트에 대응 색이 없어 신규 추가했습니다.
  grade-seed: '#625f4e'            # = tertiary
  grade-seed-container: '#e4dfca'  # = tertiary-container
  on-grade-seed-container: '#666251'  # = on-tertiary-container
  grade-sprout: '#366758'          # = primary
  grade-sprout-container: '#b5ead7'  # = primary-container
  on-grade-sprout-container: '#396b5c'  # = on-primary-container
  grade-flower: '#874f4c'          # = secondary
  grade-flower-container: '#ffb7b2'  # = secondary-container
  on-grade-flower-container: '#7b4542'  # = on-secondary-container
  grade-fruit: '#e08a3c'           # NEW (팔레트에 주황 없음)
  grade-fruit-container: '#fce3cb'  # NEW
  on-grade-fruit-container: '#9a5514'  # NEW
typography:
  headline-lg:
    fontFamily: Quicksand
    fontSize: 28px
    fontWeight: '700'
    lineHeight: 36px
    letterSpacing: -0.02em
  headline-md:
    fontFamily: Quicksand
    fontSize: 22px
    fontWeight: '700'
    lineHeight: 30px
    letterSpacing: -0.01em
  body-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 18px
    fontWeight: '500'
    lineHeight: 28px
  body-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  label-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 14px
    fontWeight: '600'
    lineHeight: 20px
    letterSpacing: 0.01em
  label-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
rounded:
  sm: 0.5rem
  DEFAULT: 1rem
  md: 1.5rem
  lg: 2rem
  xl: 3rem
  full: 9999px
spacing:
  base: 4px
  xs: 8px
  sm: 12px
  md: 16px
  lg: 24px
  xl: 32px
  gutter: 16px
  margin-mobile: 20px
shadow:
  sm: '0 4px 12px rgba(0, 0, 0, 0.04)'
  md: '0 8px 24px rgba(181, 234, 215, 0.2)'
motion:
  duration-fast: 120ms
  duration-base: 200ms
  duration-slow: 320ms
  easing-standard: 'cubic-bezier(0.2, 0, 0, 1)'
breakpoints:
  mobile: 0px
  tablet: 768px
  desktop: 1024px
state-opacity:
  hover: '0.08'
  pressed: '0.12'
  disabled: '0.38'
  disabled-container: '0.12'
---

## 이 문서를 구현에 사용하는 규칙 (READ FIRST)

- **색상값의 단일 출처는 위 프론트매터입니다.** 아래 산문에 등장하는 hex(#B5EAD7 등)는 설명을 위한 참고이며, 구현 시에는 반드시 프론트매터의 토큰 이름을 참조하세요. 산문의 값과 프론트매터의 값이 다르면 **프론트매터가 우선**입니다.
- 토큰에 없는 색·그림자·간격을 임의로 만들지 마세요. 필요하면 토큰을 추가한 뒤 사용합니다.
- 상태(hover/pressed/disabled), 트랜지션, 브레이크포인트는 프론트매터의 `state-opacity`, `motion`, `breakpoints`를 사용합니다.

### Surface 레이어 사용 규칙
5단계 surface 컨테이너는 임의로 고르지 말고 아래 위계를 따릅니다.

- `background` / `surface`: 화면 최하단 배경.
- `surface-container-lowest`(흰색): **콘텐츠 카드의 기본 배경.**
- `surface-container-low`: 카드 내부의 강조 영역, 리스트 아이템 hover 배경.
- `surface-container` ~ `high`: 모달·바텀시트 등 배경 위에 크게 뜨는 면.
- `surface-container-highest`: 입력 필드 등 눌린 느낌이 필요한 오목한 면.
- 위로 뜰수록(카드 → 모달) 한 단계 밝은 값이 아니라 **그림자(shadow)로 깊이를 표현**합니다. 톤은 위 순서대로만 이동시킵니다.

### 폰트 로딩
Quicksand, Plus Jakarta Sans, 그리고 아이콘용 Material Symbols는 시스템에 없으므로 반드시 웹폰트로 로드해야 설계된 느낌이 납니다. 로드하지 않으면 텍스트는 시스템 폰트로, 아이콘은 빈 네모/글자로 폴백되어 밋밋하거나 깨집니다.

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Quicksand:wght@500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
<!-- 아이콘: Material Symbols Rounded (FILL 축 포함) -->
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200&display=block" rel="stylesheet">
```

- 영문/숫자 표시: `Quicksand`
- 한글/본문/데이터: `Plus Jakarta Sans`, 한글 폴백으로 `Pretendard`, 이후 `system-ui`, `sans-serif`.
- `font-family` 예시: `'Plus Jakarta Sans', Pretendard, system-ui, sans-serif`
- 아이콘: `Material Symbols Rounded`. 채움/굵기/크기는 CSS `font-variation-settings`의 `FILL`·`wght`·`opsz` 축으로 제어합니다 (Iconography 섹션 참고). URL 쿼리에 `FILL@...0..1`을 반드시 포함해야 활성 탭 채움이 동작합니다.


## Brand & Style
The design system for icecream is built on a "Soft-Professional" ethos. It balances the playful innocence of early childhood with the structured reliability required for fitness and developmental tracking. The aesthetic is a hybrid of **Minimalism** and **Tactile** design, utilizing high whitespace and soft, pillowy volumes to evoke a sense of safety and tenderness.

The target audience includes parents of children aged 4-6 and physical education professionals. The UI must feel approachable and "gentle like ice cream," avoiding the chaotic energy of typical children's apps in favor of a calm, organized, and growth-oriented atmosphere.

Key Brand Principles:
- **Nurturing Geometry:** Every edge is rounded to remove visual friction.
- **Organic Clarity:** Using soft, natural tones to categorize rigorous health data.
- **Growth Narrative:** Visualizing fitness milestones through a botanical metaphor (Seed to Fruit).

## Colors
The palette is rooted in desaturated pastels that provide a soothing user experience. 구현 시에는 아래 이름 대신 프론트매터의 토큰을 사용합니다.

- **Primary (Mint):** `primary` / `primary-container`. Primary actions, success states, key highlights.
- **Secondary (Soft Coral):** `secondary` / `secondary-container`. Secondary interactive elements and emotional accents.
- **Tertiary (Cream):** `tertiary-container`. Container backgrounds and subtle sectioning.
- **Background:** 프론트매터 `background`(`#faf9f5`)를 사용합니다. 순백 대비 눈부심을 줄인 따뜻한 오프화이트입니다.

**Grade-Specific Colors (Growth Stages):**
접근성을 위해 **항상 해당 아이콘과 텍스트 라벨을 함께** 사용합니다. 색상만으로 등급을 구분하지 않습니다. 구현 시 프론트매터의 `grade-*` 토큰을 사용합니다.

1. **씨앗 (Seed):** `grade-seed` — 초기 기준점(baseline). 기존 `tertiary` 재사용.
2. **새싹 (Sprout):** `grade-sprout` — 초기 성장. 기존 `primary` 재사용.
3. **꽃 (Flower):** `grade-flower` — 유의미한 발달. 기존 `secondary` 재사용.
4. **열매 (Fruit):** `grade-fruit` — 최고 수행. 기존 팔레트에 대응 색이 없어 신규 주황을 추가했습니다.

각 등급은 배지·배경 틴트용으로 `grade-*-container`, 그 위 텍스트용으로 `on-grade-*-container`를 함께 제공합니다. seed/sprout/flower 는 기존 팔레트 토큰의 별칭이므로, 원 토큰(`tertiary`/`primary`/`secondary`)을 수정하면 자동으로 함께 바뀝니다. 색상만으로 등급을 구분하지 말고 반드시 아이콘·텍스트 라벨을 함께 사용하세요 — 특히 seed(올리브)와 flower(코랄)는 원래 브랜드 설명의 "갈색/핑크"와는 톤이 다르므로 라벨 병기가 필수입니다.

## Typography
The typography system prioritizes legibility and a friendly tone.

- **English/Numerical Display:** **Quicksand** — 헤드라인과 숫자에 사용해 부드럽고 둥근 지오메트릭 느낌을 줍니다.
- **Korean/System Text:** **Plus Jakarta Sans** (Pretendard 폴백) — 본문·데이터용의 깔끔하고 가독성 높은 산세리프.
- **Tone of Voice:** 모든 카피는 "해요체"로 — 정중하고 따뜻하며 격려하는 톤. 예: "우리 아이의 성장을 확인해보세요".
- **Scale:** 모바일 우선 화면에서 헤드라인은 28px를 넘지 않습니다.

## Layout & Spacing
This design system uses a **fluid grid** optimized for mobile-first responsiveness.

- **Grid:** 모바일 4컬럼(태블릿/데스크톱에서 12컬럼으로 확장). 브레이크포인트는 프론트매터 `breakpoints`를 사용합니다.
- **Margins:** 모바일 좌우 여백 20px (`spacing.margin-mobile`).
- **Safe Areas:** 노치·홈 인디케이터 대응. 특히 하단 탭바.
- **Spacing Rhythm:** 4px 베이스라인. 요소 그룹 간 16px(`md`), 섹션 세로 간격 24px(`lg`).
- **Touch Targets:** 인터랙티브 요소는 최소 44x44px.

## Elevation & Depth
Depth는 **Tonal Layers**와 **Ambient Shadows**로 표현하며, 강한 아웃라인은 쓰지 않습니다.

- **Surface Layers:** 위의 "Surface 레이어 사용 규칙"을 따릅니다.
- **Shadows:** 프론트매터 `shadow` 토큰을 사용합니다.
  - `shadow.sm`: 카드·작은 버튼.
  - `shadow.md`: 활성 상태·플로팅 요소 (Primary Mint 틴트).
- **Focus:** 이너 섀도우 금지. 깊이는 항상 바깥으로 투사(additive)합니다.

## Shapes
The shape language is defined by hyper-roundedness.

- **Large Components (Cards, Modals):** 최소 24px radius (`rounded.md`).
- **Interactive Elements (Buttons, Inputs):** pill (`rounded.full`).
- **Data Visualizations:** 바 차트·프로그레스 바는 rounded caps.
- **Iconography:** [Material Symbols](https://fonts.google.com/icons) **Rounded** 변형을 사용합니다. Outlined/Sharp가 아니라 Rounded 여야 이 시스템의 hyper-rounded 톤과 맞습니다. AI가 SVG path를 임의로 그리지 말고 아이콘 이름으로 가져옵니다.
  - **축(variation axes) 기본값:** `'wght' 400, 'GRAD' 0, 'opsz' 24`. 아이콘이 두꺼워 보이면 `wght`를 **300**으로 낮춥니다 (지난 버전이 두껍게 보인 원인이 여기입니다).
  - **fill vs 비움 규칙:** Material Symbols는 별도 아이콘이 아니라 하나의 아이콘에서 **`FILL` 축(0~1)**으로 채움을 조절합니다. 기본은 `FILL 0`(외곽선), **선택/활성 상태에서만 `FILL 1`(채움)**. 전환은 `font-variation-settings`로 처리합니다 (아래 Navigation 참고).
  - **크기:** 탭바 24px, 인라인/본문 20px, 소형 16px. `opsz`는 표시 크기에 맞춥니다(20/24 등).

## Components

> 모든 컴포넌트의 색은 프론트매터 토큰으로 지정합니다. 상태 표현은 `state-opacity`, 트랜지션은 `motion`을 사용합니다.

### Buttons
- **Primary:** pill, 배경 `primary-container`, 텍스트 `on-primary-container`. Height 48px 또는 56px.
- **Secondary:** pill, 배경 `secondary-container`, 텍스트 `on-secondary-container`.
- **Ghost:** 배경 없음, 1.5px 보더 `primary`, 텍스트 `primary`.
- **상태:** hover 시 `state-opacity.hover` 오버레이, pressed 시 `state-opacity.pressed`, disabled 시 컨테이너 `state-opacity.disabled-container` · 텍스트 `state-opacity.disabled`.
- **트랜지션:** `motion.duration-fast` + `motion.easing-standard`.

### Navigation (Bottom Tab Bar)
- **Structure:** 4 items (홈, 진단, 기록, 센터).
- **아이콘 상태 (중요):** 선택 여부를 **채움(`FILL`)**으로 구분합니다.
  - **활성(선택) 탭:** `FILL 1`(채워진 아이콘). 뒤에 `primary-container`의 소프트 민트 blob(pill/원형)을 깔고, 아이콘·라벨은 강조 톤(`on-primary-container` 또는 `primary`).
  - **비활성 탭:** `FILL 0`(외곽선 아이콘), 색은 `on-surface-variant`. blob 없음.
  - Material Symbols(Rounded) 이름 예시: 홈=`home`, 진단=`analytics`(또는 `monitoring`), 기록=`edit_note`, 센터=`location_on`. 같은 이름을 쓰고 `FILL` 축만 0↔1로 바꿉니다.
- **라벨:** 아이콘 아래 12px(`label-sm`). 활성은 강조 톤, 비활성은 `on-surface-variant`.
- **전환:** 탭 전환 시 blob 등장/채움 전환에 `motion.duration-base` + `motion.easing-standard`.
- **Blur:** 고불투명 backdrop blur(Glassmorphism)로 가벼운 느낌.

### Cards & Containers
- **Content Cards:** 배경 `surface-container-lowest`(흰색), radius 24px(`rounded.md`), `shadow.sm`.
- **Grade Cards:** 등급 색을 좌측 보더 액센트(`grade-*`) 또는 배경 틴트(`grade-*-container`)로 사용.

### Form Elements
- **Inputs:** 높이 52px, pill, 배경 `surface-container-highest`, 1px 보더 `outline-variant`. 포커스 시 보더 `primary`.
- **Selection:** 체크박스·라디오는 24px로 크게(터치 용이).
- **상태:** disabled는 `state-opacity.disabled`.

### Progress & Grades
- **Growth Tracker:** 씨앗→열매(`grade-seed`→`grade-fruit`) 색 진행을 쓰는 세로/가로 라인.
- **Grade Badges:** 항상 아이콘(예: 새싹 아이콘)과 텍스트("새싹 등급")를 함께 표시해 접근성 확보. 배경 `grade-*-container`, 텍스트 `on-grade-*-container`.
