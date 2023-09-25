import requests
from bs4 import BeautifulSoup

FILE_PATH="./lotto720/count.log"

group_num = {key: 0 for key in range(1, 6)}
num_matrixt =[]
bonus_num_matrixt =[]
for idx in range(1, 7):
    num_row = {key: 0 for key in range(0, 10)}
    num_matrixt.append(num_row)
    bonus_num_matrixt.append(num_row)    

def getMaxRoundNum():
    url="https://dhlottery.co.kr/common.do?method=main"
    html=requests.get(url).text
    soup=BeautifulSoup(html, "lxml")
    tag=soup.find(name="strong", attrs={"id":"drwNo720"})
    return int(tag.text)

def getWinNumbers(round_num: int):
    url="https://dhlottery.co.kr/gameResult.do?method=win720"
    html=requests.post(url, data={'Round': round_num}).text
    soup=BeautifulSoup(html, "lxml")
    win_result_tag=soup.find(name="div", attrs={"class", "win_result"})

    win720_num_tag=win_result_tag.find_all("div", "win720_num")
    group_result=int(win720_num_tag[0].find("div", "group").find_all("span")[1].text)

    group_num[group_result] += 1  # 조넘버 카운팅

    num_result = []
    num_result.append(group_result)
    for i in range(6):
        num=win720_num_tag[0].find("span", f"num al720_color{i+1} large")
        num_result.append(int(num.find("span").text))
        num_matrixt[i][int(num.find("span").text)] += 1  # 번호 카운팅

    bonus_num_result = []
    bonus_num_result.append('na')
    for i in range(6):
        num=win720_num_tag[1].find("span", f"num al720_color{i+1} large")
        bonus_num_result.append(int(num.find("span").text))
        bonus_num_matrixt[i][int(num.find("span").text)] += 1  # 보너스번호 카운팅

    print(round_num, num_result, bonus_num_result)

def load_lotto_count():
    rstr=""
    try:
        with open(FILE_PATH, "r") as file:
            rstr = file.read()
    except:
        return 0

    rstr_split=rstr.split("\n")

    group_num_str = rstr_split[1].split(';')
    for val in group_num:
        group_num[val] = int(group_num_str[val - 1])
    
    idx = 2
    for num_arr in num_matrixt:
        split_str = rstr_split[idx].split(';')
        for val in num_arr:
            num_matrixt[idx-2][val] = int(split_str[val])
        idx += 1
    for num_arr in bonus_num_matrixt:
        split_str = rstr_split[idx].split(';')
        for val in num_arr:
            bonus_num_matrixt[idx-8][val] = int(split_str[val])
        idx += 1

    print("[LOAD] group :", group_num)
    for val in num_matrixt:
        print("[LOAD] count :", val)
    for val in bonus_num_matrixt:
        print("[LOAD] bonus :", val)

    return int(rstr_split[0])

def save_lotto_count(lcnt):
    gstr=""
    cstr=""
    bstr=""
    for val in group_num:
        gstr += str(group_num[val]) + ";"
    for num_arr in num_matrixt:
        for val in num_arr:
            cstr += str(num_arr[val]) + ";"
        cstr += "\n"
    for num_arr in bonus_num_matrixt:
        for val in num_arr:
            bstr += str(num_arr[val]) + ";"
        bstr += "\n"
    
    with open(FILE_PATH, "w") as file:
        file.write(str(lcnt) + "\n")
        file.write(gstr + "\n")
        file.write(cstr)
        file.write(bstr)
    with open(FILE_PATH, "r") as file:
        print("[SAVE] ", file.read())


# 현재 회차 가져오기
print("연금복권 현재 회차 찾기 ...")
num=getMaxRoundNum()

# 캐쉬된 데이터 불러오기
onum=load_lotto_count()

# 당첨번호 확인하기
print("연금복권 번호 크롤링 ...", onum, num)
for i in (range(onum+1, num+1)):
    getWinNumbers(i)

# 크롤링 데이터 캐쉬에 저장하기
save_lotto_count(num)
