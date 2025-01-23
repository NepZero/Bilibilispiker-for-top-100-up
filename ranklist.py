import json
import os
from matplotlib import pyplot as plt
from matplotlib.ticker import PercentFormatter
import pandas as pd
import statistics

class Ranklist:
    def __init__(self,year):
        self.year=year
        self.users=[]
        #显示中文
        plt.rcParams['font.sans-serif'] = ['SimHei']
        #打开文件
        if(os.path.exists(f"{year}_top.json")):
            self.users=pd.read_json(f"{year}_top.json",encoding="utf-8", orient='records')
            # print(self.users["video"][0][0])
        else:
            print("No such file")

    def video_num(self):
        """
        百大up视频量的柱状图
        """
        video_num=[]
        for i in self.users["video"]:
            video_num.append(len(i))
        df = pd.DataFrame({"name": self.users["name"], "nums": video_num})
        df.sort_values("nums", inplace=True,ascending=False)
        plt.bar(df["name"],df["nums"])
        plt.title(f"{self.year}年百大up主视频数量")
        plt.xticks(rotation=270) #横坐标竖直显示
        plt.xlabel("up")
        plt.ylabel("视频数")
        plt.show()

    def video_num_cmp(self,years):
        """
        几年百大视频数量对比图
        """

        #整合这几年数据并绘制成折线
        for year in years:
            if(os.path.exists(f"{year}_top.json")):
                users=pd.read_json(f"{year}_top.json",encoding="utf-8", orient='records')
            else:
                print("No {year} file")
                return
            video_num=[]
            for i in users["video"]:
                video_num.append(len(i))
            df = pd.DataFrame({"name": users["name"], "nums": video_num})
            df.sort_values("nums", inplace=True,ascending=False)
            plt.plot(list(range(1,101)),df["nums"])
        
        #设置label
        plt.legend(years, ncol=2, prop={"family": "Times New Roman", "size": 20})
        plt.title(f"百大up主视频数量对比")
        plt.xlabel("up")
        plt.ylabel("视频数")
        plt.show()


    def viewcoinratio(self):
        """
        百大up投币数/播放量的柱状图
        """

        #求每个up主的平均ratio
        ratios=[]
        for i in self.users["video"]:
            ratio=[]
            for j in i:
                ratio.append(self.tonumber(j["coin"])/self.tonumber(j["view"]))
            ratios.append(statistics.mean(ratio))

        df = pd.DataFrame({"name": self.users["name"], "ratios": ratios})
        df.sort_values("ratios", inplace=True,ascending=False)
        #设置纵坐标为百分比
        fig, ax = plt.subplots()
        ax.bar(df["name"], df["ratios"])
        ax.yaxis.set_major_formatter(PercentFormatter(1))
        plt.title(f"{self.year}年百大up主投币数/播放量")
        plt.xticks(rotation=270) #横坐标竖直显示
        plt.xlabel("up")
        plt.ylabel("Ratio")
        plt.show()

    def viewcoinratio_cmp(self,years):
        """
        几年百大投币数/播放量对比图
        """

        fig, ax = plt.subplots()
        ax.yaxis.set_major_formatter(PercentFormatter(1))
        #整合这几年数据并绘制成折线
        for year in years:
            if(os.path.exists(f"{year}_top.json")):
                users=pd.read_json(f"{year}_top.json",encoding="utf-8", orient='records')
            else:
                print("No {year} file")
                return
            
            ratios=[]
            for i in users["video"]:
                ratio=[]
                for j in i:
                    ratio.append(self.tonumber(j["coin"])/self.tonumber(j["view"]))
                ratios.append(statistics.mean(ratio))
            df = pd.DataFrame({"name": users["name"], "ratios": ratios})
            df.sort_values("ratios", inplace=True,ascending=False)
            ax.plot(list(range(1,101)), df["ratios"])
            # plt.plot(list(range(1,101)),df["ratios"])
        
        #设置label
        plt.legend(years, ncol=2, prop={"family": "Times New Roman", "size": 20})
        plt.title(f"百大up主投币数/播放量对比")
        plt.xlabel("up")
        plt.ylabel("Ratio")
        plt.show()

    def view_mean(self):
        """
        百大up主平均视频播放量柱状图
        """
        views=[]
        for i in self.users["video"]:
            view=[]
            for j in i:
                view.append(self.tonumber(j["view"]))
            views.append(statistics.mean(view)/1e4)
        
        df = pd.DataFrame({"name": self.users["name"], "views": views})
        df.sort_values("views", inplace=True,ascending=False)
        plt.bar(df["name"], df["views"])
        plt.title(f"{self.year}年百大up主平均视频播放量")
        plt.xticks(rotation=270) #横坐标竖直显示
        plt.xlabel("up")
        plt.ylabel("播放量(万)")
        plt.show()
        

    def tonumber(self,number):
        """
        将中文数字转化为实际数字
        """
        if(number[-1]=="万"):
            return(float(number[:-1])*1e4)
        else:
            return(float(number))




if __name__=="__main__":
    rank=Ranklist(2023)
    # rank.viewcoinratio()
    # rank.viewcoinratio_cmp([2023,2024])
    rank.video_num_cmp([2023,2024])

