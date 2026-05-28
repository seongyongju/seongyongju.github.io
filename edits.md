# 사이트 수정 가이드

이 사이트의 콘텐츠·디자인을 어디서 어떻게 고치는지 정리한 문서입니다.

> 변경 후 로컬에서 미리 보려면: `export PATH="/opt/homebrew/opt/ruby@3.1/bin:$PATH" && bundle exec jekyll serve`
> → http://127.0.0.1:4000/ 에서 확인. `_data/`·`_pages/`·`_sass/`는 자동 리로드, `_config.yml`은 서버 재시작 필요.

---

## 1. 메뉴 (네비게이션 바)

상단 메뉴는 `_data/navigation.yml` 한 곳에서 관리합니다.

```yaml
main:
  - title: "Publications"
    url: /publications/
  - title: "Research"
    url: /research/
  - title: "Posts"
    url: /posts/
  - title: "CV"
    url: /cv/
```

- 항목 추가/삭제는 위 블록에 줄을 추가/삭제하면 됨
- `url` 은 해당 페이지의 `permalink` 와 일치해야 함

---

## 2. 카테고리별 페이지

| 카테고리 | 수정할 파일 | 설명 |
|---|---|---|
| **About (홈)** | `_pages/about.md` | 첫 화면에 보이는 자기소개 본문 |
| **Publications** | `_pages/publications.md` | 논문/학회 발표 목록 |
| **Research** | `_pages/research.md` | 연구 관심사·진행 중 연구·과거 연구 |
| **CV** | `_pages/cv.md` | 이력 요약 + PDF 다운로드 버튼 |
| **Posts (블로그)** | `_posts/YYYY-MM-DD-제목.md` | 블로그 글, 파일명 규칙 엄수 |

### 2-1. Publications 양식

`_pages/publications.md`:
```markdown
## Under Review
1. **논문 제목**

## Conferences
1. **논문 제목**. *학회명*, 연도.

## Software Registrations
1. **소프트웨어 이름**. 등록기관 (등록번호), 연도.
```

### 2-2. Research 양식

`_pages/research.md`:
```markdown
## Interests
한 줄 요약 문단.

## Current
- **연구 제목** (펀딩/협력기관), 소속 랩. 시작 – Present

## Past
- **연구 제목**, 소속 랩. 기간
```

### 2-3. CV 양식

`_pages/cv.md` 는 한 줄 요약 + 상세는 `files/CV_SeongyongJu.pdf` 로 위임:
```markdown
## Education
- **학교명**, 학위. 기간

## Research Experience
- **소속**, 랩 이름 (PI: 교수명). 기간

## Honors & Patents
- **상 이름**, 주최기관. 날짜

## External Activities
- **활동명**, 기관. 기간
```

CV PDF 교체: `files/CV_SeongyongJu.pdf` 파일을 같은 이름으로 덮어쓰면 됨. (이름을 바꾸려면 `_pages/cv.md` 의 `<a href=".../files/...pdf">` 부분도 같이 수정)

### 2-4. Posts (블로그)

새 글: `_posts/2026-05-09-제목.md` 형식으로 파일 생성.
```markdown
---
title: '글 제목'
date: 2026-05-09
permalink: /posts/2026/05/blog-post-title/
tags:
  - 태그1
  - 태그2
---

본문 마크다운...
```

초안: `_drafts/` 에 두면 빌드에 안 들어감.

---

## 3. 사이드바 / 프로필

### 3-1. 프로필 정보 (이름·소속·이메일·소셜링크)

**`_config.yml`** 의 `author:` 블록에서 모두 관리합니다.

```yaml
author:
  name: "Seongyong Ju"
  avatar: "profile.png"            # images/profile.png
  bio: "BS - Industrial Security"  # 이름 아래 한 줄 소개
  employer: "Chung-Ang University"
  email: "jusy4901@cau.ac.kr"
  uri: "http://sor.snu.ac.kr/"     # "Website" 링크 — 라벨은 ui-text.yml 에서 변경
  github: "seongyongju"
  googlescholar:                   # 비워두면 표시 안 됨
  linkedin:
  orcid:
  # ... 그 외 소셜 항목들
```

- 항목을 비워두면 사이드바에 자동으로 안 뜸
- 아바타 이미지는 `images/profile.png` 를 같은 이름으로 덮어쓰기

### 3-2. "Website" 라벨 (현재 "SNU SOR")

`_data/ui-text.yml` line 27:
```yaml
website_label              : "SNU SOR"
```
- 표시 라벨 변경은 여기, 링크 자체는 위 `_config.yml` 의 `uri:` 에서

### 3-3. 사이드바 레이아웃·CSS

| 무엇을 바꾸나 | 어디서 |
|---|---|
| 사이드바 표시 조건 (페이지별 노출 여부) | `_includes/sidebar.html` |
| 프로필 카드 HTML 구조 | `_includes/author-profile.html` |
| 프로필 사진 호버 효과 (현재 0.55 → 1.0) | `_sass/_sidebar.scss` line ~85 |
| 사이드바 너비·sticky 동작 | `_sass/_sidebar.scss` 상단 |
| 전역 색상·폰트 | `_sass/_variables.scss` |

예: 프로필 사진 호버 진하기 조정 (`_sass/_sidebar.scss`):
```scss
img {
  opacity: 0.55;        // 평소 — 낮을수록 더 흐림 (0.3~0.7 권장)
  transition: opacity 0.3s ease-in-out;
  &:hover { opacity: 1; }
}
```

---

## 4. 파일 / 이미지 업로드

| 무엇을 | 어디에 | URL |
|---|---|---|
| PDF·다운로드 자료 | `files/` | `/files/파일명.pdf` |
| 본문 이미지·아이콘 | `images/` | `/images/파일명.png` |

링크 걸 때는 `{{ base_path }}/files/...` 또는 `{{ base_path }}/images/...` 형식 사용.

---

## 5. 사이트 기본 설정 (제목·URL·분석)

`_config.yml` 상단:
- `title:` — 브라우저 탭 제목
- `description:` — SEO 설명문
- `url:` — 배포 도메인 (변경 비추천)
- `repository:` — GitHub 저장소 (변경 비추천)
- `google_analytics` 블록 — 분석 ID

`_config.yml` 변경 후에는 **Jekyll 서버 재시작 필요** (다른 파일들은 자동 리로드).
