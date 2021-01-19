# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 16:18:41 2018

@author: xuanxuan
"""
#首先来写如何统计一个英文文本中单词出现的频率（非自己独立完成）
import glob
import os
import pdfplumber
import shutil
import win32api,win32con
import pymysql
import sys

DBHOST='172.26.90.183'
DBUSER='root'
DBPASS='root'
DBNAME='awsdatabase'


try:
    conn = pymysql.connect(host=DBHOST, user=DBUSER, password=DBPASS, database=DBNAME)
    print('数据库连接成功')
    # 使用 cursor() 方法创建一个游标对象 cursor
except pymysql.Error as e:
    print('数据库连接失败'+str(e))
cursor = conn.cursor()
# 使用 execute() 方法执行 SQL，如果表存在则删除
cursor.execute("SELECT * FROM pdftextextract")
# print(cursor.fetchall())
data=cursor.fetchall()

# 关闭数据库连接
conn.commit()
cursor.close()
conn.close()

def main():
    wordCounts={}    #先建立一个空的字典，用来存储单词 和相应出现的频次
    count=200       #显示前多少条（按照单词出现频次从高到低）
    file=open("D:/15954/AWSdataanalyse/count_word.txt",'r')
    # for line in file:
    # for list in data:
    #         for i in range (2,len(list)):
    #     print(line)
    for list1 in data:
        print("1")
        for i in range (2,len(list1)):
            print(list1[i])
            line=str(list1[i])
    #     print(line)
    # for line in file:
    #     print(line)
            lineprocess(line.lower(),wordCounts)  #对于每一行都进行处理，调用lineprocess()函数，参数就是从file文件读取的一行

            items0=list(wordCounts.items())       #把字典中的键值对存成列表，形如：["word":"data"]
            items=[[x,y] for (y,x) in items0]     #将列表中的键值对换一下顺序，方便进行单词频次的排序 就变成了["data":"word"]
            items.sort()            #sort()函数对每个单词出现的频次按从小到大进行排序

    for i in range(len(items)-1,len(items)-count-1,-1):   #上一步进行排序之后 对items中的元素从后面开始遍历 也就是先访问频次多的单词
        # if items[i][1] != ["a","b",'c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',"der","und"]:
         if len(items[i][1])>3 and items[i][1]!="vwcs":
            print(items[i][1]+"\t"+str(items[i][0]))




def lineprocess(line,wordCounts):
    for ch in line:   #对于每一行中的每一个字符 对于其中的特殊字符需要进行替换操作
        if ch in "~@#$%^&*()_-+=<>?/,.:;{}[]|\'""1234567890":
            line=line.replace(ch,"")
        # elif ch in [" a "," b "," c "," d "," e "," f "," g "," h "," i "," j "," k "]:
        #     line = line.replace(ch, "")
    words=line.split()  #替换掉特殊字符以后 对每一行去掉空行操作,也就是每一行实际的单词数量
    for word in words:
        if word in wordCounts:
            wordCounts[word]+=1
        else:
            wordCounts[word]=1

    #这个函数执行完成之后整篇文章里每个单词出现的频次都已经统计好了
#
main()