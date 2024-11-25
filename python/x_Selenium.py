from httpx import NetworkError
from bs4 import BeautifulSoup
import time
import telegram
import asyncio
import re
import hashlib
import json
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
from telegram.error import RetryAfter
# 要监控的用户
USERNAMES = [
    "realDonaldTrump",  # 原有用户
    "elonmusk",  # 原有用户
    "laobaishare",  # 原有用户
    "Danny_Crypton",  # 原有用户
    "DefiWimar",  # 原有用户
    "VitalikButerin",  # 以太坊创始人
    "cz_binance",  # Binance CEO
    "coinbase",  # Coinbase 官方
    "binance",  # Binance 官方
    "dogecoin",  # Dogecoin 官方
    "ShibaInuCoin",  # Shiba Inu 官方
    "Solana",  # Solana 官方
    "Polkadot",  # Polkadot 官方
    "Cardano",  # Cardano 官方
]
# 关键词列表
KEYWORDS = [
    "Meme", "Crypto", "Token", "BTC", "ETH", "XRP", "BCH",  # 原有关键词
    "new coin", "new token", "airdrop", "ICO", "launch",  # 新币相关
    "moon", "pump", "bullish", "rocket", "soar", "all-time high",  # 涨幅相关
    "bull market", "altcoin", "hodl", "blockchain", "defi", "nft",  # 区块链和DeFi相关
    "staking", "yield farming", "liquidity mining",  # DeFi和金融产品相关
    "Ethereum", "Solana", "Polkadot", "Cardano", "Avalanche",  # 区块链平台
    "Shiba Inu", "Dogecoin", "Litecoin", "Chainlink",  # 热门加密项目
    "BTC/ETH", "BTC/USDT", "ETH/USDT", "SOL/USDT", "AVAX/USDT",  # 热门交易对
    "FOMO","Fear of missing out", "bear market", "panic selling"  # 情绪相关
]

LAST_TWEETS = {username: None for username in USERNAMES}  # 存储推文ID而非文本
PUSHED_TWEETS_FILE = "pushed_tweets.json"  # 存储已推送推文的文件
# Telegram 配置
TELEGRAM_TOKEN = "7550030741:AAHR2J4XU2JQ0vIzTVWyp9k8eucitc_3OZ4"
CHAT_ID = "6320366185"
bot = telegram.Bot(token=TELEGRAM_TOKEN)
# 指定 Chrome 配置文件路径
chrome_options = Options()
# chrome_options.add_argument("user-data-dir=/Users/huoxing/Library/Application Support/Google/Chrome")# Chrome版本要和chromedriver版本一致
# chrome_options.add_argument("profile-directory=Profile 3")  # 使用默认配置文件

chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("useAutomationExtension", False)
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--remote-debugging-port=9222")
# 初始化 Chrome 浏览器
service = Service('/usr/local/bin/chromedriver')  # 替换为您的 chromedriver 路径
driver = webdriver.Chrome(service=service, options=chrome_options)
# 初始化 Selenium WebDriver
# driver = webdriver.Chrome()  # 或替换为其他浏览器驱动
# 在全局变量中初始化锁
lock = asyncio.Lock()
# 网络错误
async def handle_network_error():
    print("网络错误，正在重试...")
    await asyncio.sleep(5)  # 等待 5 秒后重试
# 异步发送消息
async def send_telegram_message_async(message):
    try:
        await bot.send_message(chat_id=CHAT_ID, text=message)
    except NetworkError as e:
        print(f"NetworkError occurred: {e}. Retrying...")
        await handle_network_error()
    except RetryAfter as e:
        print(f"Rate limited by Telegram. Retry after {e.retry_after} seconds.")
        await asyncio.sleep(e.retry_after)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
def is_tweet_pinned(tweet):
    try:
        html = tweet.get_attribute("outerHTML")
        soup = BeautifulSoup(html, "html.parser")
        if "Pinned Tweet" in soup.text:  # 检查文本中是否包含置顶标志
            print("检测到有置顶标志")
            return True
        else:
            # print("没有检测到置顶标志")
            return False
        # tweet_class = tweet.get_attribute("class")
        # if "pinned" in tweet_class.lower():
        #     return True
    except Exception as e:
        print(f"检查置顶推文时出错: {e}")
    return False
# 加载已推送的推文
def load_pushed_tweets():
    if os.path.exists(PUSHED_TWEETS_FILE):
        with open(PUSHED_TWEETS_FILE, "r") as file:
            return json.load(file)
    return {}

# 保存已推送的推文
def save_pushed_tweets(pushed_tweets):
    with open(PUSHED_TWEETS_FILE, "w") as file:
        json.dump(pushed_tweets, file)
        
# 检查推文是否包含指定关键词
def contains_keywords(text):
    # 去掉推文中的换行符和多余空格
    clean_text = re.sub(r"\s+", " ", text).strip().lower()

    # 遍历关键词，检查是否匹配
    for keyword in KEYWORDS:
        # 转小写进行匹配
        if re.search(re.escape(keyword.lower()), clean_text):
            return True
    return False
# 获取推文发布时间
def get_tweet_time(tweet):
    try:
        time_element = tweet.find_element(By.CSS_SELECTOR, 'time')
        tweet_time = time_element.get_attribute('datetime')  # 获取 ISO 格式时间
        return datetime.fromisoformat(tweet_time.replace("Z", "+00:00"))  # 转换为 datetime 对象
    except Exception as e:
        print(f"获取推文时间失败: {e}")
        return None
