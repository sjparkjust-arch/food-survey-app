# 🍽️ 좋아하는 음식 종류 설문조사

> Python과 MariaDB를 연동한 음식 종류 설문조사 프로그램

---

<details>
<summary>🛠️ 사용 기술</summary>

| 항목 | 내용 |
|------|------|
| 언어 | Python |
| 데이터베이스 | MariaDB |
| 라이브러리 | pymysql |

</details>

<details>
<summary>🗄️ DB 설계</summary>

| 테이블 | 설명 |
|--------|------|
| users | 회원 정보 (nickname, password, age, gender) |
| survey | 투표 데이터 (nickname, food, voted_at) |
| cancel_log | 취소 기록 (nickname, food, canceled_at) |

</details>

<details>
<summary>✅ 주요 기능</summary>

1. 회원가입 - 한글 실명, 숫자 4자리 비밀번호
2. 로그인 - 이름+나이+성별+비밀번호 인증
3. 설문 참여 - 1인 1표, 중복 투표 방지
4. 설문 현황보기 - 득표수, 퍼센트, 1위, 성별/연령대 통계
5. 내 투표 기록 보기
6. 내 투표 취소 - 취소 기록 DB 저장
7. 로그아웃

</details>

<details>
<summary>🚀 실행 방법</summary>

1. MariaDB 서버 실행
2. `python meal_research.py` 실행

</details>

## 🚀 실행 방법
1. MariaDB 서버 실행
2. `python meal_research.py` 실행
