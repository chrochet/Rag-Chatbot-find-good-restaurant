import os, json, urllib.request, urllib.parse, pandas as pd
from dotenv import load_dotenv
from time import sleep
import re

# 데이터 수집하는 파일 
load_dotenv()
NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")

regions = ["서울", "부산", "인천", "대전", "광주"]
categories = ["보쌈", "카페", "한식", "술집", "분식", "중식", "양식"]

queries = []
for region in regions:
    for cat in categories:
        queries.append({'query': f'{region} {cat}', 'region': region, 'category': cat})
queries.append({'query': '명지대 부근 맛집', 'region': '서울', 'category': '맛집'})

# 사용자 요청에 따라 남가좌동 및 명지대(서울인문캠) 위주로 쿼리 추가
queries.append({'query': '남가좌동 맛집', 'region': '서울', 'category': '맛집'})
queries.append({'query': '남가좌동 보쌈', 'region': '서울', 'category': '보쌈'})
queries.append({'query': '남가좌동 카페', 'region': '서울', 'category': '카페'})
queries.append({'query': '남가좌동 한식', 'region': '서울', 'category': '한식'})
queries.append({'query': '남가좌동 술집', 'region': '서울', 'category': '술집'})
queries.append({'query': '남가좌동 분식', 'region': '서울', 'category': '분식'})
queries.append({'query': '남가좌동 중식', 'region': '서울', 'category': '중식'})
queries.append({'query': '남가좌동 양식', 'region': '서울', 'category': '양식'})
queries.append({'query': '명지대 인문캠 맛집', 'region': '서울', 'category': '맛집'})
queries.append({'query': '명지대 맛집', 'region': '서울', 'category': '맛집'})


def search_naver_blog(query, start=1, display=100):
    encText = urllib.parse.quote(query)
    url = f"https://openapi.naver.com/v1/search/blog.json?query={encText}&display={display}&start={start}"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", NAVER_CLIENT_ID)
    request.add_header("X-Naver-Client-Secret", NAVER_CLIENT_SECRET)
    response = urllib.request.urlopen(request)
    return json.loads(response.read().decode('utf-8'))

if __name__ == "__main__":
    all_posts = []
    for q_info in queries:
        query = q_info['query']
        region = q_info['region']
        cat = q_info['category']
        print(f"🔍 '{query}' 데이터 수집 중...")
        for start in range(1, 1001, 100):  # 1~1000까지 100단위 페이지
            try:
                data = search_naver_blog(query, start=start)
                for item in data['items']:
                    title = re.sub("<[^>]*>", "", item['title'])
                    desc = re.sub("<[^>]*>", "", item['description'])
                    link = item['link']
                    all_posts.append({
                        "region": region,
                        "category": cat,
                        "title": title,
                        "description": desc,
                        "link": link
                    })
                sleep(0.7)
            except Exception as e:
                print(f"⚠️ {query} {start} 실패: {e}")
                break
        sleep(1.5)

    df = pd.DataFrame(all_posts)
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/naver_blog_bigdata.csv", index=False, encoding="utf-8-sig")
    print(f"\n✅ 총 {len(df)}건 저장 완료 (data/naver_blog_bigdata.csv)")
