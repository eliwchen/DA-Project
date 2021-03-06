# -*- coding: utf-8 -*-
from sklearn import tree
import sys
import os
import pandas as pd
import time
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_score
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

pd.set_option("display.max_columns",None) #显示所有列
pd.set_option('display.max_rows', None)  #显示所有行
pd.set_option('display.width',2000) #设置显示宽度

plt.rcParams['font.sans-serif']=['Microsoft YaHei'] # 正常显示中文字体
plt.style.use('seaborn-notebook') #选择美化样式 ['bmh', 'classic', 'dark_background', 'fast', 'fivethirtyeight', 'ggplot', 'grayscale', 'seaborn-bright', 'seaborn-colorblind', 'seaborn-dark-palette', 'seaborn-dark', 'seaborn-darkgrid', 'seaborn-deep', 'seaborn-muted', 'seaborn-notebook', 'seaborn-paper', 'seaborn-pastel', 'seaborn-poster', 'seaborn-talk', 'seaborn-ticks', 'seaborn-white', 'seaborn-whitegrid', 'seaborn', 'Solarize_Light2', 'tableau-colorblind10', '_classic_test']
sns.set_style({'font.sans-serif':['simhei','Arial']}) #设置字体风格
sns.set()#切换到seaborn的默认运行配置
from matplotlib.font_manager import FontProperties
myfont=FontProperties(fname=r'C:\Windows\Fonts\simhei.ttf',size=14)
sns.set(font=myfont.get_name())



"""数据导入"""
rowdata=pd.read_csv("data.csv",encoding='gbk')
data=rowdata.copy()
# print(data.head())
# print(data.info())
data["经验"]=data["一般要求"].str.split("/",expand=True)[0]
data["学历"]=data["一般要求"].str.split("/",expand=True)[1]
data["经验"]=data["一般要求"].str.split(" ",expand=True)[1]
data.drop("一般要求",axis=1,inplace=True)
data["城市"]=data["城市区域"].str.split("·",expand=True)[0]
data["区域"]=data["城市区域"].str.split("·",expand=True)[1]
data.drop("城市区域",axis=1,inplace=True)
data["最低工资(k)"]=data["薪资水平"].str.split("-",expand=True)[0]
data["最低工资(k)"]=data["最低工资(k)"].apply(lambda x:int(x.replace("k","")))
data["最高工资(k)"]=data["薪资水平"].str.split("-",expand=True)[1]
data["最高工资(k)"]=data["最高工资(k)"].apply(lambda x:int(x.replace("k","")))
data.drop("薪资水平",axis=1,inplace=True)
data["公司类型"]=data["公司信息"].str.split(" / ",expand=True)[0]
data["公司规模"]=data["公司信息"].str.split(" / ",expand=True)[2]
data["融资阶段"]=data["公司信息"].str.split(" / ",expand=True)[1]
data.drop("公司信息",axis=1,inplace=True)
data["经验"]=data["经验"].apply(lambda x:x.replace("经验",""))
data=data[["岗位名","岗位关键字","城市","区域","经验","学历","最高工资(k)","最低工资(k)","岗位诱惑"
           ,"公司名","公司类型","公司规模","融资阶段"]]
# print(data.head())

"""城市分析"""


#绘制非对称子图
fig1=plt.figure() #设置图窗口
ax1=plt.subplot2grid((2,2),(0,0)) #设置第一张子图，位置0,0
ax2=plt.subplot2grid((2,2),(0,1))  #设置第二张子图，位置0,1
ax3=plt.subplot2grid((2,2),(1,0),colspan=2)  #设置第三张子图，位置1,0开始，列跨度为2
plt.subplots_adjust(wspace=0.1, hspace=0.2)  # 调整子图间距

sns.barplot(x='城市', y='最低工资(k)', palette="Blues_d", data=data.sort_values("最低工资(k)",ascending=False), ax=ax1)
ax1.tick_params(axis='x',labelsize=6)
ax1.tick_params(axis='y',labelsize=6)
ax1.set_xlabel('城市',fontsize=10)
ax1.set_ylabel('最低工资(k)',fontsize=10)

