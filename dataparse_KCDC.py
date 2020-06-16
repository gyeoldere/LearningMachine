from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
import pandas as pd

delay=3
browser = Chrome(r'C:\Users\gyeol\Desktop\chromedriver.exe')
browser.implicitly_wait(delay)


browser.get('https://www.cdc.go.kr/board/board.es?mid=a20501000000&bid=0015')
browser.find_element_by_tag_name('body')

title_to_want = "코로나바이러스감염증-19"
time_to_want = "정례브리핑"

forpath = "/html/body/div[4]/main/div/section[2]/section[2]/div[2]/div[3]/ul["
backpath = "]/li[2]/a"

xpath = "";

contries = ['중국','중국 외 아시아','유럽','미국','아프리카','호주']

datas = []
dates = []
for page in range(18):
    page = browser.page_source
    soup = BeautifulSoup(page, features="html.parser")
    titles = soup.find_all("span", "ellipsis")
    for i in range(10):
        text = titles[i].get_text()
        num = text.find(title_to_want)
        time = text.find(time_to_want)
        start = text.find("(")
        end = text.find("일")
        ##print(num,time)
        if (num != -1 and time != -1):

            xpath = forpath + str(i+1) + backpath
            browser.find_element_by_xpath(xpath).click()
            browser.find_elements_by_xpath("/html/body/div[4]/main/div/section[2]/section[2]/div[1]/div[2]/div[3]/table/tbody/tr[4]/td[3]/p/span")
            page = browser.page_source
            soup = BeautifulSoup(page, features="html.parser")
            numtable = soup.find_all("div", class_ ="table_wrap scroll")
            all = soup.find_all("tbody")
            ##print(len(numtable) - 1)
            all = all[len(numtable)-1]
            all = all.find_all("tr")[3]

            data = []
           ## print(text[start+1:start+2]+"/"+ text[start+4:end])
            dates.insert(0,text[start+1:start+2]+"/"+ text[start+4:end])

            for i in range(6):
                try:
                    numfinder = all.find_all("td")[2+i]
                    numfinder = numfinder.find("p")
                    numfinder = numfinder.find("span")
                    result = numfinder.get_text()
                    ##print(result)
                    ## result = contries[i] + result
                    data.append(result)
                except:
                    print("exeption")
                    data.append('x')

            datas.insert(0,data)
            browser.back()
    browser.find_element_by_xpath("/html/body/div[4]/main/div/section[2]/section[2]/div[3]/span/a[13]/i").click()

dataframe = pd.DataFrame(datas,index = dates, columns = contries)
dataframe.to_csv("일별 해외확진자_데이터.csv")
print (datas)