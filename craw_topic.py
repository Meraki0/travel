import praw
from langdetect import detect
import re
from collections import Counter, defaultdict
import nltk
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt

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

# 주제별 키워드 사전 정의
TOPIC_KEYWORDS = {
    "food": ["food", "meal", "rice", "soup", "vegetarian", "tea", "eat", "dish"],
    "meditation": ["meditation", "peace", "calm", "relax", "breath", "mindfulness"],
    "accommodation": ["room", "bed", "bathroom", "facility", "clean", "comfortable"],
    "people": ["monk", "teacher", "guide", "host", "staff", "person"],
    "activity": ["chanting", "bowing", "walking", "temple", "experience", "program"]
}

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
    topic_emotion = defaultdict(list)
    for post in posts:
        text = re.sub(r"http\S+", "", post)
        text = re.sub(r"[^a-zA-Z\s]", "", text).lower()
        words = text.split()
        filtered = [w for w in words if w not in stop_words and len(w) > 2]
        
        for word in filtered:
            if word in sia.lexicon:
                for topic, keywords in TOPIC_KEYWORDS.items():
                    if any(k in post.lower() for k in keywords):
                        topic_emotion[topic].append(word)
                        break
    return topic_emotion

def plot_emotion_words(topic_emotion):
    for topic, words in topic_emotion.items():
        counter = Counter(words).most_common(10)
        labels, counts = zip(*counter) if counter else ([], [])
        
        plt.figure(figsize=(8, 4))
        plt.barh(labels, counts, color="skyblue")
        plt.title(f"Top Emotion Words in Topic: {topic}")
        plt.xlabel("Frequency")
        plt.gca().invert_yaxis()
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    print("크롤링 중...")
    posts = crawl_reddit(limit=100)
    print(f"{len(posts)}개 영어 후기 수집 완료")

    print("감정 단어 추출 및 주제 분류 중...")
    topic_emotion = extract_emotion_words(posts)

    print("\n[주제별 감정 단어 개수]")
    for topic, words in topic_emotion.items():
        print(f"{topic}: {len(words)}개 단어")

    print("\n시각화 중...")
    plot_emotion_words(topic_emotion)
