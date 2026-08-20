# webfont

웹 폰트 모음집

## 생성 도구 사용 방법 (UV)

### 도움말

```bash
uv run wfgen.py --help
```

### 전체 폰트 생성 (Full + Subset)

```bash
uv run wfgen.py --all --both
```

### 특정 폰트만 생성

```bash
uv run wfgen.py --font="Noto Sans KR" --subset
uv run wfgen.py --font="RIDI Batang" --full
```

### 대화형 모드

인자를 생략하면 폰트/생성 모드를 순서대로 선택할 수 있습니다.

```bash
uv run wfgen.py
```

### 사전 준비

- `fonts-original/` 경로에 원본 폰트 파일이 있어야 합니다.
- subset 생성 시 `glyphs/glyphs.txt`가 필요합니다.
- Git 저장소라면 다음 명령으로 서브모듈을 먼저 준비하세요.

```bash
git submodule update --init --recursive
```

## 사용 방법

### 구름 산스 코드

각 버전의 `font-family`는 다음과 같습니다.

* 일반 버전: `goorm-sans-code`
* 서브셋 버전: `goorm-sans-code-subset`

#### 로컬 설치 버전

```html
<link href="/path/to/goorm-sans-code-local.css" rel="stylesheet">
<link href="/path/to/goorm-sans-code-subset-local.css" rel="stylesheet">
```

```css
@import url('/path/to/goorm-sans-code-local.css');
@import url('/path/to/goorm-sans-code-subset-local.css');
```

#### 웹 (jsDelivr)

```html
<link href="//cdn.jsdelivr.net/gh/TetraTheta/webfont/dist/goorm-sans-code-web.css" rel="stylesheet">
<link href="//cdn.jsdelivr.net/gh/TetraTheta/webfont/dist/goorm-sans-code-subset-web.css" rel="stylesheet">
```

```css
@import url('//cdn.jsdelivr.net/gh/TetraTheta/webfont/dist/goorm-sans-code-web.css');
@import url('//cdn.jsdelivr.net/gh/TetraTheta/webfont/dist/goorm-sans-code-subset-web.css');
```

### 리디바탕

각 버전의 `font-family`는 다음과 같습니다.

* 일반 버전: `ridi-batang`
* 서브셋 버전: `ridi-batang-subset`

#### 로컬 설치 버전

```html
<link href="/path/to/ridi-batang-local.css" rel="stylesheet">
<link href="/path/to/ridi-batang-subset-local.css" rel="stylesheet">
```

```css
@import url('/path/to/ridi-batang-local.css');
@import url('/path/to/ridi-batang-subset-local.css');
```

#### 웹 (jsDelivr)

```html
<link href="//cdn.jsdelivr.net/gh/TetraTheta/webfont/dist/ridi-batang-web.css" rel="stylesheet">
<link href="//cdn.jsdelivr.net/gh/TetraTheta/webfont/dist/ridi-batang-subset-web.css" rel="stylesheet">
```

```css
@import url('//cdn.jsdelivr.net/gh/TetraTheta/webfont/dist/ridi-batang-web.css');
@import url('//cdn.jsdelivr.net/gh/TetraTheta/webfont/dist/ridi-batang-subset-web.css');
```

### 본고딕 (Noto Sans KR)

각 버전의 `font-family`는 다음과 같습니다.

* 일반 버전: `noto-sans-kr`
* 서브셋 버전: `noto-sans-kr-subset`

#### 로컬 설치 버전

```html
<link href="/path/to/noto-sans-kr-local.css" rel="stylesheet">
<link href="/path/to/noto-sans-kr-subset-local.css" rel="stylesheet">
```

```css
@import url('/path/to/noto-sans-kr-local.css');
@import url('/path/to/noto-sans-kr-subset-local.css');
```

#### 웹 (jsDelivr)

```html
<link href="//cdn.jsdelivr.net/gh/TetraTheta/webfont/dist/noto-sans-kr-web.css" rel="stylesheet">
<link href="//cdn.jsdelivr.net/gh/TetraTheta/webfont/dist/noto-sans-kr-subset-web.css" rel="stylesheet">
```

```css
@import url('//cdn.jsdelivr.net/gh/TetraTheta/webfont/dist/noto-sans-kr-web.css');
@import url('//cdn.jsdelivr.net/gh/TetraTheta/webfont/dist/noto-sans-kr-subset-web.css');
```
