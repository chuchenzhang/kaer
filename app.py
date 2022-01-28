import os
import sys
import time

import numpy as np
# import pymysql

import cv2
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QUrl
# from PyQt5.uic.properties import QtCore
# from pyqt5_plugins.examplebuttonplugin import QtGui

import randomNumber
import Heroes


app_name = "卡秃子英雄随机器"


class MainWindow(QMainWindow):
    MARGIN = 0

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        # 主体窗口
        self.resize(1240, 734)
        # 设置窗口无边框和背景透明 *必须
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)  # 无边框
        self.setAttribute(Qt.WA_TranslucentBackground)

        # 中心控件
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)
        # 主布局 水平布局
        main_layout = QHBoxLayout(centralWidget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(QMargins(self.MARGIN, self.MARGIN, self.MARGIN, self.MARGIN))

        # 左侧菜单栏
        leftWidget = QWidget()
        leftWidget.setFixedSize(200, self.height())
        # 设置objectName来设置样式
        leftWidget.setObjectName("leftWidget")

        main_layout.addWidget(leftWidget)
        # leftWidget相对于main_layout左对齐
        main_layout.setAlignment(leftWidget, Qt.AlignLeft)
        left_layout = QVBoxLayout(leftWidget)

        # 左侧头像区域
        head_portrait = QWidget()
        # head_portrait.setStyleSheet('''QWidget{background: red;}''')
        head_portrait.setFixedSize(leftWidget.width(), 100)

        head_portrait_layout = QHBoxLayout(head_portrait)

        head_img = QLabel()
        head_img_pix = QPixmap("./images/kaer_head.png")
        head_img.setPixmap(head_img_pix)
        head_img.setScaledContents(True)  # 令图片自适应label大小
        head_img.setFixedSize(60, 60)
        head_portrait_layout.addWidget(head_img)

        app_title = QLabel(app_name)
        app_title.setObjectName("app_title")
        app_title.setWordWrap(True)
        # app_title.setFixedSize()
        head_portrait_layout.addWidget(app_title)

        left_layout.addWidget(head_portrait)

        # 左侧list
        items = ["随机英雄", "所有英雄", "添加英雄"]
        img_urls = ['item_random.png', 'item_heroes.png', 'item_add.png']

        self.left_list = QListWidget()
        # self.left_list.setStyleSheet('''QWidget{border: 1px solid red;}''')
        self.left_list.setObjectName("left_list")
        self.left_list.setMinimumSize(leftWidget.width(), 100)
        # self.left_list.setMaximumSize(leftWidget.width(), self.height() - head_portrait.height() - 10)

        # 自定义Item
        i = 0
        for item, img_url in zip(items, img_urls):
            custom_item = QListWidgetItem()
            custom_item.setSizeHint(QSize(leftWidget.width() - 4, 60))

            item_widget = self.get_item_widget(item, img_url)  # 调用函数返回生成widget控件
            self.left_list.insertItem(i, custom_item)
            i += 1
            self.left_list.setItemWidget(custom_item, item_widget)  # 自定义item
        # 默认选中QListWidget的第一项
        self.left_list.setCurrentItem(QListWidget.item(self.left_list, 0))

        left_layout.addWidget(self.left_list)

        # left_layout.setSpacing(10)  # 控件间边距
        left_layout.addStretch(1)  # 拉伸因子，会已有的部件紧凑挨近，只占据部件需要的大小位置，之后使用空白占据剩余的位置。
        left_layout.setContentsMargins(0, 0, 0, 0)  # 外边距

        # 创建三个面板
        self.stack_random = QWidget()
        self.stack_heroes = QWidget()
        self.stack_add = QWidget()
        self.stack_random.setFixedSize(self.width() - leftWidget.width() - 50, self.height() - 60)
        self.stack_heroes.setFixedSize(self.width() - leftWidget.width() - 50, self.height() - 60)
        self.stack_add.setFixedSize(self.width() - leftWidget.width() - 50, self.height() - 60)

        self.stack_random.setObjectName("stack_random")
        self.stack_heroes.setObjectName("stack_heroes")
        self.stack_add.setObjectName("stack_add")

        self.stack_random_ui()
        self.stack_heroes_ui()
        self.stack_add_ui()

        # 在QStackedWidget对象中填充三个子控件
        self.stack = QStackedWidget(self)
        self.stack.setObjectName("stack")
        # self.stack.resize(1000, 734)
        self.stack.addWidget(self.stack_random)
        self.stack.addWidget(self.stack_heroes)
        self.stack.addWidget(self.stack_add)

        # 右侧面板
        rightWidget = QWidget()
        rightWidget.setObjectName("rightWidget")
        # rightWidget.setStyleSheet('''QWidget{background: rgba(236,237,240,.3);}''')
        right_layout = QVBoxLayout(rightWidget)
        right_layout.setSpacing(14)

        # 右侧顶部关闭栏
        title_bar = QWidget()
        # title_bar.setStyleSheet('''background: rgba(240,240,240,.5);''')
        title_bar_layout = QHBoxLayout(title_bar)
        title_bar_layout.setContentsMargins(0, 0, 10, 0)  # 左 上 右 下
        title_bar_layout.setSpacing(10)

        title_bar_layout.addStretch()

        self.minimum_button = QPushButton('0', self)
        # self.maximum_button = QPushButton('1', self)
        self.close_button = QPushButton('r', self)
        title_bar_layout.addWidget(self.minimum_button, alignment=Qt.AlignRight)
        # title_bar_layout.addWidget(self.maximum_button, alignment=Qt.AlignRight)
        title_bar_layout.addWidget(self.close_button, alignment=Qt.AlignRight)
        font = QFont('webdings')  # 使用webding字体设置按钮的图标
        self.minimum_button.setFont(font)
        # self.maximum_button.setFont(font)
        self.close_button.setFont(font)
        self.minimum_button.setFixedSize(30, 30)
        # self.maximum_button.setFixedSize(30, 30)
        self.close_button.setFixedSize(30, 30)
        self.minimum_button.clicked.connect(self.window_minimum)  # 设置点击的信号事件
        # self.maximum_button.clicked.connect(self.window_maximum)
        self.close_button.clicked.connect(self.window_close)
        # 设置objectName来设置样式
        self.minimum_button.setObjectName('minimumButton')
        # self.maximum_button.setObjectName('maximumButton')
        self.close_button.setObjectName('closeButton')

        right_layout.addWidget(title_bar)
        right_layout.addWidget(self.stack, alignment=Qt.AlignCenter)
        right_layout.setContentsMargins(0, 0, 0, 0)

        right_layout.addStretch()

        main_layout.addWidget(rightWidget)
        # main_layout.addStretch(1)

        self.left_list.currentRowChanged.connect(self.display)

        # 总css样式
        # self.window().setStyleSheet('''
        #     *{
        #         margin: 0;
        #         padding: 0;
        #     }
        #     @font-face {
        #         font-family: 'webfont';
        #         font-display: swap;
        #         src: url('//at.alicdn.com/t/webfont_jq0mkvmpxhn.eot'); /* IE9*/
        #         src: url('//at.alicdn.com/t/webfont_jq0mkvmpxhn.eot?#iefix') format('embedded-opentype'), /* IE6-IE8 */
        #         url('//at.alicdn.com/t/webfont_jq0mkvmpxhn.woff2') format('woff2'),
        #         url('//at.alicdn.com/t/webfont_jq0mkvmpxhn.woff') format('woff'), /* chrome、firefox */
        #         url('//at.alicdn.com/t/webfont_jq0mkvmpxhn.ttf') format('truetype'), /* chrome、firefox、opera、Safari, Android, iOS 4.2+*/
        #         url('//at.alicdn.com/t/webfont_jq0mkvmpxhn.svg#NotoSansHans-Black') format('svg'); /* iOS 4.1- */
        #     }
        #     #leftWidget{
        #         background: rgba(170,183,183,.8);
        #     }
        #     #app_title{
        #         color: white;
        #         font-size: 22px;
        #         font-family: 微软雅黑;
        #     }
        #     #left_list{
        #         background: transparent;
        #     }
        #     #left_list::Item{
        #         height: 60px;
        #         text-align: center;
        #         color: white;
        #         font: 18px;
        #     }
        #     #left_list::Item:hover{
        #         background: rgba(60,62,66,.8);
        #     }
        #     #left_list::Item:selected{
        #         background: rgba(60,62,66,.8);
        #     }
        #     #left_list::Item:selected:!active{
        #         background: rgba(60,62,66,.8);
        #     }
        #     #rightWidget{
        #         background: rgba(137, 143, 158, 0.6);
        #     }
        #     #minimumButton, #maximumButton, #closeButton{
        #         border: none;
        #         background-color: rgb(34,102,175);
        #     }
        #     #minimumButton:hover,#maximumButton:hover {
        #         color: rgb(33,165,229);
        #     }
        #     #closeButton:hover {
        #         color: rgb(200,49,61);
        #     }
        #     #stack_random,#stack_heroes,#stack_add{
        #         background: rgba(173,226,217,.3);
        #         border-radius: 10px;
        #     }
        #     #amount, #amount QLabel,#amount QLineEdit{
        #         background-color: transparent;
        #         color: white;
        #     }
        #     #random_hero_res{
        #         border: 2px solid gray;
        #         border-radius: 10px;
        #     }
        #     #randomBtn{
        #         height: 100px;
        #     }
        #     #add_form{
        #         border: 1px solid red;
        #         background: transparent;
        #     }
        #     #add_form *{
        #         color: white;
        #     }
        #     #add_form QLineEdit,#add_form QComboBox,#add_form QPushButton{
        #         height: 30px;
        #         background: transparent;
        #         border: 1px solid black;
        #     }
        #     QComboBox QAbstractItemView { /* 下拉后的整个下拉窗体样式 */
        #         background: rgba(168,209,209,.9);
        #     }
        #     QComboBox QListView::item{  /* 下拉项样式 背景蓝色 */
        #         padding-left:30px;
        #         background:pink;
        #         color:#ffffff;
        #     }
        #     QComboBox QListView::item:selected{   /* 下拉项选中样式（效果不明显）*/
        #         color:#DCDCDC;
        #         background: pink;
        #     }
        #     QComboBox QListView::item:hover{  /* 下拉项鼠标悬浮样式 背景灰绿色 */
        #         color:#DCDCDC;
        #         background:#3da79d;
        #     }
        # ''')

    def stack_random_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(4, 4, 4, 4)
        # layout.addWidget(QLabel('random hero'))
        # 随机英雄结果展示区域
        random_hero_res = QWidget()
        random_hero_res.setObjectName("random_hero_res")
        # random_hero_res.setStyleSheet('''background: blue;''')
        self.random_hero_res_layout = QHBoxLayout(random_hero_res)
        self.random_hero_res_layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(random_hero_res)

        # 操作区
        random_operation = QWidget()
        # random_operation.setStyleSheet('''background: pink;''')
        random_operation_layout = QVBoxLayout(random_operation)

        # 设置随机数量 表单布局
        amount = QWidget(self)
        amount.setObjectName("amount")
        # amount.setStyleSheet('''background: red;''')
        amount.setFixedSize(random_operation.width(), 80)
        amount.setContentsMargins(104, 0, 0, 0)
        amount_layout = QFormLayout(amount)
        # 创建单行文本框
        self.amountEdit = QLineEdit('2')
        self.amountEdit.setFixedSize(200, 40)
        self.amountEdit.setAlignment(Qt.AlignCenter)
        self.amountEdit.setPlaceholderText("输入数字1-9")
        # 实例化整型校验器，并设置范围（0-100）
        inputValidator = QIntValidator(1, 9)
        self.amountEdit.setValidator(inputValidator)
        # 把文本框添加到布局，第一个参数为左侧的说明标签
        amount_layout.addRow('数\40\40量：', self.amountEdit)

        # 开始随机按钮
        self.randomBtn = QPushButton('开\40\40\40始')
        self.randomBtn.setObjectName("randomBtn")
        self.randomBtn.setFixedSize(200, 60)
        # 按钮绑定随机查询函数
        self.randomBtn.clicked.connect(self.doAction)

        random_operation_layout.addWidget(amount)
        random_operation_layout.setAlignment(amount, Qt.AlignCenter)  # 控件居中
        random_operation_layout.addWidget(self.randomBtn)
        random_operation_layout.setAlignment(self.randomBtn, Qt.AlignCenter)

        layout.addWidget(random_operation)

        # 定时器，周期性执行某段程序或某个函数
        self.timer = QBasicTimer()
        self.stack_random.setLayout(layout)

    def stack_heroes_ui(self):
        layout = QHBoxLayout()
        # layout.addWidget(QLabel('al heroes'))

        # 定义滚动区域
        self.sa = QScrollArea(self)
        self.sa.setObjectName('scrollArea')
        # 滑动条样式
        self.sa.setStyleSheet('''
            QScrollBar:vertical{ /* 竖直滚动条，水平滚动条用horizontal，都不加则表示所有滚动条 */
                border-radius:7px;  /* 滚动条的滑轨的圆角 */
                background:#858585;    /* 滚动条的滑轨的背景颜色 */
                padding-top:14px;   /* 滚动条上部增加padding */
                padding-bottom:14px;
                width: 10px;
            }
            QScrollBar::handle:vertical{
                background: #79b1b1;    /* 滚动条颜色 */
                border-radius: 10px;      /* 滚动条圆角 */
                /* 滚动条和滑轨之间的左间隙 */
                /**
                margin-left:2px;        
                margin-right:2px;
                **/
            }
            QScrollBar::handle:vertical:hover{  /* 鼠标放上滑块滑块变色 */
                background:gray;
                border-radius:6px;
            }
            QScrollBar::add-line:vertical{  /* 下方箭头 */
                width:30px;height:40px;      /* 设置箭头区域的宽高 */
                image:url('');
                border-radius: 15px;
                background: #858585;
            }
            QScrollBar::sub-line:vertical{  /* 上方箭头 */
                width:30px;height:40px;
                image:url('');
                border-radius: 15px;
                background: #858585;
            }
            QScrollBar::add-line:vertical:hover /* 鼠标放到下箭头箭头变成其他图片 */
            {
                width:30px;height:40px;
                image:url('');
                control-position:bottom;
            }
            QScrollBar::sub-line:vertical:hover{ /* 鼠标放到上箭头箭头变成其他图片 */
                width:30px;height:40px;
                image:url('');
                control-position:top;
            }
            QScrollBar::add-page:vertical{  /* 滑块已经经过的滑轨区域的颜色，若没有这里的设置，该区域会呈现网格状，不美观 */
                background:#e3e7e7;
            }
            QScrollBar::sub-page:vertical{  /*  滑块还没经过的滑轨区域的颜色，若没有这里的设置，该区域会呈现网格状，不美观 */
                background:#a3b0b0;
            }
        ''')
        # 定义滚动区域的Widget
        self.hero_plat = QWidget()
        self.hero_plat.setStyleSheet('''
            background: transparent;
        ''')
        self.hero_plat_layout = QVBoxLayout(self.hero_plat)
        # 显示所有英雄
        displayHeroes = Heroes.Heroes(None)
        self.hero_plat_layout.addWidget(displayHeroes.select())
        self.hero_plat.setLayout(self.hero_plat_layout)

        # 将self.hero_plat widget布置到滚动区域上
        self.sa.setWidget(self.hero_plat)
        # 将滚筒区域布置到layout布局上
        layout.addWidget(self.sa)

        self.stack_heroes.setLayout(layout)

    def stack_add_ui(self):
        layout = QVBoxLayout()
        # layout.addWidget(QLabel('add hero'))

        add_form = QWidget()
        add_form.setObjectName('add_form')
        add_form_layout = QFormLayout(add_form)

        # 创建文本框
        self.heroNameEdit = QLineEdit()
        self.nickNameEdit = QLineEdit()
        self.vocationCombo = QComboBox(self)
        self.vocationCombo.addItems(['战士', '坦克', '法师', '刺客', '射手', '辅助'])
        # 上传图片按钮
        uploadPicBtn = QPushButton('上传图片')
        uploadPicBtn.clicked.connect(self.openImage)
        # 标签显示图片
        self.labHeroIcon = QLabel('请上传\n\n英雄头像')
        self.labHeroIcon.setFixedSize(120, 120)
        self.labHeroIcon.setStyleSheet(
            "QLabel{background:transparent;border: 1px solid rgb(71, 149, 220);}"
            "QLabel{font-size:18px;font-weight:bold;font-family:宋体;color: white;}"
        )
        # 提交按钮
        submit = QPushButton('添加英雄')
        submit.clicked.connect(self.uploadHeroData)

        add_form_layout.addRow('英雄名称：', self.heroNameEdit)
        add_form_layout.addRow('英雄昵称：', self.nickNameEdit)
        add_form_layout.addRow('英雄位置：', self.vocationCombo)
        add_form_layout.addRow('', uploadPicBtn)
        add_form_layout.addRow('预\40\40\40\40览：', self.labHeroIcon)
        add_form_layout.addRow('', submit)

        layout.addWidget(add_form)

        self.stack_add.setLayout(layout)

    # 循环执行random()函数
    def timerEvent(self, e):
        time.sleep(0.1)
        self.random()

    def doAction(self, value):
        # print("do action")
        if self.timer.isActive():
            # print('停止随机...')
            self.timer.stop()
            self.randomBtn.setText('开\40\40\40始')
        else:
            # print('正在随机...')
            self.timer.start(100, self)
            self.randomBtn.setText('停\40\40\40止')

    # 随机英雄
    def random(self):
        amount = int(self.amountEdit.text())  # 字符型转int型
        # 判断为空
        # if self.amountEdit.text() == '':
        #     pass
        self.data = randomNumber.randomHero(amount)
        # print(self.data)
        if self.data is None:
            QMessageBox.about(self, '提示', '数量不能为0')
            self.timer.stop()
            self.randomBtn.setText('开\40\40\40始')
            return
        # 清除上一次随机的英雄头像widget控件
        for i in range(self.random_hero_res_layout.count()):
            self.random_hero_res_layout.itemAt(i).widget().deleteLater()
        # 显示图片在label上
        for hero in self.data:
            pix = QPixmap(hero[4])
            self.headIcon = QLabel()
            self.headIcon.setPixmap(pix)
            self.headIcon.setStyleSheet("background: rgb(236,215,167)")
            self.headIcon.setFixedSize(120, 120)
            self.headIcon.setToolTip(hero[1] + ' ' + hero[2])
            self.random_hero_res_layout.addWidget(self.headIcon)

    # 打开图片
    def openImage(self):
        # imgName 图片地址
        imgName, imgType = QFileDialog.getOpenFileName(self, "打开图片", "*.jpg;;*.png;;*.jpeg")
        # 取消选择
        if imgName == "":
            self.labHeroIcon.setText('请上传\n\n英雄头像')
            return
        jpg = QPixmap(imgName).scaled(self.labHeroIcon.width(), self.labHeroIcon.height())
        self.labHeroIcon.setPixmap(jpg)
        self.iconUrl = imgName  # C:/Users/出陈/Desktop/Python/kaer/LOL/Bard.png

    # 上传至本地sql文件
    def uploadHeroData(self, event):
        global hero_info
        if self.heroNameEdit.text() == '' or self.nickNameEdit.text() == '' or self.vocationCombo.currentText() == '':
            QMessageBox.about(self, '提示', '请填写英雄信息')
            return
        try:
            img_path = os.path.split(self.iconUrl)[1]
            img_path = 'heroes/' + img_path
            print(img_path)  # heroes/xxx.png
            hero_info = (
                self.heroNameEdit.text(),
                self.nickNameEdit.text(),
                self.vocationCombo.currentText(),
                img_path
            )
        except AttributeError as e:
            print(e)
            QMessageBox.about(self, '提示', '请上传英雄头像')
            return
        # 插入数据库
        add = Heroes.Heroes(hero_info)
        add.insert()

        # 防止路径中含有中文
        # 借助于numpy来读入数据，然后cv2.imdecode()把数据转换(解码)成图像
        img = cv2.imdecode(np.fromfile(self.iconUrl, dtype=np.uint8), -1)

        # 将图片写入指定文件夹
        cv2.imwrite(img_path, img)

        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # 反馈
        QMessageBox.about(self, '提示', '英雄添加成功')

        # 清空文本框内容以及图片信息
        self.heroNameEdit.setText('')
        self.nickNameEdit.setText('')
        self.vocationCombo.setCurrentIndex(0)
        self.labHeroIcon.setPixmap(QPixmap(""))
        self.labHeroIcon.setText('请上传\n英雄头像')

        # 所有英雄面板刷新数据
        # 删除旧的控件
        for i in range(self.hero_plat_layout.count()):
            self.hero_plat_layout.itemAt(i).widget().deleteLater()
        # 重新请求数据
        displayHeroes = Heroes.Heroes(None)
        self.hero_plat_layout.addWidget(displayHeroes.select())
        self.hero_plat.setLayout(self.hero_plat_layout)
        # 将self.hero_plat widget布置到滚动区域上
        self.sa.setWidget(self.hero_plat)

    def display(self, i):
        # 设置当前可见选项卡的索引
        self.stack.setCurrentIndex(i)

    # 自定义Item
    def get_item_widget(self, item, img_url):
        widget = QWidget()
        widget.setStyleSheet('''color: white;''')

        item_widget = QWidget()
        item_widget_layout = QHBoxLayout(item_widget)
        # list图标
        item_icon = QLabel()
        item_icon_pix = QPixmap('./images/' + img_url)
        item_icon.setScaledContents(True)
        item_icon.setFixedSize(30, 30)
        item_icon.move(3, 3)
        item_icon.setPixmap(item_icon_pix)
        item_widget_layout.addWidget(item_icon)
        # list名称
        item_title = QLabel()
        item_title.setText(item)
        item_widget_layout.addWidget(item_title)

        widget.setLayout(item_widget_layout)

        return widget

    # 背景图片
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(Qt.NoPen)
        brush = QBrush()
        brush.setTextureImage(QImage("./images/bilgewater.png"))  # brush来加载背景图
        painter.setBrush(brush)  # painter来加载brush
        painter.setRenderHint(QPainter.Antialiasing)  # 抗锯齿化，如果不加的话，圆角的会有锯齿
        painter.drawRoundedRect(0, 0, self.width() - 0, self.height() - 0, 5, 5)  # 圆角设置

    def window_minimum(self):
        self.showMinimized()

    def window_maximum(self):
        if self.maximum_button.text() == '1':
            self.maximum_button.setText('2')
            self.showMaximized()
        else:
            self.maximum_button.setText('1')
            self.showNormal()

    def window_close(self):
        self.close()

    # 重写移动事件
    def mouseMoveEvent(self, e: QMouseEvent):
        self._endPos = e.pos() - self._startPos
        self.move(self.pos() + self._endPos)

    def mousePressEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._isTracking = True
            self._startPos = QPoint(e.x(), e.y())

        if e.button() == Qt.RightButton:
            pass

    def mouseReleaseEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._isTracking = False
            self._startPos = None
            self._endPos = None

        if e.button() == Qt.RightButton:
            pass


# 公共类 加载qss文件
class CommonHelper:
    def __init__(self):
        pass

    @staticmethod
    def readQss(style):
        with open(style, 'r', encoding='UTF-8') as f:
            return f.read()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    the_mainWindow = MainWindow()

    # 加载qss文件
    styleFile = './style.qss'
    qssStyle = CommonHelper.readQss(styleFile)
    the_mainWindow.setStyleSheet(qssStyle)

    the_mainWindow.show()
    sys.exit(app.exec_())