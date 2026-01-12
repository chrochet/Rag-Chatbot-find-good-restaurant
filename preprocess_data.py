import os, re, pandas as pd
import config # 설정 파일 import
from konlpy.tag import Okt # 형태소 분석기 import

#수집한 데이터를 전처리 
# Okt 형태소 분석기 인스턴스 생성
okt = Okt()

def clean_text(text: str) -> str:
    """요청사항에 맞춘 새로운 텍스트 정제 파이프라인"""
    # 텍스트가 문자열이 아닌 경우 빈 문자열로 변환하여 오류 방지
    if not isinstance(text, str):
        return ""
    
    # 1. HTML 태그 제거 (기존 로직)
    text = re.sub(r"<[^>]*>", "", text)

    # 2. 이모티콘 및 불필요한 특수문자 제거 (한글, 영어, 숫자, 기본 구두점 및 광고 키워드에 필요한 #은 남김)
    text = re.sub(r'[^가-힣ㄱ-ㅎㅏ-ㅣa-zA-Z0-9\s\.,\?!#]', '', text)

    # 3. 형태소 분석 (명사, 형용사 추출)
    # okt.pos(text, stem=True)는 텍스트를 [('단어', '품사'), ...] 형태로 반환하고, 어간을 추출합니다.
    morphs = okt.pos(text, stem=True)
    words = [word for word, pos in morphs if pos in ['Noun', 'Adjective']]

    # 4. 불용어 제거
    # config.py에 정의된 불용어 목록에 없는 단어만 남깁니다.
    words = [word for word in words if word not in config.STOPWORDS and len(word) > 1]

    return ' '.join(words)

def extract_name_from_title(title: str) -> str:
    """'맛집 [가게이름]' 또는 '카페 [가게이름]' 패턴에서 가게이름을 추출합니다."""
    if not isinstance(title, str):
        return ""
    # '맛집' 또는 '카페' 바로 뒤에 오는 한글/영문/숫자 시퀀스를 가게 이름으로 추출
    match = re.search(r"(?:맛집|카페)\s+([가-힣a-zA-Z0-9]+)", title)
    if match:
        return match.group(1)
    return ""

def score_text(text: str) -> int:
    """키워드별 가중치 점수 계산"""
    score = 0
    # config.py에서 키워드 점수표를 가져와 사용
    for word, value in config.KEYWORD_SCORES.items():
        if word in text:
            score += value
    return score

def classify_store(score: int) -> str:
    """점수 기준으로 맛집 / 비맛집 판정"""
    # 이 threshold 값도 config.py로 옮길 수 있지만, 여기서는 유지합니다.
    threshold = 5
    return "맛집" if score >= threshold else "비맛집"

def preprocess_data(input_csv: str, output_csv: str):
    """데이터 전처리 + 점수화 + 라벨링 + 가게이름 추출"""
    print("🔄 데이터 전처리를 시작합니다. 잠시만 기다려주세요...")
    df = pd.read_csv(input_csv)

    # 텍스트 정제 (새로운 clean_text 함수 적용)
    df["description_clean"] = df["description"].astype(str).apply(clean_text)
    
    # 점수 계산 (광고, 협찬 단어가 살아있는 원본 텍스트 기준)
    df["score"] = df["description"].astype(str).apply(score_text)
    
    # 맛집 판별
    df["label"] = df["score"].apply(classify_store)

    # 가게 이름 추출
    df["extracted_name"] = df["title"].astype(str).apply(extract_name_from_title)

    df.to_csv(output_csv, index=False, encoding="utf-8-sig")

    print(f"✅ 전처리 완료: {output_csv}")
    print("--- 라벨 분포 ---")
    print(df["label"].value_counts())
    print("--- 점수 통계 ---")
    print(f"평균점수 {df['score'].mean():.2f}, 최고점 {df['score'].max()}, 최저점 {df['score'].min()}")
    print("--- 가게 이름 추출 예시 ---")
    print(df[df["extracted_name"] != ""]["extracted_name"].head())

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python preprocess_data.py <input_csv_path> <output_csv_path>")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        preprocess_data(input_file, output_file)
