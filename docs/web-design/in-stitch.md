# 아이쑥크림 — Stitch 디자인 프롬프트

## 사용법
1. 먼저 아래 **[Global Theme]**를 입력해 앱 전체 스타일을 잡습니다.
2. 그다음 각 화면 프롬프트를 하나씩 입력해 화면을 생성합니다.
3. 화면 문구(한글 카피)는 그대로 두고, 지시문(영어)만 Stitch에 전달하면 됩니다.

---

## [Global Theme] — 먼저 입력

```
Design a mobile-first responsive web app called "icecream" (always lowercase), 
a child fitness management service for parents of preschoolers aged 4–6.

Overall mood: soft, warm, friendly, and trustworthy — like ice cream: gentle and 
tender, but clean and organized, not childish, since it presents official national 
fitness standards.

Color palette: pastel-based. Mint, cream, and soft coral as primary tones. 
White-to-cream backgrounds with generous whitespace. 
Grade color coding: Seed (soft brown), Sprout (light green), Flower (coral/pink), 
Fruit (warm red-orange).

Typography: rounded sans-serif, highly legible and friendly. Korean text uses 
Pretendard-style font.

Shapes: large rounded corners, soft shadows, roomy padding, pill-shaped buttons. 
Avoid sharp edges.

Navigation: bottom tab bar with 4 tabs — 홈 (Home), 진단 (Diagnosis), 기록 (Records), 
센터 (Centers).

Touch targets minimum 44px. Number inputs are large and keypad-friendly.
Accessibility: never rely on color alone — grades always combine color + icon + text.
Copy tone: warm, easy, encouraging Korean. Growth-framed, never judgmental toward the child.
```

---

## 화면 1 — 온보딩 / 자녀 등록

```
Create an onboarding and child profile registration screen.
- Top: friendly one-line intro of the service + a large primary CTA button 
  labeled "우리 아이 등록하고 시작하기".
- Child registration form: nickname input, gender toggle (남/여), 
  birth month picker with auto-calculated age in months displayed.
- Inline warning text if age is outside 48–83 months: "유아기 측정 대상 범위 밖이에요".
- Support multiple children: avatar chips at top to switch between children.
Use soft pastel cards with rounded corners.
```

## 화면 2 — 홈 대시보드

```
Create a home dashboard screen.
- Top: selected child's avatar + large current overall grade badge 
  (Seed/Sprout/Flower/Fruit as a cute illustration).
- Recent measurement summary card: last measured date, 1–2 strength tags 
  and 1–2 weakness tags.
- Action cards in a vertical list: "체력 진단하기", "근처 센터 찾기", 
  "우리 동네 참여 현황".
- If weaknesses exist, a preview card "이런 활동 어때요?" with a recommended activity thumbnail.
Warm, spacious layout with pastel cards.
```

## 화면 3 — 진단 입력

```
Create a fitness measurement input screen.
- Top toggle: measurement type "정식 측정" / "자가측정(참고용)". 
  When 자가측정 is selected, show a persistent "참고용" badge.
- A list of 8 input cards, each with item name + unit + a large number input field:
  심폐지구력 (10m 왕복오래달리기, 회) / 근력 (상대악력, %) / 근지구력 (윗몸말아올리기, 회) / 
  유연성 (앉아윗몸앞으로굽히기, cm) / 민첩성 (5m×4 왕복달리기, 초) / 
  순발력 (제자리멀리뛰기, cm) / 협응력 (3×3 버튼누르기, 초) / 신체조성 (BMI).
- Each card has a small "측정 방법 보기" secondary link. Partial input is allowed.
- Fixed bottom button: "진단 결과 보기".
```

## 화면 4 — 진단 결과

```
Create a diagnosis result screen.
- Top: large overall grade badge (Seed/Sprout/Flower/Fruit) + one encouraging comment line.
- Strength/weakness profile as a radar chart (or per-item bars): strengths highlighted, 
  weaknesses marked with a "개선 필요" tag.
- Each weakness card has an entry point button "이 활동 추천받기".
- A prominent CTA "무료로 정식 측정 받기" linking to center connect.
- Encouraging, non-judgmental tone. Growth framing (seed to fruit).
```

## 화면 5 — 센터 연계

```
Create a nearby fitness certification center screen.
- Region selector or current-location based list of nearby centers, sorted by distance.
- Each center card shows: center name, address, distance, a "유아 무료 측정 가능" badge, 
  and a "예약하기" button.
- Include a map/list view toggle.
Clean pastel cards, clear distance hierarchy.
```

## 화면 6 — 기록 & 성장 추적

```
Create a records and growth tracking screen.
- Measurement history list: by date, each with a 정식/자가 type badge.
- Growth trend chart over time: official values as solid line with filled dots, 
  self-measured values as dashed line with faded dots — visually distinct in one chart.
- Item filter selector. Add grade background bands and baseline so the chart 
  looks meaningful even with few data points.
```

## 화면 7 — 활동 추천

```
Create an activity recommendation screen.
- Exercise content cards grouped by weakness fitness element 
  (thumbnail + title + fitness-element tag).
- If arriving from a diagnosis result, the relevant weakness element is shown at the top first.
Warm, encouraging layout.
```

## 화면 8 — 지역 참여 인사이트

```
Create a regional participation insight screen.
- Primary insight card with one sentence like: 
  "OO구의 유아 체력측정 참여는 전국 평균보다 낮은 편이에요. 가까운 센터에서 무료로 측정해보세요." 
  plus a center-connect button.
- Optional expansion: a district participation-rate map (color-coded) or ranking bars. 
  If data is missing, gracefully fall back to just the insight card.
```

## 한국어 유지

Keep all Korean text exactly as written, do not translate to English