# 获取用户的最新推文，并返回推文的唯一ID和文本
def get_latest_tweet(username):
    url = f"https://twitter.com/{username}"
    driver.get(url)
    time.sleep(2)  # 等待页面加载
    print(f"正在获取 {username} 的推文")

    try:
        # 找到推文内容
        tweets = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'article[role="article"]'))
        )

        latest_tweet = None
        latest_time = None

        for tweet in tweets:
            # 检查是否为置顶推文
            is_pinned = False
            try:
              
                # print(f"检查后发现为置顶推")
                pinned_label = tweet.find_element(By.XPATH, ".//*[contains(text(), 'Pinned')]")
                if pinned_label:
                    is_pinned = True
                    print("发现置顶推文标志")
                else:
                    print("没有检测到置顶推文标志")
            except:
                # print(f"无置顶标记")
                pass  # 无置顶标记则继续
            # is_pinned = is_tweet_pinned(tweet)
            if is_pinned:
                print("发现置顶推文通过HTML解析")
            # 获取推文时间
            tweet_time = get_tweet_time(tweet)
            if not tweet_time:
                continue  # 跳过无效时间的推文

            # 更新最新推文逻辑
            if not latest_time or tweet_time > latest_time:
                latest_time = tweet_time
                latest_tweet = (tweet, is_pinned)

        if latest_tweet:
            tweet, is_pinned = latest_tweet
            tweet_text_element = tweet.find_element(By.CSS_SELECTOR, 'div[data-testid="tweetText"]')
            tweet_text = tweet_text_element.text.strip()  # 获取文本内容并去除多余的空格
            tweet_link = tweet.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
            tweet_id = hashlib.md5(tweet_text.encode()).hexdigest()

            print(f"{'置顶且最新' if is_pinned else '最新'}推文: {tweet_text}, ID: {tweet_id}, 时间: {latest_time}, 链接: {tweet_link}")
            return tweet_id, tweet_text, tweet_link
        else:
            print(f"未找到 {username} 的推文")
    except Exception as e:
        print(f"获取 {username} 的推文时出错: {e}")
    return None, None, None
# 获取用户的最上面的推文，并返回推文的唯一ID和文本
# def get_top_tweet(username):
#     url = f"https://twitter.com/{username}"
#     headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
#     }
#     driver.get(url)
#     time.sleep(2)  # 等待页面加载
#     print(f"正在获取 {username} 的推文")
    
#     # 模拟滚动页面，向下滚动 0 次,如果滚动过多无法获取最新
#     for _ in range(0):
#         driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
#         time.sleep(2)  # 等待页面加载

#     try:
#         # 找到推文内容
#         tweets = WebDriverWait(driver, 10).until(
#             EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'article[role="article"]'))
#         )

#         if tweets:
#             # 获取第一条推文的唯一 ID 和文本
#             tweet = tweets[0]
#             # 等待推文加载
#             # tweet_text_element = WebDriverWait(driver, 20).until(
#             #     EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-testid="tweetText"]'))
#             # )
#             tweet_text_element = tweet.find_element(By.CSS_SELECTOR, 'div[data-testid="tweetText"]')  # 通过 tweetText 提取正文内容
#             tweet_text = tweet_text_element.text.strip()  # 获取文本内容并去除多余的空格
#             # tweet_text = tweet.text
#             # 使用推文文本生成唯一 ID（替代 data-tweet-id）
#             tweet_id = hashlib.md5(tweet_text.encode()).hexdigest()
#              # 尝试获取推文链接，并从 URL 中提取 tweet_id
#             tweet_link = tweet.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
#             tweet_id_element = tweet_link.split('/')[-1]  # Tweet ID 位于 URL 的最后部分
#             print(f"返回的tweet_id_element {tweet_id_element} 和推文link: {tweet_link}")
#             print(f"返回的tweet_id {tweet_id} ")
#             return tweet_id, tweet_text,tweet_link
#         else:
#             print(f"未找到 {username} 的推文")
#     except Exception as e:
#         print(f"获取 {username} 的推文时出错: {e}")
#     return None, None, None
# 监控逻辑
async def monitor_tweets():
    global LAST_TWEETS
    pushed_tweets = load_pushed_tweets()
    for username in USERNAMES:
        tweet_id, tweet_text, tweet_link = get_latest_tweet(username)
        if tweet_id and tweet_id not in pushed_tweets:
            async with lock:  # 使用异步锁保护 LAST_TWEETS
                # 检查是否有新推文
                # if tweet_id != LAST_TWEETS[username]:
                    print(f"来自 {username} 的新推文: {tweet_text}")
                    if contains_keywords(tweet_text):  
                        # 检查是否包含关键词
                        print("推文符合条件")
                        # 推送到 Telegram
                        await send_telegram_message_async(f"新推文来自 {username}: {tweet_text}\n{tweet_link}")
                        pushed_tweets[tweet_id] = tweet_text
                        save_pushed_tweets(pushed_tweets)
                        print(f"已保存推文 {tweet_id} 到 JSON 文件")
                    # # 更新 LAST_TWEETS
                    # LAST_TWEETS[username] = tweet_id
        await asyncio.sleep(5)  # 避免请求过快
# 主函数，使用 asyncio.run 执行异步任务
async def main():
    while True:
        await monitor_tweets()
        await asyncio.sleep(60)  # 每分钟检查一次

# 调用 main() 来运行程序
if __name__ == "__main__":
    asyncio.run(main())
