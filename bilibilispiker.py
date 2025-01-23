from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import json
import re
import os

# Chrome浏览器
class Spiker():
    def __init__(self, user_ids,year):

        #代理IP
        # proxy_ip = "112.17.16.208"
        # proxy_port = "8089"
        # chrome_options = Options()
        # chrome_options.add_argument('--proxy-server={}:{}'.format(proxy_ip, proxy_port))
        # self.driver = webdriver.Chrome(options=chrome_options)

        self.year=year
        self.user=[]
        self.driver = webdriver.Chrome()  
        self.driver.implicitly_wait(30)
        self.user_ids = user_ids
        self.base_url = f'https://space.bilibili.com'
        self.driver.get(self.base_url)

        #检查是否有未完成文件
        if(os.path.exists(f"{year}_top.json")):
            with open(f"{self.year}_top.json","r",encoding="utf-8") as f:
                self.user=json.load(f)
                f.close()
        print("速度扫码登入")
        # time.sleep(10) #扫码等待时间
        print("---------------------------start-----------------------------")
        return
       

    def get_url(self):
        '''
        获取每个up主空间的视频链接
        '''
        print("========================get_url==========================")

        for user in self.user:      #从上次中断处开始
            self.user_ids.remove(user["id"])
        save_num=0
        for user_id in self.user_ids:
            self.driver.get(self.base_url+f"/{user_id}/upload/video")       #遍历个人空间
            nickname=self.driver.find_element(By.XPATH,"//div[@class='nickname'] | //span[@id='h-name']")
            nickname=nickname.get_attribute("innerHTML")
            print(nickname)         
            url_list=[]
            time.sleep(1)

            #防止只有一页无页数
            try:    
                total=self.driver.find_element(By.XPATH,"//span[@class='vui_pagenation-go__count' or @class='be-pager-total']")     #视频页数，不要缩放窗口
                total=total.get_attribute("innerHTML")
                total=int(re.findall(r"\d+",total)[0])
            except:
                total=1
            # print(total)
            print(f"total: {total}")

            self.driver.implicitly_wait(5)
            #获取每个视频链接
            for i in range(total):        
                videos=self.driver.find_elements(By.CLASS_NAME,"bili-cover-card")
                videos=self.driver.find_elements(By.XPATH,"//a[@class='bili-cover-card'] | //li[@class='small-item fakeDanmu-item']")
                datas=self.driver.find_elements(By.XPATH,"//div[@class='bili-video-card__subtitle']//span | //span[@class='time']")

                flag=False
                for video, data in zip(videos, datas):
                    #判断符合规定年份的视频
                    if(len(data.get_attribute('innerHTML'))>6 and int(re.findall(r"\d+",data.get_attribute('innerHTML')[:4])[0])<self.year):
                        flag=True
                        break
                    elif(len(data.get_attribute('innerHTML'))>6 and int(re.findall(r"\d+",data.get_attribute('innerHTML')[:4])[0])==self.year):
                        url_list.append(video.get_attribute("href"))
                if(flag or total-1==i):
                    break

                self.driver.find_element(By.XPATH,"//button[text()='下一页'] | //a[text()='下一页']").click()
                time.sleep(2)
            self.user.append({"name":nickname,"id":user_id,"url_list":url_list,"code":"000"})       #code：000代表获取视频链接成功
            save_num+=1
            if(save_num%2==0):      #即使保存，防止被封ip
                print("save success")
                self.save()
            print(f"get url of {nickname} complete save:{save_num}")
        return

    def get_data(self):
        '''
        获取视频详细信息
        '''
        print("=========================get_data========================")
        self.driver.implicitly_wait(5)
        save_num=0
        for user in self.user:
            if(user["code"]=="001"):    #从上次中断处开始
                continue
            user["video"]=[]
            for url in user["url_list"]:    #获取视频详细信息
                self.driver.get(url)
                #防止个别视频无标题信息或视频不见
                try:
                    title=self.driver.find_element(By.XPATH,"//h1[@class='video-title special-text-indent']").get_attribute("innerHTML")
                except:
                    continue
                print(f"title: {title}")
                view=self.driver.find_element(By.XPATH,"//div[@class='view-text']").get_attribute("innerHTML")
                like=self.driver.find_element(By.XPATH,"//span[@class='video-like-info video-toolbar-item-text']").get_attribute("innerHTML")
                coin=self.driver.find_element(By.XPATH,"//span[@class='video-coin-info video-toolbar-item-text']").get_attribute("innerHTML")
                date=self.driver.find_element(By.XPATH,"//div[@class='pubdate-ip-text']").get_attribute("innerHTML")
                if(int(date[:4])<self.year):
                    break
                elif(int(date[:4])>self.year):
                    continue
                user["video"].append({"title":title,"view":view,"like":like,"coin":coin,"date":date,"url":url})
            user["code"]="001"      #code:001 代表该up主视频信息获取成功
            user.pop('url_list')    #删除视频链接，无用信息
            save_num+=1
            if(save_num%2==0):      #及时保存
                print("save success")
                self.save()
            print(f"save:{save_num} {user['name']} finish")
        # print(user)
        print("All finish")
        return 

    
    def run(self):
        self.get_url()
        self.get_data()
        self.save()
        return
    
    def save(self):
        '''
        保存现有信息
        '''
        with open(f"{self.year}_top.json","w",encoding="utf-8") as f:
           json.dump(self.user,f,ensure_ascii=False,indent=4)
           f.close()
        return




if __name__=="__main__":
    year=2024
    with open(f"{year}.json","r",encoding="utf-8") as f:
        user=json.load(f)
        f.close()
    bot=Spiker(user,year)
    bot.run()
    time.sleep(50)

#https://space.bilibili.com/3546382956759627/video