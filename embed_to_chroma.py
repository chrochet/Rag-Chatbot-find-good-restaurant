import os
import sys
import pandas as pd
from dotenv import load_dotenv

from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def build_chroma(csv_path: str, persist_directory: str) -> None:
    df = pd.read_csv(csv_path)

    # 🔹 데이터 확인
    required_cols = ["title", "description", "description_clean", "score", "label", "extracted_name"]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(
            f"❌ CSV 파일에 필요한 컬럼이 없습니다.\n"
            f"- 누락된 컬럼: {missing}\n"
            f"- 필요한 컬럼 전체: {required_cols}"
        )

    # 🔹 검색용 텍스트 생성
    df["search_text"] = (
        df["title"].fillna("").astype(str) + " " +
        df["description"].fillna("").astype(str) + " " +
        df["description_clean"].fillna("").astype(str)
    )

    # 🔹 텍스트 분할기 (RAG용)
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)

    # 🔹 메타데이터 생성 (NaN → "")
    metadatas = [
        {"score": s, "label": l, "extracted_name": en}
        for s, l, en in zip(
            df["score"],
            df["label"],
            df["extracted_name"].fillna("").astype(str)
        )
    ]

    docs = splitter.create_documents(
        texts=df["search_text"].tolist(),
        metadatas=metadatas
    )

    # 🔹 OpenAI 임베딩 모델
    if not OPENAI_API_KEY:
        raise ValueError("❌ OPENAI_API_KEY가 설정되어 있지 않습니다. (.env 확인)")

    emb = OpenAIEmbeddings(
        model="text-embedding-3-small",
        api_key=OPENAI_API_KEY,
    )

    # 🔹 ChromaDB에 저장
    db = Chroma.from_documents(
        documents=docs,
        embedding=emb,
        persist_directory=persist_directory,
    )

    # 버전에 따라 persist가 있을 수도/없을 수도 있어서 방어
    if hasattr(db, "persist"):
        db.persist()

    print(f"✅ ChromaDB 구축 및 저장 완료 ({len(df)}건 저장됨)")
    print(f"📂 저장 경로: {persist_directory}/")


if __name__ == "__main__":
    # ✅ 편의 기능:
    # - 인자 1개: csv_path만 주면 persist_directory는 기본값 vectordb4
    # - 인자 2개: csv_path + persist_directory (기존 방식)
    if len(sys.argv) == 2:
        csv_path = sys.argv[1]
        persist_directory = "vectordb4"
        print("ℹ️ 저장 디렉토리를 입력하지 않아 기본값 'vectordb4'를 사용합니다.")
        print(f"   예) python embed_to_chroma.py {csv_path} vectordb4")

    elif len(sys.argv) == 3:
        csv_path = sys.argv[1]
        persist_directory = sys.argv[2]

    else:
        print("사용법: python embed_to_chroma.py <csv_경로> [저장_디렉토리]")
        print("예시1: python embed_to_chroma.py data/naver_blog_bigdata_cleaned4.csv")
        print("예시2: python embed_to_chroma.py data/naver_blog_bigdata_cleaned4.csv vectordb4")
        sys.exit(1)

    if not os.path.exists(csv_path):
        print(f"❌ {csv_path} 파일이 없습니다. 먼저 preprocess_data.py를 실행하세요.")
        sys.exit(1)

    os.makedirs(persist_directory, exist_ok=True)
    build_chroma(csv_path, persist_directory)
