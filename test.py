import wx
import wx.xrc
import os

class PAGE():
    Unit = 0
    Time = 1
    Setting = 2

class GENERATION_VALUE():
    customInputMode = -1

class MainFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs)
        self.SetSize((400, 500))        #視窗大小
        self.SetTitle('Simple menu')    #視窗標題
        self.Centre()   # 把產生出來的視窗放在螢幕正中間
        self.pageIndex = PAGE.Unit      #指示當前所在的頁面
        self.tagsConfPath = ".\\test.conf"
        self.schedulConfPath = ""
        self.appRootConfPath = ".\\app_root.conf"
        self.applicationExePath = "%windir%\system32\SnippingTool.exe"
        self.existUnitList = self.ReadDataFile_Tags(self.tagsConfPath)
        
        

        # 頁面按鈕區域==========================================================
        switchBtnPanel = wx.Panel(self)
        switchBtnSizer = wx.BoxSizer(wx.HORIZONTAL)
        switchBtnPanel.SetSizer(switchBtnSizer)

        button_newUnit = wx.Button(switchBtnPanel, label="新規追加")
        button_time = wx.Button(switchBtnPanel, label="スケジュール")
        button_setting = wx.Button(switchBtnPanel, label="パラメータ設定")
        button_newUnit.Bind(wx.EVT_BUTTON, lambda event, idx=PAGE.Unit: self.ChangePage(event, idx))
        button_time.Bind(wx.EVT_BUTTON,lambda event, idx=PAGE.Time: self.ChangePage(event, idx))
        button_setting.Bind(wx.EVT_BUTTON, lambda event, idx=PAGE.Setting: self.ChangePage(event, idx))
        switchBtnSizer.Add(button_newUnit)
        switchBtnSizer.Add(button_time)
        switchBtnSizer.Add(button_setting)
        

        # 創建各種頁面
        self.newUnitPanel = wx.Panel(self)
        # self.newUnitPanel.Hide() 
        self.timePanel = wx.Panel(self)
        self.timePanel.Hide()
        self.settingPanel = wx.Panel(self)
        self.settingPanel.Hide()


        # 新規追加 頁面==========================================================
        # 參數
        self.newUnitName = wx.TextCtrl(self.newUnitPanel)
        self.newUnitSSID = wx.TextCtrl(self.newUnitPanel)
        self.existUnitListBox = wx.ListBox(self.newUnitPanel, choices = self.existUnitList, size=(200,300))
        #self.existUnitListBox.Bind(wx.EVT_LISTBOX,self.SelectUnit)
        unitCheckBtn = wx.Button(self.newUnitPanel, label="確定")
        unitCheckBtn.Bind(wx.EVT_BUTTON, self.CheckUnit)
        #unitModifyBtn = wx.Button(self.newUnitPanel, label="修正")
        unitDeleteBtn = wx.Button(self.newUnitPanel, label="消除")
        unitDeleteBtn.Bind(wx.EVT_BUTTON, self.DeleteUnit)
        
        # 布局
        newUnitbSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.newUnitPanel.SetSizer(newUnitbSizer)
        newUnitleftPart = wx.BoxSizer(wx.VERTICAL)
        newUnitleftPart.Add(wx.StaticText(self.newUnitPanel, label="既存コナンエアー"), flag=wx.ALL, border=5)
        newUnitleftPart.Add(self.existUnitListBox, flag=wx.ALL, border=0)

        newUnitrightPart = wx.BoxSizer(wx.VERTICAL)
        newUnitrightPart.Add(wx.StaticText(self.newUnitPanel, label="新規名前"), flag=wx.ALL, border=5)
        newUnitrightPart.Add(self.newUnitName)
        newUnitrightPart.Add(wx.StaticText(self.newUnitPanel, label="新規SSID"), flag=wx.ALL, border=5)
        newUnitrightPart.Add(self.newUnitSSID)
        newUnitrightPart.Add(wx.Panel(self.newUnitPanel, size=(1,10)))
        newUnitrightPart.Add(unitCheckBtn, flag=wx.ALIGN_CENTER|wx.ALL, border=10)
        #newUnitrightPart.Add(unitModifyBtn, flag=wx.ALIGN_CENTER|wx.ALL, border=10)
        newUnitrightPart.Add(unitDeleteBtn, flag=wx.ALIGN_CENTER|wx.ALL, border=10)
        
        newUnitbSizer.Add(wx.Panel(self.newUnitPanel, size=(10,1)))
        newUnitbSizer.Add(newUnitleftPart)
        newUnitbSizer.Add(wx.Panel(self.newUnitPanel, size=(20,1)))
        newUnitbSizer.Add(newUnitrightPart)
        
        

        # スケジュール時間 頁面==========================================================
        # 參數
        timebSizer = wx.BoxSizer(wx.VERTICAL)
        self.timePanel.SetSizer(timebSizer)
        scheduleList = ["test1, daily, 00:00,+00:30*?, , , , , , , ,","test, monthly, Mon1 09:30, Mon2 09:30, Mon3 09:30, Mon4 09:30, , , , , ,"]
        weekList = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]

        timebSizer.Add(wx.StaticText(self.timePanel, label="保存されたスケジュール"), flag=wx.ALL, border=5)
        timebSizer.Add(wx.ComboBox(self.timePanel,choices=scheduleList),flag=wx.ALL, border = 5)

        monthPart = wx.BoxSizer(wx.HORIZONTAL)
        monthPart.Add(wx.RadioButton(self.timePanel, label="毎月"), flag=wx.ALL, border = 10)
        timebSizer.Add(monthPart)

        timePart = wx.BoxSizer(wx.HORIZONTAL)
        hourList = ["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23"]
        minuteList = ["00","30"]
        timePart.Add(wx.ComboBox(self.timePanel, choices=hourList), flag=wx.ALL, border=5)
        timePart.Add(wx.StaticText(self.timePanel, label="時"), flag=wx.ALL, border=10)
        timePart.Add(wx.ComboBox(self.timePanel, choices=minuteList), flag=wx.ALL, border=5)
        timePart.Add(wx.StaticText(self.timePanel, label="分"), flag=wx.ALL, border=10)
        timebSizer.Add(timePart)

        btnPart = wx.BoxSizer(wx.HORIZONTAL)
        btnPart.Add(wx.Button(self.timePanel, label="確定"),flag=wx.ALL, border=10)
        #btnPart.Add(wx.Button(self.timePanel, label="修正"),flag=wx.ALL, border=10)
        btnPart.Add(wx.Button(self.timePanel, label="削除"),flag=wx.ALL, border=10)
        timebSizer.Add(btnPart)

        radioPart = wx.BoxSizer(wx.HORIZONTAL)
        radioPart.Add(wx.RadioButton(self.timePanel, label="30分ごと"), flag=wx.ALL, border = 10)
        radioPart.Add(wx.RadioButton(self.timePanel, label="5分ごと"), flag=wx.ALL, border = 10)
        timebSizer.Add(radioPart)


        # パラメータ設定 頁面==========================================================
        # 參數
        self.appRootPath = wx.TextCtrl(self.settingPanel)
        self.appRootPath.Bind(wx.EVT_LEFT_DCLICK, self.SelectPath)
        generationShowName = ["無制限","10個",""]
        generationCodeName = [0,10, GENERATION_VALUE.customInputMode]   # 跟上面這行對應，最後一個"自行輸入"的數值設為 -1
        self.generationCustonInput = wx.TextCtrl(self.settingPanel) # 自行輸入的輸入框
        dataSynchronizes = ["ON","OFF","OFF APP ONLY"]
        fileTypeShowName = ["CSVのみ", "要約CSV", "CNA", "要約CSV + CNA"]
        fileTypeCodeName = ["CSV","SUMMARY_CSV","CNA","SUMMARY_CSV+CNA"]    # 跟上面這行對應
        # 重要參數及預設值
        self.DATA_GEN = generationCodeName[0]
        self.DATA_SYNC = dataSynchronizes[0]
        self.FILE_TYPE = fileTypeCodeName[0]
        
        # 布局
        settingSizer = wx.BoxSizer(wx.VERTICAL)
        self.settingPanel.SetSizer(settingSizer)
        
        pathSizer = wx.BoxSizer(wx.HORIZONTAL)
        pathSizer.Add(wx.StaticText(self.settingPanel, label="フォルダー保存場所"),flag=wx.ALL, border=10)
        pathSizer.Add(self.appRootPath, flag=wx.ALL, border=5)
        #browseBtn = wx.Button(self.settingPanel, label="ブラウズ")
        #browseBtn.Bind(wx.EVT_BUTTON,self.SelectPath)
        #pathSizer.Add(browseBtn, flag= wx.ALL, border=5)
        settingSizer.Add(pathSizer)

        generationSizer = wx.BoxSizer(wx.HORIZONTAL)
        generationSizer.Add(wx.StaticText(self.settingPanel, label="保存データ世代数"), flag=wx.ALL|wx.EXPAND, border=10)
        for idx, choice in enumerate(generationShowName):   # 創造單選按鈕
            generationRadio = wx.RadioButton(self.settingPanel, label=choice, style=wx.RB_GROUP if idx==0 else 0)   # radiobutton 加上 style = wx.RB_GROUP 表示為一組的開頭
            generationRadio.selfDefinedCustomVal = generationCodeName[idx]      # 額外設定保留自己實際所需數值的變數
            generationRadio.Bind(wx.EVT_RADIOBUTTON, self.GenerationSelect)
            generationSizer.Add(generationRadio,flag=wx.ALL|wx.EXPAND, border=10)
        #generationSizer.Add(wx.RadioButton(self.settingPanel, label="無制限",style = wx.RB_GROUP), flag=wx.ALL|wx.EXPAND, border=10)    # radiobutton 加上 style = wx.RB_GROUP 表示為一組的開頭
        #generationSizer.Add(wx.RadioButton(self.settingPanel, label="10個"),flag=wx.ALL|wx.EXPAND, border=10)
        #generationSizer.Add( wx.RadioButton(self.settingPanel), flag=wx.ALL|wx.EXPAND, border=5)
        generationSizer.Add(self.generationCustonInput, flag=wx.ALL, border=5)
        settingSizer.Add(generationSizer)


        dataSizer = wx.BoxSizer(wx.HORIZONTAL)
        dataSizer.Add(wx.StaticText(self.settingPanel, label="データ同期"), flag=wx.ALL|wx.EXPAND, border=10)
        for idx, sync in enumerate(dataSynchronizes):       # 創造單選按鈕
            syncRadio = wx.RadioButton(self.settingPanel, label=sync, style=wx.RB_GROUP if idx==0 else 0)   # radiobutton 加上 style = wx.RB_GROUP 表示為一組的開頭
            syncRadio.Bind(wx.EVT_RADIOBUTTON, self.SyncSelect)
            dataSizer.Add(syncRadio,flag=wx.ALL|wx.EXPAND, border=10)
        #dataSizer.Add(wx.RadioButton(self.settingPanel, label="ON",style = wx.RB_GROUP),flag=wx.ALL|wx.EXPAND, border=10)
        #dataSizer.Add(wx.RadioButton(self.settingPanel, label="OFF"),flag=wx.ALL|wx.EXPAND, border=10)
        #dataSizer.Add(wx.RadioButton(self.settingPanel, label="OFF APP ONLY"),flag=wx.ALL|wx.EXPAND, border=10)
        settingSizer.Add(dataSizer)

        settingSizer.Add(wx.StaticText(self.settingPanel, label="データファイル種別"), flag=wx.ALL|wx.EXPAND, border=10)

        fileTypeSizer = wx.GridSizer(0,2,0,0)
        for idx, ftype in enumerate(fileTypeShowName):      # 創造單選按鈕
            fileTypeRadio = wx.RadioButton(self.settingPanel, label=ftype, style=wx.RB_GROUP if idx==0 else 0)   # radiobutton 加上 style = wx.RB_GROUP 表示為一組的開頭
            fileTypeRadio.selfDefinedCustomVal = fileTypeCodeName[idx]
            fileTypeRadio.Bind(wx.EVT_RADIOBUTTON, self.FileTypeSelect)
            fileTypeSizer.Add(fileTypeRadio, flag=wx.ALL, border=10 )
        #fileTypeSizer.Add(wx.RadioButton(self.settingPanel, label="CSVのみ",style = wx.RB_GROUP), flag=wx.ALL, border=10)
        #fileTypeSizer.Add(wx.RadioButton(self.settingPanel, label="要約CSV"), flag=wx.ALL, border=10)
        #fileTypeSizer.Add(wx.RadioButton(self.settingPanel, label="CNA"), flag=wx.ALL, border=10)
        #fileTypeSizer.Add(wx.RadioButton(self.settingPanel, label="要約CSV + CNA"), flag=wx.ALL, border=10)
        settingSizer.Add(fileTypeSizer)

        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        rootCheckBtn = wx.Button(self.settingPanel, label="確定")
        rootCheckBtn.Bind(wx.EVT_BUTTON, self.RefreshAppRootFile)
        btnSizer.Add(rootCheckBtn, flag=wx.ALIGN_CENTER|wx.ALL, border=10)
        #btnSizer.Add(wx.Button(self.settingPanel, label="修正"), flag=wx.ALIGN_CENTER|wx.ALL, border=10)
        btnSizer.Add(wx.Button(self.settingPanel, label="消除"), flag=wx.ALIGN_CENTER|wx.ALL, border=10)
        settingSizer.Add(btnSizer)

        # 整合所有頁面到sizer，最下面的實行按鈕==========================================================
        self.basicbSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.basicbSizer)    # 把boxsizer綁到panel上
        self.basicbSizer.Add(switchBtnPanel,proportion=1,flag=wx.ALL|wx.EXPAND,border=5)
        self.basicbSizer.Add(wx.StaticLine(self), flag=wx.GROW)         # 水平線
        self.basicbSizer.Add(self.newUnitPanel,1,flag=wx.ALL,border=5)
        self.basicbSizer.Add(self.timePanel,1,flag=wx.ALL,border=5)
        self.basicbSizer.Add(self.settingPanel,1,flag=wx.ALL,border=5)
        self.basicbSizer.Add(wx.StaticLine(self), flag=wx.GROW)         # 水平線
        #self.basicbSizer.Add(wx.Panel(self,size=(1,20)))
        executionBtn = wx.Button(self, label="実行")
        executionBtn.Bind(wx.EVT_BUTTON, self.Execution)
        self.basicbSizer.Add(executionBtn,flag=wx.ALL|wx.EXPAND)

    # 最上方頁面按鈕功能
    def ChangePage(self, event, idx):
        self.pageIndex = idx
        print("cur index:",self.pageIndex)
        if idx==PAGE.Unit:
            self.newUnitPanel.Show()
            self.timePanel.Hide()
            self.settingPanel.Hide()
            self.Layout()
        elif idx==PAGE.Time:
            self.newUnitPanel.Hide()
            self.timePanel.Show()
            self.settingPanel.Hide()
            self.Layout()
        elif idx==PAGE.Setting:
            self.newUnitPanel.Hide()
            self.timePanel.Hide()
            self.settingPanel.Show()
            self.Layout()

    # 讀取檔案
    def ReadDataFile_Tags(self, filePath)->list:
        data = []
        with open(filePath,"r+") as f:
            for line in f.readlines():
                data.append(line.split("\n")[0])
        #f = open(filePath,"r+")
        #for line in f.readlines():
        #    data.append(line.split("\n")[0])
        #print("data:",data)
        #f.close()
        return data
    
    # 選取紀錄過的機器單元
    def SelectUnit(self, event):
        #obj = event.GetEventObject()    #找不到其他寫法
        #self.selectUnitStr = obj.GetStringSelection()
        
        print(self.existUnitListBox.GetStringSelection())
    # 新規單元頁面按鈕
    def CheckUnit(self, event):
        print("test")
        newName = str(self.newUnitName.Value).strip()
        newSSID = str(self.newUnitSSID.Value).strip()
        if len(newName) !=0 and len(newSSID) != 0:
            newUnitStr = newName+", "+newSSID
            self.existUnitList.append(newUnitStr)           # 加到實際資料
            self.existUnitListBox.Append(newUnitStr)        # 加到GUI畫面上
            self.RefreshTagsFile()
            self.newUnitName.Value = ""     # 清掉畫面上的輸入
            self.newUnitSSID.Value = ""
        print(newName)
        print(newSSID)

    def DeleteUnit(self, event):
        delitem = self.existUnitListBox.GetSelection()
        self.existUnitListBox.Delete(delitem)
        self.existUnitList.pop(delitem)
        self.RefreshTagsFile()
        
    def RefreshTagsFile(self):
        with open(self.tagsConfPath,"w") as f:
            for unit in self.existUnitList:
                f.write(unit+"\n")
        wx.MessageBox("tags.conf データ修正完了しました \n " + self.tagsConfPath)


    # 設定頁面按鈕
    def SelectPath(self, event):
        openFileDialog = wx.DirDialog(self)
        openFileDialog.ShowModal()      # 跳出選路徑視窗
        tmp = openFileDialog.GetPath()  # 回傳所選路徑
        if tmp != "":
            self.appRootPath.Value = tmp
        openFileDialog.Destroy()
    def GenerationSelect(self, event):
        self.DATA_GEN = event.GetEventObject().selfDefinedCustomVal # chatgpt提供的做法，針對物件額外自訂取用值
        #print(self.DATA_GEN)
    def SyncSelect(self, event):
        self.DATA_SYNC = event.GetEventObject().GetLabel()
        #print(self.DATA_SYNC)
    def FileTypeSelect(self, event):
        self.FILE_TYPE = str(event.GetEventObject().selfDefinedCustomVal)
        #print(self.FILE_TYPE)
    def RefreshAppRootFile(self, event):

        genWriteToFile = 0
        if self.DATA_GEN == GENERATION_VALUE.customInputMode:
            genWriteToFile = str(self.generationCustonInput.Value)
            if not genWriteToFile.isnumeric():  # 判斷是否為數字，不是就強制轉成無制限的 0
                wx.MessageBox("入力された数字は正しくありません。もう一度ご確認ください")
                genWriteToFile = 0
            genWriteToFile = str(genWriteToFile).lstrip("0")    # 清除最高位數連續 0
            if len(genWriteToFile) == 0: genWriteToFile = 0     # 回補預設值
            self.generationCustonInput.Value = str(genWriteToFile)  # 顯示回畫面
        else:
            genWriteToFile = self.DATA_GEN

        with open(self.appRootConfPath,"w") as f:
            f.write("APP_ROOT, " + self.appRootPath.GetValue() + "\n")
            f.write("DATA_GEN, " + str(genWriteToFile) + "\n")
            f.write("DATA_SYNC, " + self.DATA_SYNC + "\n")
            f.write("FILE_TYPE, " + self.FILE_TYPE + "\n")
            f.write("SCHED30, DISABLE")
            wx.MessageBox("app_root.conf データ修正完了しました \n " + self.appRootConfPath)
        
    # 實行按鈕功能
    def Execution(self,event):
        #os.popen("ls")
        os.popen(self.applicationExePath)
        pass
    
if __name__ == '__main__':
    app = wx.App()
    frm = MainFrame(None)
    frm.Show()
    app.MainLoop()
