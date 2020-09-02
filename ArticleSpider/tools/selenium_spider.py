from time import sleep

from fake_useragent import UserAgent
from selenium import webdriver
from scrapy.selector import Selector
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# 进入开发者模式
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-automation'])
# b=webdriver.Chrome(executable_path='C:\\Users\\23607\\Desktop\\py\\chromedriver.exe',options=options)

# b=webdriver.Chrome(executable_path='C:\\Users\\23607\\Desktop\\py\\chromedriver.exe')

def get_ip_selenium(ip):
    ua = UserAgent()
    print('\n当前测试IP：',ip)
    # chromeOptions = webdriver.ChromeOptions()
    # chromeOptions.add_argument('user-agent={}'.format(ua.random))
    chromeOptions=Options()
    chromeOptions.add_argument("--proxy-server={}".format(ip))
    # chromeOptions.add_argument('--user-agent={}'.format(ua.random))
    b = webdriver.Chrome(executable_path='C:\\Users\\23607\\Desktop\\py\\chromedriver.exe',
                         chrome_options=chromeOptions)
    # b.get("http://httpbin.org/ip")
    b.implicitly_wait(10)
    b.get('https://www.baidu.com/')

    try:
        WebDriverWait(b, 10, 0.5).until(EC.presence_of_element_located((By.ID, 'head')))
        # WebDriverWait(b,10,0.5).until(EC.presence_of_element_located((By.ID,'su')))
        if '<html><head></head><body></body></html>' in b.page_source:
            sleep(3)
        if '未连接到互联网' in b.page_source:
            print('\n***代理不好使啦')
        elif '百度一下' in b.page_source:
            print('\n❤effective ip!', ip)
        else:
            print(b.page_source)
        if 'anti_Spider-checklogin&' in b.page_source:
            print('\n***被anti_Spider check啦')
    finally:
        b.close()
    sleep(1)
    b.quit()

random_ip = [ 'http://106.75.8.141:808', 'http://121.33.220.158:808',
              'http://61.135.155.82:443','http://119.4.45.103:61234']
for i in random_ip:
    get_ip_selenium(i)

# get_ip_selenium('http://115.219.107.19:8010')


# b=webdriver.Edge(executable_path='C:\\Users\\23607\\Desktop\\py\\msedgedriver.exe')
# options = webdriver.ChromeOptions()
# # 不加载图片,加快访问速度
# options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})

# from selenium.webdriver.chrome.options import Options
# # 接管浏览器
# chrome_options = Options()
# chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
# b=webdriver.Chrome(executable_path='C:\\Users\\23607\\Desktop\\py\\chromedriver.exe',chrome_options=chrome_options)

# b.get('https://zhihu.com/')
# b.find_element_by_xpath('//*[@id="root"]/div/main/div/div/div[2]/div/form/div[1]/div[2]').click()
#
# b.find_element_by_css_selector('.SignFlow-accountInputContainer div input[name="username"]').send_keys('18894899674')
# b.find_element_by_css_selector('.SignFlow-password div div input[name="password"]').send_keys('18894899674.')
#
# b.find_element_by_xpath('//*[@id="root"]/div/main/div/div/div[2]/div/form/button').click()
#
#b.get('https://weibo.com/')
# sleep(15)
# print(b.page_source)
# # 微博登录
# b.find_element_by_css_selector('#loginname').send_keys('18894899674')
# b.find_element_by_css_selector('.info_list.password div input[name="password"]').send_keys('18894899674.')
# b.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[6]/a').click()

# b.get('https://www.oschina.net/blog')
# sleep(5)
# for i in range(3):
#     b.execute_script('window.scrollTo(0,document.body.scrollHeight);var lenOfPage=document.body.scrollHeight; return lenOfPage')
#
#     sleep(3)
# b.quit()