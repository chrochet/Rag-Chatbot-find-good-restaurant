import os
import streamlit as st
from main_v4 import run_rag
import config

st.set_page_config(
    page_title="맛집 판별 AI",
    page_icon="🍚",
)

st.title("🍚 맛집 판별 AI ")

st.markdown("""안녕하세요! 저는 맛집 판별 AI입니다.  
판별하고자 하는 가게 이름을 입력하고 '판별 시작' 버튼을 눌러주세요.
(리뷰 데이터가 없는 식당은 판별이 불가능할 수 있습니다)
""")

# =========================
# ✅ VectorDB 경로 자동 설정
# =========================
VDB_DIR = os.getenv("VDB_DIR")

if VDB_DIR:
    vectordb_path = VDB_DIR
elif os.path.isdir("vectordb4"):
    vectordb_path = "vectordb4"
elif os.path.isdir("vectordb5"):
    vectordb_path = "vectordb5"
else:
    vectordb_path = None

with st.expander("⚙️ 설정(현재 사용 중인 벡터DB)"):
    if vectordb_path:
        st.write(f"✅ vectordb_path = `{vectordb_path}`")
        if VDB_DIR:
            st.caption("환경변수 VDB_DIR로 지정된 경로를 사용 중입니다.")
        else:
            st.caption("폴더 자동 탐색으로 vectordb를 선택했습니다.")
    else:
        st.error("❌ vectordb 폴더를 찾지 못했습니다. embed_to_chroma.py로 먼저 생성해주세요.")
        st.code("python embed_to_chroma.py <cleaned_csv_path> vectordb4", language="bash")

# =========================
# ✅ 세션 상태
# =========================
if "last_query" not in st.session_state:
    st.session_state.last_query = ""
if "last_result" not in st.session_state:
    st.session_state.last_result = ""

store_name = st.text_input("가게 이름", placeholder="예: 가타쯔무리, 만득이네")
branch_name = ""

if store_name in config.CHAIN_RESTAURANTS:
    branch_name = st.text_input("지점명", placeholder="예: 강남점 (체인점은 지점명을 입력해주세요)")

final_query = store_name.strip()
if branch_name.strip():
    final_query = f"{store_name.strip()} {branch_name.strip()}"

# ✅ 입력이 바뀌면 이전 결과 삭제
if final_query != st.session_state.last_query:
    st.session_state.last_result = ""

if st.button("판별 시작"):
    if not store_name:
        st.warning("가게 이름을 입력해주세요.")
    else:
        if vectordb_path is None:
            st.error("❌ 벡터DB(vectordb4)가 아직 없습니다. 먼저 embed_to_chroma.py를 실행해 DB를 생성해주세요.")
            st.code("python embed_to_chroma.py <cleaned_csv_path> vectordb4", language="bash")
            st.stop()

        with st.spinner(f"'{final_query}'에 대한 리뷰를 분석 중입니다... 잠시만 기다려주세요."):
            result = run_rag(final_query, vectordb_path=vectordb_path)
            st.session_state.last_query = final_query
            st.session_state.last_result = result

# ✅ 결과 영역을 입력/버튼 아래에 고정 (위치만 변경)
result_box = st.empty()

# ✅ 결과는 placeholder에만 렌더링
if st.session_state.last_result:
    result_box.divider()
    result_box.markdown(st.session_state.last_result)
else:
    result_box.empty()
