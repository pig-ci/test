import requests
import time
import random
import os
import threading
from flask import Flask
app = Flask(__name__)
FLICKR_PHOTO_URL = os.environ.get("FLICKR_URL", "https://www.flickr.com/photos/your_user_id/your_photo_id/")
NUMBER_OF_REQUESTS = int(os.environ.get("NUM_REQUESTS", 100))
DELAY_SECONDS = float(os.environ.get("DELAY", 0.1))
LOOP_DELAY_SECONDS = int(os.environ.get("LOOP_DELAY", 300))
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7'
}
def run_flickr_test(num_requests, delay):
    """核心測試邏輯，用於單輪執行"""
    log_message = f"--- Flickr 測試開始 (N={num_requests}, Delay={delay}s) ---"
    print(log_message)
    success_count = 0
    start_time = time.time()
    for i in range(1, num_requests + 1):
        try:
            requests.get(FLICKR_PHOTO_URL, headers=HEADERS, timeout=10)
            success_count += 1
            if i % 1000 == 0 or i == num_requests:
                print(f"[{i}/{num_requests}] 請求成功... (總耗時: {time.time()-start_time:.2f}s)")
        except requests.exceptions.RequestException as e:
            print(f"請求發生錯誤: {e}")
        time.sleep(delay)
    total_duration = time.time() - start_time
    print(f"測試完成。總耗時: {total_duration:.2f} 秒，成功: {success_count}/{num_requests}")
    return total_duration
def background_infinite_loop():
    """在獨立線程中無限運行測試"""
    num_requests = NUMBER_OF_REQUESTS
    delay = DELAY_SECONDS
    loop_delay = LOOP_DELAY_SECONDS
    print("--------------------------------------------------")
    print("背景無限循環線程已啟動！")
    print(f"配置: 每 {loop_delay} 秒執行 {num_requests} 次請求 (間隔 {delay}s)")
    print("--------------------------------------------------")

    while True:
        run_flickr_test(num_requests, delay)
        print(f"下一輪將在 {loop_delay} 秒後開始...")
        time.sleep(loop_delay)
@app.route('/')
def ping_service():
    """根路由：用於 UptimeRobot 喚醒，並檢查無限線程是否運行"""
    status = "Active" if hasattr(app, 'test_thread_running') else "Inactive (Needs to be triggered)"
    return f"Flickr Test Service is Running. Status: {status}"

@app.route('/run-full-test')
def trigger_full_test():
    """手動訪問此路由，啟動背景無限循環"""
    if not hasattr(app, 'test_thread_running'):
        thread = threading.Thread(target=background_infinite_loop)
        thread.daemon = True # 允許主程序結束時，線程自動結束
        thread.start()
        app.test_thread_running = True
        return f"無限循環背景測試已啟動！請查看 Render Log。"
    else:
        return "無限循環背景測試已在運行中。"
