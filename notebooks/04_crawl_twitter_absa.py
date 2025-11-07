import os
import pandas as pd
from tqdm import tqdm
import snscrape.modules.twitter as sntwitter

# -----------------------------
# KONFIGURASI DASAR
# -----------------------------
OUTPUT_DIR = "data/crawling_2024"
os.makedirs(OUTPUT_DIR, exist_ok=True)

DATE_START = "2023-09-01"
DATE_END = "2024-05-31"
MAX_TWEETS = 1000  # target per aspek

# -----------------------------
# KEYWORD PER ASPEK
# -----------------------------
aspect_keywords = {
    "integritas": [
        '"bersih dari korupsi"', '"tidak korupsi"', '"pemimpin jujur"', '"integritas tinggi"', '"amanah"'
    ],
    "kapabilitas": [
        '"kompeten"', '"kapabilitas"', '"berpengalaman memimpin"', '"cerdas"', '"profesional"'
    ],
    "empati": [
        '"peduli rakyat"', '"turun ke rakyat"', '"bantu korban"', '"dekat dengan rakyat"'
    ],
    "akseptabilitas": [
        '"disukai rakyat"', '"diterima masyarakat"', '"elektabilitas tinggi"', '"popularitas kandidat"'
    ],
    "kontinuitas": [
        '"lanjutkan program"', '"keberlanjutan pembangunan"', '"visi jangka panjang"', '"melanjutkan kerja"'
    ]
}

# -----------------------------
# FUNGSI CRAWLING
# -----------------------------
def crawl_tweets(keyword_query, max_tweets=500):
    tweets_data = []
    query = f"{keyword_query} lang:id since:{DATE_START} until:{DATE_END}"
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
        if i >= max_tweets:
            break
        tweets_data.append({
            "date": tweet.date,
            "username": tweet.user.username,
            "content": tweet.rawContent,
            "replyCount": tweet.replyCount,
            "retweetCount": tweet.retweetCount,
            "likeCount": tweet.likeCount,
            "url": tweet.url
        })
    return tweets_data

# -----------------------------
# PROSES CRAWLING PER ASPEK
# -----------------------------
for aspect, keywords in aspect_keywords.items():
    print(f"\n🔍 Mengambil tweet untuk aspek: {aspect}")
    all_tweets = []
    for kw in tqdm(keywords, desc=f"Aspek {aspect}"):
        tweets = crawl_tweets(kw, max_tweets=MAX_TWEETS // len(keywords))
        all_tweets.extend(tweets)

    # Simpan ke CSV
    df = pd.DataFrame(all_tweets)
    df["aspect_target"] = aspect
    csv_path = os.path.join(OUTPUT_DIR, f"tweets_{aspect}.csv")
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")
    print(f"✅ Disimpan: {csv_path} ({len(df)} tweet)")
