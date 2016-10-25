# coding=utf-8
from PIL import Image
from selenium import webdriver
import time
import re
import requests
from bs4 import BeautifulSoup

my_header = {
    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E)'
}


class check_credit(object):
    def __init__(self):
        self.login_url = 'http://192.168.2.229/axsxx/AASZUstd.ASP'
        self.screen_path = 'before.jpg'
        self.grade_url = 'http://192.168.2.229/AXSXX/aCHENGJISTD.asp'
        self.sum_credit = 0.0
        self.all_get_grade = 0.0
        self.average = 0.0
        self.driver = webdriver.PhantomJS(executable_path=r'I:\phantomjs-2.1.1-windows\bin\phantomjs.exe')
        self.s = requests.session()
        self.uid = ''
        self.name = ''
        self.sex = ''
        self.major = ''
        self.core_course = 0.0
        self.core_course_list = []
        self.required_course = 0.0
        self.required_course_list = []
        self.liberal_elective_course = 0.0
        self.liberal_elective_course_list = []
        self.science_elective_course = 0.0
        self.science_elective_course_list = []
        self.pro_elective_course = 0.0
        self.pro_elective_course_list = []
        self.not_found_class = 0.0
        self.not_found_class_list = []
        self.cids = {}

    def get_vcode(self):
        self.driver.get(self.login_url)
        time.sleep(0.5)
        self.driver.get_screenshot_as_file(self.screen_path)
        img = Image.open('before.jpg')
        img1 = img.crop([403, 218, 502, 241])
        img1.save('vcode.jpg')
        # img1.show()

    def login_and_get_source(self, (userid, passwd, vcode)):

        self.userid = userid
        self.passwd = passwd

        print u'正在登陆中...'
        useridElement = self.driver.find_element_by_name('USERID')
        passwdElement = self.driver.find_element_by_name('PASSWORD')
        codeElement = self.driver.find_element_by_name('GetCode')
        # print useridElement.get_attribute("type"), passwdElement.get_attribute("type")
        useridElement.send_keys(self.userid)
        passwdElement.send_keys(self.passwd)
        codeElement.send_keys(vcode)
        submitElement = self.driver.find_element_by_name('SUBMIT')

        submitElement.submit()
        time.sleep(2)
        try:
            self.driver.find_element_by_tag_name('body')
            print u'登陆失败，请重新登陆'
            return False
        except:
            self.driver.get(self.grade_url)
            self.credit_html = self.driver.page_source
            bsObj = BeautifulSoup(self.credit_html, 'html.parser')
            tds = bsObj.findAll('td')
            self.uid = tds[1].text.strip()
            self.name = tds[3].text.strip()
            self.sex = tds[5].text.strip()
            self.major = tds[7].text.strip()
            return True

    def get_message(self):
        pattern1 = re.compile(ur'所选学分:(.*?)</small>', re.S)
        pattern2 = re.compile(ur'平均学分绩点:(.*?)</small>', re.S)
        pattern3 = re.compile(ur'取得学分:(.*?)</small>', re.S)
        credit = pattern1.findall(self.credit_html)
        Grade = pattern2.findall(self.credit_html)
        get_credit = pattern3.findall(self.credit_html)
        sum_credit = 0.0
        average = 0.0
        all_get_grade = 0.0
        for i in get_credit:
            all_get_grade += float(i)
        for i in credit:
            sum_credit += float(i)
        for i in range(len(credit)):
            average += (float(credit[i]) / sum_credit) * float(Grade[i])
        # print sum_credit, all_get_grade, average
        self.sum_credit, self.all_get_grade, self.average = sum_credit, all_get_grade, average

    def show_message(self):
        print u'{} | {} | {} | {} '.format(self.uid, self.name, self.sex, self.major)
        print u'所选学分：{0} 取得学分：{1} 平均学分绩点{2} '.format(self.sum_credit, self.all_get_grade, self.average)

    def get_class_details(self, cid):
        params = {
            'bh': str(cid),
        }
        r = self.s.get('http://192.168.2.229/newkc/akcjj0.asp?xqh='+str(self.cids[cid]), headers=my_header) #获得cookies
        r = self.s.post('http://192.168.2.229/newkc/kccx.asp?flag=kch', headers=my_header, data=params)
        text = r.content.decode(encoding='gb18030')
        bsObj = BeautifulSoup(text, 'html.parser')
        trs = bsObj.findAll('tr')
        tr = trs[1]
        tds = tr.findAll('td')
        tmp = tds[7].text.strip()
        if tmp in (u'公共必修课', u'综合必修'):
            self.required_course += float(tds[3].text)
            self.required_course_list.append(u'{} {}'.format(tds[2].text.strip(), float(tds[3].text)))
        elif tmp in (u'学科专业核心课', u'专业必修'):
            self.core_course += float(tds[3].text)
            self.core_course_list.append(u'{} {}'.format(tds[2].text.strip(), float(tds[3].text)))
        elif tmp in (u'综合选修', u'学科专业选修课'):
            self.pro_elective_course += float(tds[3].text)
            self.pro_elective_course_list.append(u'{} {}'.format(tds[2].text.strip(), float(tds[3].text)))

        elif tmp in (u'公共选修课', u'综合选修'):
            if tds[13].text.strip() == u'理科学分':
                self.science_elective_course += float(tds[3].text)
                self.science_elective_course_list.append(u'{} {}'.format(tds[2].text.strip(), float(tds[3].text)))
            else:
                self.liberal_elective_course += float(tds[3].text)
                self.liberal_elective_course_list.append(u'{} {}'.format(tds[2].text.strip(), float(tds[3].text)))

        else:
            self.not_found_class += float(tds[3].text)
            self.not_found_class_list.append(u'{} {}'.format(tds[2].text.strip(), float(tds[3].text)))

    # 获取所有的课程id，然后去检索
    def get_class_as_dict(self):
        bsObj = BeautifulSoup(self.credit_html, 'html.parser')
        tables = bsObj.findAll('table')
        for table in tables:
            trs = table.findAll('tr')
            if trs is not None:
                for t in trs[1:]:
                    term = t.find('td', {'width': '6%'})
                    cid = t.find('td', {'width': '10%'})
                    if term and cid:
                        term = term.text.strip()
                        cid = cid.text.strip()
                        self.cids[cid] = term

    def search_cid(self):
        self.get_class_as_dict()
        for c in self.cids:
            self.get_class_details(c)
            time.sleep(0.1)
        print u'必修:{} 专业核心课：{} 专业选修:{} 文科选修：{} 理科选修：{} 无法分辨的学分 {}'.format(
            self.required_course, self.core_course, self.pro_elective_course,
            self.liberal_elective_course, self.science_elective_course,
            self.not_found_class)


    def run(self):
        # print u'hello'
        # while not self.login_and_get_source():
        #     pass
        # while True:
        #     comment = raw_input(u'请输入指令，c是查询平均绩点,s是查看学分种类，q是退出>>>')
        #     if comment.strip() == 'c':
        #         self.get_message()
        #         self.show_message()
        #     if comment.strip() == 's':
        #         self.search_cid()
        #     elif comment.strip() == 'q':
        #         print u'Bye Bye'
        #         self.driver.close()
        #         break
        #     else:
        #         print u'无效命令'
        pass

if __name__ == '__main__':
    c = check_credit()
    c.run()
