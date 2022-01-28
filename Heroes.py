import os

import numpy as np
import pymysql
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QGroupBox, QGridLayout, QWidget
from PyQt5.QtCore import QUrl

class Heroes(object):

    def __init__(self, heroInfo):

        self.heroInfo = heroInfo
        # if not self.heroInfo:
        #     print('heroInfo is null')
        # self.insert()
        self.db = pymysql.connect(
            host="127.0.0.1",
            port=3306,
            user="root",
            password="root",
            db="kaer",
            charset="utf8"
        )

    def insert(self):

        cursor = self.db.cursor()

        sql = "INSERT INTO HEROES (HERO_NAME, NICK_NAME, VOCATION, URL) VALUES ('%s','%s','%s','%s')" % self.heroInfo

        try:
            cursor.execute(sql)

            self.db.commit()

            print('Dialog: insert successful')
        except:
            print('Error: insert failed')

        self.db.close()

    def select(self):

        global data
        # db = pymysql.connect(host='127.0.0.1', user='root', password='root', database='kaer', charset='utf8')

        cursor = self.db.cursor()

        sql = "select id,hero_name,nick_name,url from heroes order by id"

        try:
            cursor.execute(sql)

            data = cursor.fetchall()
            # print(data)
        except:
            print('Error: unable to fetch data')

        # print(len(heroes))
        # 计算一行5张图片占用行数
        div = len(data) // 5  # 商
        mod = len(data) % 5  # 余数
        # print(len(data))
        # print(div,mod)
        if mod != 0:
            row = div + 1
        else:
            row = div

        positions = [(i, j) for i in range(row) for j in range(5)]
        # print(positions)

        groupBox = QWidget()
        vLayout = QGridLayout(groupBox)
        # 遍历所有英雄头像
        for position, hero in zip(positions, data):
            # print(hero[3])
            pix = QPixmap(hero[3])
            lab = QLabel()
            lab.setPixmap(pix)
            lab.setFixedSize(120, 120)
            # 提示文本：英雄名称 名字
            lab.setToolTip(hero[1] + ' ' + hero[2])
            vLayout.addWidget(lab, *position)
            vLayout.setSpacing(69)

        groupBox.setLayout(vLayout)
        self.db.close()
        return groupBox