sns.barplot(x='城市', y='最高工资(k)', palette="Greens_d", data=data, ax=ax2)
ax2.tick_params(axis='x',labelsize=6)
ax2.tick_params(axis='y',labelsize=6)
ax2.set_xlabel('城市',fontsize=10)
ax2.set_ylabel('最高工资(k)',fontsize=10)

data_city=data["城市"].value_counts().sort_values(ascending=False).to_frame().reset_index()
data_city.rename(columns=({'城市':'岗位需求量','index':'城市'}),inplace=True)
print(data_city)
# sns.countplot(data['城市'], palette="Reds_d", ax=ax3)
sns.barplot(x=data_city["城市"],y=data_city["岗位需求量"],palette="Reds_d", data=data_city, ax=ax3)#
ax3.tick_params(axis='x',labelsize=6)
ax3.tick_params(axis='y',labelsize=6)
ax3.set_xlabel('城市',fontsize=10)
ax3.set_ylabel('岗位需求量',fontsize=10)
plt.show()

# 首先安装对应的python模块
# pip install pyecharts==0.5.10
# pip install echarts-countries-pypkg
# pip install echarts-china-provinces-pypkg
# pip install echarts-china-cities-pypkg
# pip install echarts-china-counties-pypkg

# from pyecharts import Geo
# geo = Geo("数据分析岗位需求分布热力图", "data from Lagou", title_color="#fff",
#           title_pos="left", width=1200, height=600,
#           background_color='#404a59')
# geo.add("数据分析岗位需求分布热力图",data_city["城市"] , data_city["岗位需求量"],
#         visual_range=[0, 5], type='heatmap',
#         visual_text_color="#fff", symbol_size=15,
#         is_visualmap=True, is_roam=True)  # type有scatter, effectScatter, heatmap
#                                           # 三种模式可选，可根据自己的需求选择对应的图表模式
# geo.render(path="数据分析岗位需求分布热力图2.html")
# plt.show()

"""学历与经验分析"""
mypal=sns.diverging_palette(200, 20, l=40, n=4)
# fig2=plt.figure() #设置图窗口
# ax1=plt.subplot2grid((2,1),(0,0))
# ax2=plt.subplot2grid((2,1),(1,0))
# # ax3=plt.subplot2grid((2,2),(1,0))
# # ax4=plt.subplot2grid((2,2),(1,1))
# plt.subplots_adjust(wspace=0.1, hspace=0.2)  # 调整子图间距
# df_aca=data.groupby("学历")["区域"].count().sort_values(ascending=False).to_frame().reset_index()
# sns.barplot(y="学历",x="区域",data=df_aca.head(20),ax=ax1,orient="h",palette=mypal)
# ax1.set_xlabel("需求量",fontsize=10)
# ax1.set_ylabel("学历",fontsize=10)
# df_exp=data.groupby("经验")["区域"].count().sort_values(ascending=False).to_frame().reset_index()
# sns.barplot(x='经验', y='区域', palette=mypal, data=df_exp, ax=ax2)
# ax2.tick_params(axis='y',labelsize=6)
# ax2.set_xlabel('经验',fontsize=10)
# ax2.set_ylabel('需求量',fontsize=10)
# plt.show()

