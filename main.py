import requests
import time
import random
import os
from flask import Flask
app = Flask(__name__)
FLICKR_PHOTO_URL = os.environ.get("FLICKR_URL", "https://www.flickr.com/photos/203492062@N02/54838603755/in/dateposted/")
NUMBER_OF_REQUESTS = int(os.environ.get("NUM_REQUESTS", 10)) # 預設值設定較小，防止誤觸發
DELAY_SECONDS = float(os.environ.get("DELAY", 0.1))
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7'
}
def run_flickr_test(num_requests, delay):
    """核心測試邏輯，接受次數和延遲作為參數"""
    log = []
    success_count = 0
    start_time = time.time()
    log.append(f"--- Flickr 瀏覽數刷新測試開始 ---")
    log.append(f"目標 URL: {FLICKR_PHOTO_URL}")
    log.append(f"總請求次數: {num_requests}")
    log.append(f"請求間隔: {delay} 秒")
    for i in range(1, num_requests + 1):
        try:
            response = requests.get(FLICKR_PHOTO_URL, headers=HEADERS, timeout=10)
            if response.status_code == 200:
                success_count += 1
                log.append(f"[{i}/{num_requests}] 請求成功 (Status: {response.status_code})")
            else:
                log.append(f"[{i}/{num_requests}] 請求失敗 (Status: {response.status_code})")
        except requests.exceptions.RequestException as e:
            log.append(f"[{i}/{num_requests}] 請求發生錯誤: {e}")
        time.sleep(delay)
    total_duration = time.time() - start_time
    log.append("-" * 30)
    log.append(f"測試完成。總耗時: {total_duration:.2f} 秒，成功: {success_count}")
    return "<br>".join(log)
@app.route('/')
def ping_service():
    """
    根路由：用於 UptimeRobot 等監控服務 Ping 喚醒。
    每次 Ping 時，只執行一次極小的測試，確保服務存活。
    """
    # 執行一次極小的測試 (N=1, Delay=0.1) 確保服務存活且不休眠
    ping_log = run_flickr_test(num_requests=1, delay=0.1)
    return f"Flickr Test Service is Active. <br> Last Ping Check: {time.ctime()} <br> {ping_log}"

@app.route('/run-full-test')
def trigger_full_test():
    """
    手動觸發完整測試的端點。
    使用環境變數設定的大規模參數 (例如 N=500, Delay=0.5)
    """
    return run_flickr_test(num_requests=NUMBER_OF_REQUESTS, delay=DELAY_SECONDS)
# Gunicorn 不需要這個區塊，但保持它以供本地測試
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
