from appium import webdriver
import time
class Action(object):

    def __init__(self):
        #初始化配置，设置Desired Capabilities参数
        self.desired_caps = {
            "platformName": "Android",
            "deviceName": "HWEVA P9",
            "appPackage": "com.ss.android.ugc.aweme",
            "appActivity": ".main.MainActivity"
        }
        # 指定Appium Server
        self.server = 'http://localhost:4723/wd/hub'
        # 新建一个Session
        self.driver = webdriver.Remote(self.server, self.desired_caps)
        # 设置滑动初始坐标和滑动距离
        self.start_x = 538
        self.start_y = 917
        self.distance = 500

    def comments(self):
        i=1
        while i<4:
            time.sleep(2)
            # app开启之后点击一次屏幕，确保页面的展示
            self.driver.tap([(821, 1651)], 500) #第三个参数为持续时间
            i+=1

    def scroll(self):
        # 无限滑动
        while True:
            # 模拟滑动
            self.driver.swipe(self.start_x, self.start_y, self.start_x,
                              self.start_y - self.distance)
            # 设置延时等待
            # 设置延时等待
            time.sleep(2)

    def main(self):
        self.comments()
        self.scroll()


if __name__ == '__main__':
    action = Action()
    action.main()