# df_aca2=pd.DataFrame()
# df_aca2["需求比例"]=df_aca["区域"]/sum(df_aca["区域"])
# df_aca2.index=df_aca["学历"]
# print(df_aca2)
# #
# ax2=plt.pie(x=df_aca2, explode=None, labels=df_aca2.index,
#     autopct='%1.2f%%', pctdistance=0.5, shadow=False,
#     labeldistance=1, startangle=None, radius=1.3,
#     counterclock=True, wedgeprops=None, textprops=None,
#     center = (0, 0), frame = False )
#
# """薪资分析"""
# print(data.describe())
# fig3,[[ax1,ax2,ax3],[ax4,ax5,ax6]]=plt.subplots(2,3)
# sns.boxplot(x='学历', y='最高工资(k)', data=data, ax=ax1,palette=mypal)
# ax1.tick_params(axis='x',labelsize=8)
# ax1.tick_params(axis='y',labelsize=8)
# ax1.set_xlabel('学历',fontsize=10)
# ax1.set_ylabel('最高工资',fontsize=10)
# sns.distplot(data["最高工资(k)"],ax=ax2,bins=20) #面积分布情况（直方图 ）
# sns.kdeplot(data["最高工资(k)"],shade=True,ax=ax2)#生成核密度图
# sns.boxplot(x='学历', y='最低工资(k)', data=data, ax=ax4,palette=mypal)
# ax4.tick_params(axis='x',labelsize=8)
# ax4.tick_params(axis='y',labelsize=8)
# ax4.set_xlabel('学历',fontsize=10)
# ax4.set_ylabel('最低工资',fontsize=10)
#
# sns.distplot(data["最低工资(k)"],ax=ax5,bins=20) #面积分布情况（直方图 ）
# sns.kdeplot(data["最低工资(k)"],shade=True,ax=ax5)#生成核密度图
#
# sns.boxplot(x='经验', y='最高工资(k)', data=data, ax=ax3,palette=mypal)
# ax3.tick_params(axis='x',labelsize=7)
# ax3.tick_params(axis='y',labelsize=7)
# ax3.set_xlabel('经验',fontsize=10)
# ax3.set_ylabel('最高工资',fontsize=10)
#
# sns.boxplot(x='经验', y='最低工资(k)', data=data, ax=ax6,palette=mypal)
# ax6.tick_params(axis='x',labelsize=7)
# ax6.tick_params(axis='y',labelsize=7)
# ax6.set_xlabel('经验',fontsize=10)
# ax6.set_ylabel('最低工资',fontsize=10)
# plt.show()
#
# fig4,[ax1,ax2]=plt.subplots(1,2)
# sns.countplot(data['公司规模'], palette=mypal, ax=ax1)
# ax1.tick_params(axis='y',labelsize=9)
# ax1.tick_params(axis='x',labelsize=9)
# ax1.set_xlabel('公司规模',fontsize=11)
# ax1.set_ylabel('需求量',fontsize=11)
#
# data["融资阶段"]=data["融资阶段"].apply(lambda x:x.replace("不需要融资","未融资"))
# sns.countplot(data['融资阶段'], palette=mypal, ax=ax2)
# ax2.tick_params(axis='y',labelsize=9)
# ax2.tick_params(axis='x',labelsize=9)
# ax2.set_xlabel('融资阶段',fontsize=11)
# ax2.set_ylabel('需求量',fontsize=11)
#
# plt.show()

"""数值映射编码进行相关性分析"""
labels1 = data["城市"].unique().tolist()  # tolist()将数组array变为列表list
data["城市"] = data["城市"].apply(lambda x: labels1.index(x))
labels2 = data["经验"].unique().tolist()  # tolist()将数组array变为列表list
data["经验"] = data["经验"].apply(lambda x: labels2.index(x))
labels3 = data["学历"].unique().tolist()  # tolist()将数组array变为列表list
data["学历"] = data["学历"].apply(lambda x: labels3.index(x))
labels4 = data["公司规模"].unique().tolist()  # tolist()将数组array变为列表list
data["公司规模"] = data["公司规模"].apply(lambda x: labels4.index(x))
labels5= data["融资阶段"].unique().tolist()  # tolist()将数组array变为列表list
data["融资阶段"] = data["融资阶段"].apply(lambda x: labels5.index(x))
print(labels2)
# print(data.head())
# colormap = plt.cm.RdBu
# plt.figure(figsize=(30,40))
# # plt.title('Pearson Correlation of Features', y=1.05, size=15)
# sns.heatmap(data.corr(),linewidths=0.1,vmax=1.0, square=False,
#             cmap=colormap, linecolor='white', annot=True,annot_kws={'size':10,'color':'black'})
# plt.show()