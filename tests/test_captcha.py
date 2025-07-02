from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import requests
import os

def main():
    # 1. 크롬 브라우저 자동 실행
    driver = webdriver.Chrome()  # chromedriver가 PATH에 있어야 함
    driver.get("http://localhost:5000/")

    # 2. 캡챠 이미지 src 추출
    captcha_img = driver.find_element(By.ID, "captcha")
    captcha_src = captcha_img.get_attribute("src")

    # 3. 캡챠 이미지 다운로드
    img_data = requests.get(captcha_src).content
    save_path = os.path.join(os.path.dirname(__file__), "captcha_test.png")
    with open(save_path, "wb") as f:
        f.write(img_data)
    print("캡챠 이미지 다운로드 완료! ({}에 저장)".format(save_path))

    # 4. (선택) 캡챠 입력 및 제출 자동화 예시
    # driver.find_element(By.ID, "captcha-input").send_keys("ABCDE")
    # driver.find_element(By.CSS_SELECTOR, "button[type=submit]").click()

    time.sleep(2)
    driver.quit()

if __name__ == "__main__":
    main() 