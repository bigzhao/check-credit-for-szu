# coding=utf-8
import wx
from credit import *

TITLE = u"登陆"
USER = u"用   户"
PWD = u"密   码"
VC = u'验证码'
USR_LEN = 10
BUTTON_OK = u"确认"
BUTTON_CANCLE = u"取消"
TOP_TIP = u"学分|绩点查询 "




class CheckCredit(wx.Frame):
    def __init__(self, c, parent=None, title=u'绩点 | 学分 查询'):
        super(CheckCredit, self).__init__(parent, title=title,
            size=(1200, 500))
        self.c = c
        self.InitUI(self.c.average, self.c.sum_credit, self.c.all_get_grade)
        self.Centre()

    def InitUI(self, average, sum_credit, all_get_grade):
        self.panel = wx.Panel(self)
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        score = wx.StaticText(self.panel, label=u"平均绩点：{}".format(average))
        hbox.Add(score, proportion=2)
        sum = wx.StaticText(self.panel, label=u"全部学分：{}".format(sum_credit))
        hbox.Add(sum, proportion=1)
        all_get = wx.StaticText(self.panel, label=u"取得学分：{}".format(all_get_grade))
        hbox.Add(all_get, proportion=1)
        self.button = wx.Button(self.panel, -1, u'点击查看具体学分')
        self.button.SetDefault()
        self.Bind(wx.EVT_BUTTON, self.get_detail, self.button)
        hbox.Add(self.button, proportion=2)
        self.vbox.Add(hbox,flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)
        self.panel.SetSizer(self.vbox)

    def get_require_detail(self):
        """必修课显示框"""
        content = u''
        for course in self.c.required_course_list:
            content += course
            content += u'\n'
        richText = wx.TextCtrl(self.panel, -1,
                               content,
                               size=(200, 300),
                               # 创建丰富文本控件
                               style=wx.TE_MULTILINE | wx.TE_RICH2)
        richText.SetInsertionPoint(0)
        return richText

    def get_core_detail(self):
        """核心课显示框"""
        content = u''
        for course in self.c.core_course_list:
            content += course
            content += u'\n'
        richText = wx.TextCtrl(self.panel, -1,
                               content,
                               size=(200, 300),
                               # 创建丰富文本控件
                               style=wx.TE_MULTILINE | wx.TE_RICH2)
        richText.SetInsertionPoint(0)
        return richText

    def get_pro_elective_detail(self):
        """专业选修显示框"""
        content = u''
        for course in self.c.pro_elective_course_list:
            content += course
            content += u'\n'
        richText = wx.TextCtrl(self.panel, -1,
                               content,
                               size=(200, 300),
                               # 创建丰富文本控件
                               style=wx.TE_MULTILINE | wx.TE_RICH2)
        richText.SetInsertionPoint(0)
        return richText

    def get_liberal_elective_detail(self):
        """文科选修显示框"""
        content = u''
        for course in self.c.liberal_elective_course_list:
            content += course
            content += u'\n'
        richText = wx.TextCtrl(self.panel, -1,
                               content,
                               size=(200, 300),
                               # 创建丰富文本控件
                               style=wx.TE_MULTILINE | wx.TE_RICH2)
        richText.SetInsertionPoint(0)
        return richText

    def get_science_elective_detail(self):
        """理科选修显示框"""
        content = u''
        for course in self.c.science_elective_course_list:
            content += course
            content += u'\n'
        richText = wx.TextCtrl(self.panel, -1,
                               content,
                               size=(200, 300),
                               # 创建丰富文本控件
                               style=wx.TE_MULTILINE | wx.TE_RICH2)
        richText.SetInsertionPoint(0)
        return richText

    def get_not_found_detail(self):
        """找不到的课程显示框"""
        if self.c.not_found_class_list:
            st = wx.StaticText(self.panel, label=u'找不到匹配的课：')
            self.vbox.Add(st, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)
            content = u''
            for course in self.c.not_found_class_list:
                content += course
                content += u'\n'
                richText = wx.TextCtrl(self.panel, -1,
                                       content,
                                       size=(200, 300),
                                       # 创建丰富文本控件
                                       style=wx.TE_MULTILINE | wx.TE_RICH2)
                richText.SetInsertionPoint(0)
            return richText

    def get_detail(self, event):
        """按钮按下去后的操作函数"""
        self.button.Enable(False)
        c.search_cid()

        self.vbox.Add((-1, 10))

        # self.detail = wx.StaticText(self.panel, pos=(20, 100), label=u'必修:{} 专业核心课：{} 专业选修:{} '
        #                                                            u'文科选修：{} 理科选修：{} 无法分辨的学分 {}'.format('5', '5', '5', '5', '5', '5'))
        self.detail = wx.StaticText(self.panel, label=u'必修:{} 专业核心课：{} 专业选修:{} '
                                                                   u'文科选修：{} 理科选修：{} 无法分辨的学分 {}'.format(
            self.c.required_course, self.c.core_course, self.c.pro_elective_course,
            self.c.liberal_elective_course, self.c.science_elective_course,
            self.c.not_found_class))
        self.vbox.Add((-1, 10))
        self.vbox.Add(self.detail,flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)
        rt1 = self.get_require_detail()
        rt2 = self.get_core_detail()
        rt3 = self.get_pro_elective_detail()
        rt4 = self.get_liberal_elective_detail()
        rt5 = self.get_science_elective_detail()
        rt6 = self.get_not_found_detail()
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(rt1, proportion=1)
        hbox.Add(rt2, proportion=1)
        hbox.Add(rt3, proportion=1)
        hbox.Add(rt4, proportion=1)
        hbox.Add(rt5, proportion=1)
        if rt6:
            hbox.Add(rt6, proportion=1)
        self.vbox.Add(hbox, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)


