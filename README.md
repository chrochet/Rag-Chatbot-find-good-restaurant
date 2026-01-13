# 🍽️ Rag-Chatbot---hole-in-the-wall
**Streamlit 기반 RAG 맛집 판별 AI Chatbot**

---

## 🖥️ 프로젝트 소개
본 프로젝트는 사용자가 입력한 **가게명/후기 정보**를 바탕으로  
**RAG(Retrieval-Augmented Generation)** 기반으로 데이터를 검색하고,  
LLM이 근거 기반으로 맛집 여부를 판단해주는 **맛집 판별 AI 챗봇**입니다.

---

## 🕰️ 개발 기간
- 2025.10.16 ~ 2025.11.7

---

## 🧑‍🤝‍🧑 멤버 구성
- 개인 프로젝트 (1인 개발)
- 아이디어보조 

---

## ⚙️ 개발 환경
- **Python** 3.11+  
- **IDE** : VSCode / PyCharm  
- **Frontend** : Streamlit  
- **Vector DB** : ChromaDB  
- **LLM API** : OpenAI API  
- **Framework / Library**
  - `streamlit`
  - `langchain`
  - `langchain-chroma`
  - `langchain-openai`
  - `chromadb`
  - `httpx`

---

## 📁 프로젝트 구조
```bash
.
├── app_streamlit4.py          # Streamlit UI 실행 파일
├── main_v4.py                 # RAG 로직 (Retriever + LLM)
├── big_data_collector.py      # Naver API 기반 데이터 수집
├── preprocess_data.py         # 데이터 전처리
├── embed_to_chroma.py         # Embedding + ChromaDB 생성
├── config.py                  # 설정값 관리
├── requirements.txt
├── runtime.txt
├── .gitignore
├── .env.example
└── (vectordb4 / vectordb5)    # 로컬에서 생성되는 ChromaDB (Git 제외)
```
---

## 📌 주요 기능

### ✅ 1. 맛집 판별 RAG Chatbot
- [상세보기](https://github.com/USERNAME/REPO/wiki/01.-RAG-%EB%A7%9B%EC%A7%91-%ED%8C%90%EB%B3%84-Chatbot) · [WIKI 이동](https://github.com/USERNAME/REPO/wiki)
- 사용자가 입력한 가게명/키워드를 기반으로 맛집 여부를 판단하는 RAG 챗봇
- Retriever(ChromaDB)로 관련 문서/후기를 검색한 뒤, LLM이 근거 기반으로 답변 생성
- 결과는 "맛집 / 비맛집 / 정보부족" 등으로 구조화된 형태로 출력 가능

---

### ✅ 2. 데이터 수집 (Naver API)
- [상세보기](https://github.com/USERNAME/REPO/wiki/02.-Naver-API-%EB%8D%B0%EC%9D%B4%ED%84%B0-%EC%88%98%EC%A7%91) · [WIKI 이동](https://github.com/USERNAME/REPO/wiki)
- Naver API를 통해 가게/후기/블로그/리뷰 등 맛집 관련 텍스트 데이터를 수집
- 수집 데이터는 RAG 지식베이스 구축을 위한 원천 데이터로 활용

---

### ✅ 3. 전처리 파이프라인
- [상세보기](https://github.com/USERNAME/REPO/wiki/03.-%EC%A0%84%EC%B2%98%EB%A6%AC-%ED%8C%8C%EC%9D%B4%ED%94%84%EB%9D%BC%EC%9D%B8) · [WIKI 이동](https://github.com/USERNAME/REPO/wiki)
- 수집된 원천 데이터 정제(결측/중복 제거, 텍스트 클리닝)
- RAG에 적합하도록 문서 형태로 정규화
- 임베딩/벡터화 전에 품질을 일정하게 맞추는 역할

---

### ✅ 4. 임베딩 & ChromaDB(Vector DB) 구축
- [상세보기](https://github.com/USERNAME/REPO/wiki/04.-Embedding-&-ChromaDB-%EA%B5%AC%EC%B6%95) · [WIKI 이동](https://github.com/USERNAME/REPO/wiki)
- 전처리된 텍스트를 임베딩하여 Vector로 변환
- ChromaDB에 저장하여 유사도 기반 검색 가능
- `vectordb4`, `vectordb5` 등 로컬 DB 폴더로 관리 (GitHub 업로드 제외)

---

### ✅ 5. Streamlit UI 기반 판별 시스템
- [상세보기](https://github.com/USERNAME/REPO/wiki/05.-Streamlit-UI-%EA%B5%AC%EC%84%B1) · [WIKI 이동](https://github.com/USERNAME/REPO/wiki)
- Streamlit으로 입력/버튼/결과 영역이 있는 간단한 웹 UI 제공
- 사용자가 가게명을 입력 → "판별 시작" 클릭 → 결과 출력 흐름

---

### ✅ 6. 이전 검색 결과 잔상 문제 해결 (Session State)
- [상세보기](https://github.com/USERNAME/REPO/wiki/06.-Session-State-%EC%9E%94%EC%83%81-%EB%AC%B8%EC%A0%9C-%ED%95%B4%EA%B2%B0) · [WIKI 이동](https://github.com/USERNAME/REPO/wiki)
- Streamlit 특성상 입력 변경 시 이전 결과가 남는 문제 해결
- `st.session_state.last_query`, `st.session_state.last_result` 사용
- 입력값이 바뀌면 이전 결과를 자동 삭제하여 UI 혼동 방지

---

### ✅ 7. DOM removeChild 에러 방지 (출력 영역 안전화)
- [상세보기](https://github.com/USERNAME/REPO/wiki/07.-DOM-removeChild-%EC%97%90%EB%9F%AC-%EB%B0%A9%EC%A7%80) · [WIKI 이동](https://github.com/USERNAME/REPO/wiki)
- 결과 출력 영역을 `st.empty()`로 분리하여 DOM 충돌 방지
- `result_box = st.empty()` 형태로 안정적인 결과 렌더링 구현

---

### ✅ 8. vectordb 자동 탐색 기능
- [상세보기](https://github.com/USERNAME/REPO/wiki/08.-vectordb-%EC%9E%90%EB%8F%99-%ED%83%90%EC%83%89) · [WIKI 이동](https://github.com/USERNAME/REPO/wiki)
- 환경 변수 `VDB_DIR`가 있으면 해당 경로 사용
- 없으면 `vectordb4` → 없으면 `vectordb5` 순으로 자동 탐색
- 둘 다 없으면 `embed_to_chroma.py` 실행 안내 출력
