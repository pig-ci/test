import requests
import time
import random
# 替換成測試的 Flickr 照片的完整 URL
FLICKR_PHOTO_URL = "https://www.flickr.com/photos/203492062@N02/54838603755/in/dateposted/" 
# 訪問次數
NUMBER_OF_REQUESTS = 50 
# 每次請求之間的延遲時間（秒）。請測試不同延遲：
# 0.5 秒：極端刷量
# 5 秒：中度刷量
# 10 秒：模擬較快但可疑的真實用戶
DELAY_SECONDS = 0.5 
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7'
}
print(f"--- 瀏覽數測試 ---")
print(f"目標 URL: {FLICKR_PHOTO_URL}")
print(f"總請求次數: {NUMBER_OF_REQUESTS}")
print(f"請求間隔: {DELAY_SECONDS} 秒")
print("-" * 30)
success_count = 0
start_time = time.time()
for i in range(1, NUMBER_OF_REQUESTS + 1):
    try:
        response = requests.get(FLICKR_PHOTO_URL, headers=HEADERS, timeout=10)
        if response.status_code == 200:
            success_count += 1
            print(f"[{i}/{NUMBER_OF_REQUESTS}] 請求成功 (Status: {response.status_code})")
        else:
            print(f"[{i}/{NUMBER_OF_REQUESTS}] 請求失敗 (Status: {response.status_code})")
    except requests.exceptions.RequestException as e:
        print(f"[{i}/{NUMBER_OF_REQUESTS}] 請求發生錯誤: {e}")
    time.sleep(DELAY_SECONDS)
end_time = time.time()
total_duration = end_time - start_time
print("-" * 30)
print(f"測試完成。")
print(f"總耗時: {total_duration:.2f} 秒")
print(f"成功請求次數: {success_count}")
print("-" * 30)
print("除錯建議：")
print(f"1. 檢查 Flickr 瀏覽數：在 {total_duration:.2f} 秒內，瀏覽數應增加多少？")
print(f"2. 若瀏覽數只增加 1，表示系統有有效的時間窗格限制。")
print(f"3. 若瀏覽數增加的數字接近 {success_count}，則時間窗格可能過寬或完全失效。")