class LoginDialog(wx.Dialog):
    """
    登陆对话窗体,请勿直接调用ShowModal() ,调用Show()
    """

    def __init__(self, parent=None, title=TITLE, size=(400, 280),
                 userTxtLen=USR_LEN):
        wx.Dialog.__init__(self, parent, -1, title, size=size,
                           style=wx.DEFAULT_DIALOG_STYLE)
        self.txtCtrMap = {}  # 缓存输入框
        self.okBtn = None
        # self.pwdLen = pwdTxtLen
        self.usrLen = userTxtLen
        self.CreateCompment()

        # 构建label项

    def _dataTxtLabel(self):
        return ((USER, 0, self._OnUserTxtInput),
                (PWD, wx.TE_PASSWORD, self._OnPwdInput))

        # 构建button项

    def _dataWithButton(self):
        return ((wx.ID_OK, BUTTON_OK), (wx.ID_CANCEL, BUTTON_CANCLE))

        # 构建TextCtrl项
    def _CreateTxtLabel(self, sizer, eachLabel, eachStyle, eachHandler):
        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, eachLabel)
        box.Add(label, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        text = wx.TextCtrl(self, -1, size=(150, -1), style=eachStyle)
        text.Bind(wx.EVT_TEXT, eachHandler)
        box.Add(text, 1, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)
        sizer.Add(box, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        self.txtCtrMap[eachLabel] = text

    def _CreateBitPic(self, sizer):
        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, u'验证码')
        box.Add(label, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        text = wx.TextCtrl(self, -1, size=(150, -1))
        box.Add(text, 1, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)
        img = wx.Image('vcode.jpg', wx.BITMAP_TYPE_ANY)
        sb = wx.StaticBitmap(self, -1,  wx.BitmapFromImage(img))
        sizer.Add(box, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        sizer.Add(sb,  2, wx.ALIGN_CENTER | wx.ALL, 5)
        self.txtCtrMap[VC] = text

    def _CreateButton(self, btnSizer, eachID, eachLabel):
        btn = wx.Button(self, eachID, eachLabel)
        if eachID == wx.ID_OK:
            btn.SetDefault()
            self.okBtn = btn
            btn.Disable()
        btnSizer.AddButton(btn)

        # 根据数据项构建组建
    def CreateCompment(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        topTip = wx.StaticText(self, -1, TOP_TIP)
        sizer.Add(topTip, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        for eachLabel, eachStyle, eachHandler in self._dataTxtLabel():
            self._CreateTxtLabel(sizer, eachLabel, eachStyle, eachHandler)
        self._CreateBitPic(sizer)
        btnSizer = wx.StdDialogButtonSizer()
        for eachID, eachLabel in self._dataWithButton():
            self._CreateButton(btnSizer, eachID, eachLabel)
        btnSizer.Realize()
        sizer.Add(btnSizer, 1, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)
        self.SetSizer(sizer)

    def _OnUserTxtInput(self, event):
        self._EnableOrDisableOkBtn()

    def _OnPwdInput(self, event):
        self._EnableOrDisableOkBtn()

        # 确保两个框都有输入
    def _EnableOrDisableOkBtn(self):
        self.okBtn.Enable()
        usrStr = self.txtCtrMap[USER].GetValue()
        pwdStr = self.txtCtrMap[PWD].GetValue()
        if len(usrStr) != self.usrLen:
            self.okBtn.Disable()

    # 调用该函数将显示窗体并确定后可返回结果
    def Show(self):
        res = self.ShowModal()
        if res == wx.ID_OK:
            return (self.txtCtrMap[USER].GetValue(), self.txtCtrMap[PWD].GetValue(), self.txtCtrMap[VC].GetValue())

if __name__ == '__main__':
    c = check_credit()
    c.get_vcode()
    app = wx.PySimpleApp()
    while True:
        log = LoginDialog()
        res = log.Show()
        print res
        if c.login_and_get_source(res):
            log.Destroy()
            break
        c.get_vcode()
    c.get_message()
    frame = CheckCredit(c)
    frame.Show()
    app.MainLoop()
    c.driver.close()
    print 'done'