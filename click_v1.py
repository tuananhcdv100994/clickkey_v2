import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc

# Cấu hình Chrome chạy ở chế độ headless (không giao diện)
def setup_driver():
    options = Options()
    options.add_argument("--headless=new")  # Chạy ở chế độ không giao diện
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920x1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return uc.Chrome(options=options)

# Hàm tìm kiếm Google và click vào trang mục tiêu
def google_search_and_click(driver, keyword, target_url):
    print(f"\n[INFO] Đang tìm kiếm từ khóa: {keyword}")
    driver.get("https://www.google.com")
    
    # Tìm ô tìm kiếm, nhập từ khóa và nhấn Enter
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(keyword)
    search_box.send_keys(Keys.RETURN)
    time.sleep(random.uniform(2, 4))  # Đợi load kết quả

    # Duyệt tối đa 5 trang kết quả (tương đương 50 kết quả)
    for page in range(5):
        results = driver.find_elements(By.CSS_SELECTOR, "div.tF2Cxc")
        rank = page * 10  # Tính thứ hạng bắt đầu từ trang hiện tại

        for i, result in enumerate(results):
            rank += 1
            try:
                link = result.find_element(By.TAG_NAME, "a")
                url = link.get_attribute("href")

                if target_url in url:
                    print(f"[SUCCESS] Tìm thấy {target_url} ở vị trí {rank}, đang truy cập...")
                    link.click()
                    return rank, url  # Thoát sau khi click thành công
            except Exception:
                continue

        # Chuyển sang trang tiếp theo nếu chưa tìm thấy
        try:
            next_button = driver.find_element(By.LINK_TEXT, "Next")
            next_button.click()
            time.sleep(random.uniform(2, 4))
        except:
            break  # Không tìm thấy nút "Next", dừng vòng lặp

    print(f"[FAIL] Không tìm thấy {target_url}")
    return None, None

# Thực hiện hành động sau khi vào trang web
def perform_actions(driver):
    duration = random.randint(15, 20)  # Giữ trang trong khoảng 15-20s
    print(f"[INFO] Đang ở lại trang {duration} giây...")

    start_time = time.time()
    while time.time() - start_time < duration:
        driver.execute_script("window.scrollBy(0, 500);")  # Cuộn trang
        time.sleep(random.uniform(2, 4))

    print("[INFO] Hoàn thành thời gian ở trang.")

# Chạy tool
def main():
    keywords = input("Nhập danh sách từ khóa (cách nhau bằng dấu phẩy): ").split(",")
    target_url = input("Nhập URL mục tiêu: ").strip()
    
    driver = setup_driver()

    for keyword in keywords:
        keyword = keyword.strip()
        rank, clicked_url = google_search_and_click(driver, keyword, target_url)
        
        if clicked_url:
            perform_actions(driver)

        print("[INFO] Chờ 1 phút trước lần tìm kiếm tiếp theo...\n")
        time.sleep(10)

    driver.quit()

if __name__ == "__main__":
    main()
