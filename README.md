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

### 1. Streamlit 맛집 판별 UI (app_streamlit4.py)
[상세보기 · WIKI](https://github.com/USERNAME/REPO/wiki)
- 사용자 입력(가게명) 기반으로 판별을 실행하고 결과를 화면에 출력

### 2. RAG 판별 로직 구성 (main_v4.py)
[상세보기 · WIKI](https://github.com/USERNAME/REPO/wiki)
- Retriever(ChromaDB)로 관련 문서를 검색하고, LLM이 근거 기반으로 맛집/비맛집 판단 생성

### 3. Naver API 데이터 수집 (big_data_collector.py)
[상세보기 · WIKI](https://github.com/USERNAME/REPO/wiki)
- 네이버 API로 리뷰/블로그 데이터를 수집하여 RAG 학습용 원천 데이터 구축

### 4. 데이터 전처리 파이프라인 (preprocess_data.py)
[상세보기 · WIKI](https://github.com/USERNAME/REPO/wiki)
- 중복 제거, 텍스트 정제 등을 수행하여 검색 품질을 높일 수 있도록 문서를 표준화

### 5. Embedding + Vector DB 구축 (embed_to_chroma.py)
[상세보기 · WIKI](https://github.com/USERNAME/REPO/wiki)
- 전처리 데이터를 임베딩하여 ChromaDB에 저장하고, 유사도 기반 검색 환경 구성

### 6. 설정 및 판별 기준 관리 (config.py)
[상세보기 · WIKI](https://github.com/USERNAME/REPO/wiki)
- API 키, DB 경로, 프롬프트 및 맛집 판별 기준을 설정 파일로 관리

- [상세보기](https://github.com/USERNAME/REPO/wiki/Config-&-Criteria) · [WIKI](https://github.com/USERNAME/REPO/wiki)
- API 키, DB 경로, 프롬프트 및 맛집 판별 기준을 설정 파일로 관리
