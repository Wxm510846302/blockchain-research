import requests
import time
import telegram
import json
import os
import asyncio

# Twitter API 配置
BEARER_TOKEN = ''
HEADERS = {
    "Authorization": f"Bearer {BEARER_TOKEN}"
}

# 监控的账户
USERNAMES = ["realDonaldTrump","elonmusk","laobaishare", "Danny_Crypton", "DefiWimar"]
LAST_TWEET_IDS = {username: None for username in USERNAMES}

# Telegram 配置
TELEGRAM_TOKEN = ""
CHAT_ID = "6320366185"
bot = telegram.Bot(token=TELEGRAM_TOKEN)

# 推特 API URL
BASE_URL = "https://api.twitter.com/2"
USER_LOOKUP_URL = f"{BASE_URL}/users/by/username/"
USER_TIMELINE_URL = f"{BASE_URL}/users/{'{id}'}/tweets"
# 缓存文件路径
CACHE_FILE = "user_ids_cache.json"

# 关键词列表
KEYWORDS = ["Meme", "Crypto", "Token","BTC" ,"ETH"]

# 检查推文是否包含指定关键词
def contains_keywords(text):
    return any(keyword.lower() in text.lower() for keyword in KEYWORDS)

# 获取缓存中的用户 ID
def load_user_ids_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    return {}

# 保存用户 ID 到缓存文件
def save_user_ids_cache(user_ids):
    with open(CACHE_FILE, "w") as f:
        json.dump(user_ids, f)

# 获取用户 ID
def get_user_id(username,user_ids_cache):

    if username in user_ids_cache:
        print(f"从缓存中获取 {username} 的 ID: {user_ids_cache[username]}")
        return user_ids_cache[username]

    url = f"{USER_LOOKUP_URL}{username}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        # 打印响应的内容，检查结构
        print(f"获取用户 ID 响应内容: {response.json()}")
        user_id = response.json()["data"]["id"]
        user_ids_cache[username] = user_id
        save_user_ids_cache(user_ids_cache)  # 更新缓存文件
        print(f"从 API 获取 {username} 的 ID: {user_id}")
        return user_id
    elif response.status_code == 429:  # Too Many Requests 错误
        reset_time = int(response.headers.get('X-Rate-Limit-Reset'))
        reset_time = reset_time - time.time()
        print(f"获取用户 ID请求过于频繁，等待 {reset_time} 秒后重试...")
        time.sleep(reset_time)  # 暂停 60 秒
        return get_user_id(username,user_ids_cache)  # 重新请求
    else:
        print(f"无法获取用户 {username} 的 ID: {response.json()}")
        return None

# 获取最新推文
def get_latest_tweet(user_id):
    url = USER_TIMELINE_URL.replace("{id}", user_id)
    params = {"max_results": 5}  # 获取最近 5 条推文
    response = requests.get(url, headers=HEADERS, params=params)
    if response.status_code == 200:
        tweets = response.json()["data"]
        print(f"获取最新推文 响应内容: {tweets}")
        return tweets if tweets else None
    elif response.status_code == 429:  # Too Many Requests 错误
        reset_time = int(response.headers.get('X-Rate-Limit-Reset')) - time.time()
        print(f"获取最新推文请求过于频繁，等待 {reset_time:.2f} 秒后重试...")
        time.sleep(max(reset_time, 1))  # 等待后再重试
        return get_latest_tweet(user_id)  # 重新请求
    else:
        print(f"无法获取用户 {user_id} 的推文: {response.json()}")
        return None

# 保存推文 ID 到 JSON 文件
def save_last_tweet_ids():
    with open("last_tweet_ids.json", "w") as file:
        json.dump(LAST_TWEET_IDS, file)

# 加载推文 ID，从文件恢复记录
def load_last_tweet_ids():
    global LAST_TWEET_IDS
    try:
        with open("last_tweet_ids.json", "r") as file:
            LAST_TWEET_IDS = json.load(file)
    except FileNotFoundError:
        LAST_TWEET_IDS = {}
# 异步发送消息
async def send_telegram_message_async(message):

    await bot.send_message(chat_id=CHAT_ID, text=message)

# 推送消息到 Telegram
# def send_telegram_message(message):
#     asyncio.run(send_telegram_message_async(message))

# 在监控账户之前，确保 LAST_TWEET_IDS 中有每个账户的记录
def initialize_last_tweet_ids(username):
    if username not in LAST_TWEET_IDS:
        LAST_TWEET_IDS[username] = None  # 或者使用一个较早的推文 ID
        print(f"初始化 {username} 的 LAST_TWEET_IDS 为 None")
# 监控逻辑
def monitor_accounts():
    global LAST_TWEET_IDS
    user_ids_cache = load_user_ids_cache()  # 加载缓存

    for username in USERNAMES:

        user_id = get_user_id(username,user_ids_cache)
        if not user_id:
            continue    
        initialize_last_tweet_ids(username)  # 确保初始化
        latest_tweets = get_latest_tweet(user_id)
        if latest_tweets:
           for tweet in latest_tweets:
             print(f"推文内容: {tweet['text']}")
             if tweet and tweet["id"] != LAST_TWEET_IDS[username]:
             # 仅处理包含关键词的推文
               if contains_keywords(tweet["text"]):
                  print(f"符合条件的推文来自 {username}: {tweet['text']}")
                  LAST_TWEET_IDS[username] = tweet["id"]
                
                  # 推送到 Telegram
                #   send_telegram_message(f"新推文来自 {username}: {tweet['text']}")
                  await send_telegram_message_async(f"新推文来自 {username}: {tweet}")
    # 每次循环结束时保存推文记录
    save_last_tweet_ids()

# 在启动时加载记录
load_last_tweet_ids()

# 循环监控
if __name__ == "__main__":
    while True:
        # send_telegram_message("新推文")
        monitor_accounts()
        time.sleep(60)  # 每分钟检查一次
