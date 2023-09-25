from playwright.sync_api import Playwright, sync_playwright
import time
import sys

# 동행복권 아이디와 패스워드를 설정
USER_ID = sys.argv[1]
USER_PW = sys.argv[2]

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://dhlottery.co.kr/user.do?method=login")
    page.click("[placeholder=\"아이디\"]")
    page.fill("[placeholder=\"아이디\"]", USER_ID)
    page.press("[placeholder=\"아이디\"]", "Tab")
    page.fill("[placeholder=\"비밀번호\"]", USER_PW)
    page.press("[placeholder=\"비밀번호\"]", "Tab")

    with page.expect_navigation():
        page.press("form[name=\"jform\"] >> text=로그인", "Enter")
    time.sleep(5)  
    
    page.goto(url="https://el.dhlottery.co.kr/game/pension720/game.jsp")
    # "비정상적인 방법으로 접속하였습니다. 정상적인 PC 환경에서 접속하여 주시기 바랍니다." 우회하기
    # try:
    #     page.locator("#popupLayerAlert").get_by_role("button", name="확인").click()
    #     print(page.content())
    # except:
    #     print("비정상환경 접속 주의 팝업 없음") 
    
    page.click("text=자동번호")
    page.click("text=선택완료")
    page.click("text=구매하기")
    time.sleep(5)
    
    buy_button = page.locator('a.btn_blue:has(span:has-text("구매하기"))')
    if buy_button.is_visible():
        buy_button.click()
    time.sleep(1)
    
    page.goto("https://dhlottery.co.kr/user.do?method=logout&returnUrl=")
    page.close()
    context.close()
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
