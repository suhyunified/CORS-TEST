# CORS 테스트용 최소 환경 (a.com -> b.com API)

S3 + CloudFront로 React 정적 사이트를 배포 중일 때,
`a.com`(프론트)에서 `b.com`(API) 호출 시 나는 CORS 문제를 로컬에서 간단히 재현/검증할 수 있는 최소 예제입니다.

이 저장소는 의도적으로 **서로 다른 Origin**(포트가 다른 두 서버)을 사용해 CORS 상황을 만듭니다.

- 프론트 서버: `http://localhost:3000` (a.com 역할)
- 백엔드 서버: `http://localhost:4000` (b.com 역할)

---

## 구성

- `frontend/`
  - `index.html`: fetch 호출 버튼과 결과 표시 UI
  - `server.py`: 정적 파일 서버 (`localhost:3000`)
- `backend/`
  - `server.py`: CORS ON/OFF 가능한 API 서버 (`localhost:4000`)

---

## 빠른 시작

### 1) 백엔드 실행 (터미널 1)

```bash
python3 backend/server.py
```

기본값은 CORS가 꺼진 상태입니다 (`ALLOW_ORIGIN` 미설정).

### 2) 프론트 실행 (터미널 2)

```bash
python3 frontend/server.py
```

### 3) 브라우저에서 확인

`http://localhost:3000` 접속 후:

- `Call API (Simple GET)` 버튼 클릭
- `Call API (Preflight: custom header)` 버튼 클릭

기본 상태(CORS OFF)에서는 브라우저 콘솔/화면에서 CORS 에러를 확인할 수 있습니다.

---

## CORS 허용으로 바꿔보기

백엔드 실행 시 허용 Origin 지정:

```bash
ALLOW_ORIGIN=http://localhost:3000 python3 backend/server.py
```

그 다음 프론트에서 다시 호출하면 성공 응답을 확인할 수 있습니다.

> `ALLOW_ORIGIN=*` 로 설정하면 와일드카드 허용도 테스트할 수 있습니다.

---

## preflight 검증용 curl

```bash
curl -i -X OPTIONS 'http://localhost:4000/api/hello' \
  -H 'Origin: http://localhost:3000' \
  -H 'Access-Control-Request-Method: GET' \
  -H 'Access-Control-Request-Headers: X-Demo-Header, Content-Type'
```

응답 헤더에서 아래 값을 확인하세요.

- `Access-Control-Allow-Origin`
- `Access-Control-Allow-Methods`
- `Access-Control-Allow-Headers`

---

## 실제 S3 + CloudFront 환경에서 체크 포인트

1. **CORS는 API 응답에서 맞춰야 함**
   - S3/CloudFront의 프론트 배포 설정과 별개로, 최종 API 응답 헤더에 CORS가 정확히 있어야 합니다.

2. **CloudFront를 API 앞에 둔 경우**
   - `Origin` 헤더를 오리진으로 전달하도록 정책(Origin Request Policy) 확인
   - OPTIONS 메서드 허용 여부 확인
   - 캐시 정책 때문에 CORS 헤더가 섞이지 않도록 `Origin` 기준 캐시 분리 필요 여부 확인

3. **쿠키/인증 사용 시**
   - `Access-Control-Allow-Credentials: true` 필요
   - 이 경우 `Access-Control-Allow-Origin: *` 사용 불가 (명시 Origin 필요)

4. **프론트에서 커스텀 헤더 사용 시**
   - preflight가 발생하므로 서버에서 OPTIONS 응답을 정확히 처리해야 함

---

## React 앱에 붙일 때

React에서는 버튼 클릭 로직을 그대로 컴포넌트에 넣어 테스트할 수 있습니다.
핵심은 브라우저 개발자도구 Network 탭에서

- 실제 요청(GET/POST)
- preflight(OPTIONS)
- 응답의 CORS 헤더

3가지를 함께 확인하는 것입니다.
