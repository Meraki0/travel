import praw
from langdetect import detect
import re
from collections import Counter
import nltk
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer

# 1회만 실행
nltk.download('stopwords')
nltk.download('vader_lexicon')

stop_words = set(stopwords.words('english'))
sia = SentimentIntensityAnalyzer()

reddit = praw.Reddit(
    client_id="5-80-lQrD19i083pYAFGSQ",
    client_secret="dLY63ALq_UZ8npOEqhF6BQmkTj0GMA",
    user_agent="temple_stay_emotion_words"
)

def crawl_reddit(keyword="temple stay korea", limit=100):
    posts = []
    for submission in reddit.subreddit("travel").search(keyword, limit=limit):
        text = submission.title + " " + submission.selftext
        try:
            if detect(text) == "en":
                posts.append(text)
        except:
            continue
    return posts

def extract_emotion_words(posts):
    emotion_words = []
    for post in posts:
        text = re.sub(r"http\S+", "", post)
        text = re.sub(r"[^a-zA-Z\s]", "", text).lower()
        words = text.split()
        filtered = [w for w in words if w not in stop_words and len(w) > 2]
        
        # VADER 감정 사전에 있는 단어만 추출
        for w in filtered:
            if w in sia.lexicon:
                emotion_words.append(w)
    return emotion_words

if __name__ == "__main__":
    print("크롤링 중...")
    posts = crawl_reddit(limit=100)
    print(f"{len(posts)}개 영어 후기 수집 완료")

    print("감정 단어 추출 중...")
    emotion_words = extract_emotion_words(posts)

    counts = Counter(emotion_words)
    print("\n[감정 관련 단어 상위 30]")
    for word, count in counts.most_common(30):
        print(f"{word}: {count}")
