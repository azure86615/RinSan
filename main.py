import wx
import os

class PAGE():
    Unit = 0
    Time = 1
    Setting = 2

class GENERATION_VALUE():
    customInputMode = -1

class MyFrame(wx.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.SetSize((400, 450))        #視窗大小
        self.SetTitle('Simple menu')    #視窗標題
        self.Centre()   # 把產生出來的視窗放在螢幕正中間
        self.pageIndex = PAGE.Unit      #指示當前所在的頁面
        self.tagsConfPath = ".\\test.conf"
        self.schedulConfPath = ".\\schedule.conf"
        self.appRootConfPath = ".\\app_root.conf"
        self.applicationExePath = "%windir%\system32\SnippingTool.exe"
        self.existUnitList = self.ReadDataFile_Tags(self.tagsConfPath)
        self.periodModeIndex = 0
        self.ReadDataFile_Schedule(self.schedulConfPath)
        self.showPanelColor = True     # 控制 panel 上色(辨識區域用)
        

        # 創建主頁面面板及布局
        self.panel_main = wx.Panel(self)    # 其他元件放在此 panel 之上。一直到最後才把這層放到 self 的 sizer 裡面
        # 規則是 frame 下面第一個一定要放 sizer，雖然可以在 frame 的 sizer 上直接構圖，但是莫名會造成視窗左上角破圖，因此蓋一層 panel 比較穩
        # 而 timePanel 那頁如果也塞在這裡面莫名又會造成顯示出錯(一開始沒顯示出文字，換頁按回來就有)，所以才搞成這麼麻煩的架構
        basicbSizer = wx.BoxSizer(wx.VERTICAL)
        self.panel_main.SetSizer(basicbSizer)
        self.panel_main.SetBackgroundColour(wx.BLUE) if self.showPanelColor else False

        # 創建三個子頁面面板
        self.newUnitPanel = wx.Panel(self)
        self.newUnitPanel.SetBackgroundColour(wx.RED) if self.showPanelColor else False
        #self.newUnitPanel.Hide()
        self.timePanel = wx.Panel(self)
        self.timePanel.SetBackgroundColour(wx.GREEN) if self.showPanelColor else False
        self.timePanel.Hide()
        self.settingPanel = wx.Panel(self)
        self.settingPanel.SetBackgroundColour(wx.YELLOW) if self.showPanelColor else False
        self.settingPanel.Hide()

        # 頁面按鈕區域==========================================================
        switchBtnPanel = wx.Panel(self.panel_main)
        switchBtnSizer = wx.BoxSizer(wx.HORIZONTAL)
        switchBtnPanel.SetSizer(switchBtnSizer)

        button_newUnit = wx.Button(switchBtnPanel, label="新規追加")
        button_time = wx.Button(switchBtnPanel, label="スケジュール")
        button_setting = wx.Button(switchBtnPanel, label="パラメータ設定")
        button_newUnit.Bind(wx.EVT_BUTTON, lambda event, idx=PAGE.Unit: self.ChangePage(event, idx))
        button_time.Bind(wx.EVT_BUTTON,lambda event, idx=PAGE.Time: self.ChangePage(event, idx))
        button_setting.Bind(wx.EVT_BUTTON, lambda event, idx=PAGE.Setting: self.ChangePage(event, idx))
        switchBtnSizer.Add(button_newUnit, 0,border=20)
        switchBtnSizer.Add(button_time, 0,border=20)
        switchBtnSizer.Add(button_setting, 0,border=20)

        basicbSizer.Add(switchBtnPanel)
        self.panel_main.Fit()
        # 新規追加 頁面==========================================================
        # 參數
        self.newUnitName = wx.TextCtrl(self.newUnitPanel)
        self.newUnitSSID = wx.TextCtrl(self.newUnitPanel)
        self.existUnitListBox = wx.ListBox(self.newUnitPanel, choices = self.existUnitList, size=(200,300))
        #self.existUnitListBox.Bind(wx.EVT_LISTBOX,self.SelectUnit)
        unitCheckBtn = wx.Button(self.newUnitPanel, label="確定")
        unitCheckBtn.Bind(wx.EVT_BUTTON, self.CheckUnit)
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
        scheduleSelectionList = ["月","周","日","30分","5分"]
        self.monthCase = {}

        self.timeCase = {}
        testscheduleList = ["test1, daily, 00:00,+00:30*?, , , , , , , ,","test, monthly, Mon1 09:30, Mon2 09:30, Mon3 09:30, Mon4 09:30, , , , , ,"]
        

        hourList = ["","00","01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23"]
        minuteList = ["00","30"]
        self.scheduleOptionDic = {}
        self.scheduleHourDic = {}
        self.scheduleMinDic = {}
        
        
        # 布局
        timebSizer = wx.BoxSizer(wx.VERTICAL)
        self.timePanel.SetSizer(timebSizer)

        selectionPart = wx.BoxSizer(wx.HORIZONTAL)
        for idx, choice in enumerate(scheduleSelectionList):   # 創造週期單選按鈕
            schSelRadio = wx.RadioButton(self.timePanel, label=choice, style=wx.RB_GROUP if idx==0 else 0)   # radiobutton 加上 style = wx.RB_GROUP 表示為一組的開頭
            if self.periodModeIndex == idx: schSelRadio.SetValue(True)  # 控制模式按鈕預設
            schSelRadio.Bind(wx.EVT_RADIOBUTTON, lambda event, scheduleTypeIndex=idx: self.SelectPeriod(event, scheduleTypeIndex))
            selectionPart.Add(schSelRadio,flag=wx.ALL|wx.EXPAND, border=10)
        timebSizer.Add(selectionPart)

        timeSettingPart = wx.BoxSizer(wx.HORIZONTAL)
        self.scheduleOptionPanel = wx.Panel(self.timePanel)
        self.scheduleOptionPanel.SetBackgroundColour(wx.YELLOW) if self.showPanelColor else False
        #self.monthPanel.Hide()
        self.dayList = ["","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31"]
        self.weekList = ["","Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
        self.optionModeComboboxList: list[wx.ComboBox] = []
        self.optionModeTextList: list[wx.StaticText] = []

        optionPart = wx.BoxSizer(wx.VERTICAL)
        self.scheduleOptionPanel.SetSizer(optionPart)
        for index in range(4):
            optionPartElement = wx.BoxSizer(wx.HORIZONTAL)
            optionCombobox = wx.ComboBox(self.scheduleOptionPanel, choices=self.dayList, style=wx.CB_READONLY)
            optionCombobox.Bind(wx.EVT_COMBOBOX, lambda event, index=index: self.SelectOptionDate_1(event, index))
            self.optionModeComboboxList.append(optionCombobox)
            optionPartElement.Add(optionCombobox, flag=wx.ALL, border=5)
            modetext = wx.StaticText(self.scheduleOptionPanel, label="日")
            optionPartElement.Add(modetext, flag=wx.ALL, border=10)
            self.optionModeTextList.append(modetext)
            
            optionPart.Add(optionPartElement)
        
        timeSettingPart.Add(self.scheduleOptionPanel)


        hourMinutePart = wx.BoxSizer(wx.VERTICAL)
        for timerIndex in range(4):
            timePart = wx.BoxSizer(wx.HORIZONTAL)
            time1_hour = wx.ComboBox(self.timePanel, choices=hourList, style=wx.CB_READONLY)    #只允許用選的 (避免出錯用)
            time1_minute = wx.ComboBox(self.timePanel, choices=minuteList, style=wx.CB_READONLY)
            time1_hour.Bind(wx.EVT_COMBOBOX, lambda event, idx=timerIndex: self.SelectHour_1(event, idx))
            time1_minute.Bind(wx.EVT_COMBOBOX, lambda event, idx=timerIndex: self.SelectMinute_1(event, idx))
            timePart.Add(time1_hour, flag=wx.ALL, border=5)
            timePart.Add(wx.StaticText(self.timePanel, label="時"), flag=wx.ALL, border=10)
            timePart.Add(time1_minute, flag=wx.ALL, border=5)
            timePart.Add(wx.StaticText(self.timePanel, label="分"), flag=wx.ALL, border=10)
            hourMinutePart.Add(timePart)

        timeSettingPart.Add(hourMinutePart)
        timebSizer.Add(timeSettingPart)


        scheduleCheckBtn = wx.Button(self.timePanel, label="確定")
        scheduleCheckBtn.Bind(wx.EVT_BUTTON, self.CheckSchedule)
        timebSizer.Add(scheduleCheckBtn, flag=wx.ALIGN_CENTER|wx.ALL, border=10)

        self.SelectPeriod(any, self.periodModeIndex)    # 控制預設時間區間模式的頁面項目 (不包含模式按鈕)


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

        settingSizer.Add(pathSizer)

        generationSizer = wx.BoxSizer(wx.HORIZONTAL)
        generationSizer.Add(wx.StaticText(self.settingPanel, label="保存データ世代数"), flag=wx.ALL|wx.EXPAND, border=10)
        for idx, choice in enumerate(generationShowName):   # 創造單選按鈕
            schSelRadio = wx.RadioButton(self.settingPanel, label=choice, style=wx.RB_GROUP if idx==0 else 0)   # radiobutton 加上 style = wx.RB_GROUP 表示為一組的開頭
            schSelRadio.selfDefinedCustomVal = generationCodeName[idx]      # 額外設定保留自己實際所需數值的變數
            schSelRadio.Bind(wx.EVT_RADIOBUTTON, self.GenerationSelect)
            generationSizer.Add(schSelRadio,flag=wx.ALL|wx.EXPAND, border=10)
        generationSizer.Add(self.generationCustonInput, flag=wx.ALL, border=5)
        settingSizer.Add(generationSizer)


        dataSizer = wx.BoxSizer(wx.HORIZONTAL)
        dataSizer.Add(wx.StaticText(self.settingPanel, label="データ同期"), flag=wx.ALL|wx.EXPAND, border=10)
        for idx, sync in enumerate(dataSynchronizes):       # 創造單選按鈕
            syncRadio = wx.RadioButton(self.settingPanel, label=sync, style=wx.RB_GROUP if idx==0 else 0)   # radiobutton 加上 style = wx.RB_GROUP 表示為一組的開頭
            syncRadio.Bind(wx.EVT_RADIOBUTTON, self.SyncSelect)
            dataSizer.Add(syncRadio,flag=wx.ALL|wx.EXPAND, border=10)
        settingSizer.Add(dataSizer)

        settingSizer.Add(wx.StaticText(self.settingPanel, label="データファイル種別"), flag=wx.ALL|wx.EXPAND, border=10)

        fileTypeSizer = wx.GridSizer(0,2,0,0)
        for idx, ftype in enumerate(fileTypeShowName):      # 創造單選按鈕
            fileTypeRadio = wx.RadioButton(self.settingPanel, label=ftype, style=wx.RB_GROUP if idx==0 else 0)   # radiobutton 加上 style = wx.RB_GROUP 表示為一組的開頭
            fileTypeRadio.selfDefinedCustomVal = fileTypeCodeName[idx]
            fileTypeRadio.Bind(wx.EVT_RADIOBUTTON, self.FileTypeSelect)
            fileTypeSizer.Add(fileTypeRadio, flag=wx.ALL, border=10 )
        settingSizer.Add(fileTypeSizer)

        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        rootCheckBtn = wx.Button(self.settingPanel, label="確定")
        rootCheckBtn.Bind(wx.EVT_BUTTON, self.RefreshAppRootFile)
        btnSizer.Add(rootCheckBtn, flag=wx.ALIGN_CENTER|wx.ALL, border=10)
        #btnSizer.Add(wx.Button(self.settingPanel, label="修正"), flag=wx.ALIGN_CENTER|wx.ALL, border=10)
        btnSizer.Add(wx.Button(self.settingPanel, label="消除"), flag=wx.ALIGN_CENTER|wx.ALL, border=10)
        settingSizer.Add(btnSizer)


        # 將四個面板添加到主窗口===================================================================
        #basicbSizer.Add(self.newUnitPanel, 1, wx.EXPAND)
        #basicbSizer.Add(self.timePanel, 1, wx.EXPAND)
        #basicbSizer.Add(self.settingPanel, 1, wx.EXPAND)
        frameSizer = wx.BoxSizer(wx.VERTICAL)
        frameSizer.Add(self.panel_main, 1, wx.EXPAND)
        frameSizer.Add(wx.StaticLine(self), flag=wx.GROW)         # 水平線
        frameSizer.Add(self.newUnitPanel, 1, wx.EXPAND)
        frameSizer.Add(self.timePanel, 1, wx.EXPAND)
        frameSizer.Add(self.settingPanel, 1, wx.EXPAND)
        frameSizer.Add(wx.StaticLine(self), flag=wx.GROW)         # 水平線
        executionBtn = wx.Button(self, label="実行")
        executionBtn.Bind(wx.EVT_BUTTON, self.Execution)
        frameSizer.Add(executionBtn,flag=wx.ALL|wx.EXPAND)
        self.SetSizer(frameSizer)

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
        return data

    def ReadDataFile_Schedule(self, filePath):
        existContent = ""
        with open(filePath,"r+") as f:
            existContent = f.readline()
        modeTextTailIndex = existContent.find(",",3)
        modeText = existContent[3:modeTextTailIndex]
        if modeText == "monthly":
            self.periodModeIndex = 0
        elif modeText == "weekly":
            self.periodModeIndex = 1
        
        print("text:",modeText)
    
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
    
    # 時間表頁面按鈕
    def SelectPeriod(self, event, schIndex):
        #print(event.GetEventObject())
        print(schIndex)

        if self.periodModeIndex != schIndex:
            self.scheduleOptionDic.clear()
        
        self.periodModeIndex = schIndex
        if schIndex == 0:
            self.scheduleOptionPanel.Show()
            for modetext in self.optionModeTextList:
                modetext.SetLabel("日")
            for modeCombobox in self.optionModeComboboxList:
                modeCombobox.SetItems(self.dayList)
            self.Layout()   # 調整排版
        elif schIndex == 1:
            self.scheduleOptionPanel.Show()
            for modetext in self.optionModeTextList:
                modetext.SetLabel("曜日")
            for modeCombobox in self.optionModeComboboxList:
                modeCombobox.SetItems(self.weekList)
            self.Layout()   # 調整排版
        else:
            self.scheduleOptionPanel.Hide()
            self.Layout()   # 調整排版

    def SetTime(self, event, timeGroupNum):
        print()
    
    def CheckSchedule(self, event):
        print("option:",self.scheduleOptionDic, " hour:",self.scheduleHourDic, " min:",self.scheduleMinDic)
        print("mode:",self.periodModeIndex)
        writeToFile = ""
        modeText = ""
        if self.periodModeIndex == 0:
            modeText = "monthly"
        elif self.periodModeIndex == 1:
            modeText = "weekly"
        else:
            modeText = "daily"

        
        if self.periodModeIndex <=1:
            for idx in range(4):
                if idx not in self.scheduleOptionDic.keys() or idx not in self.scheduleHourDic.keys() or  idx not in self.scheduleMinDic.keys():
                    continue
                else:
                    writeToFile += " " + self.scheduleOptionDic[idx] + " " + self.scheduleHourDic[idx] + ":" + self.scheduleMinDic[idx] + "," #開頭空白，結尾逗號
        else:
            for idx in range(4):
                if idx not in self.scheduleHourDic.keys() or  idx not in self.scheduleMinDic.keys():
                    continue
                else:
                    writeToFile += " " + self.scheduleHourDic[idx] + ":" + self.scheduleMinDic[idx] + "," #開頭空白，結尾逗號

        with open(self.schedulConfPath,"w") as f:
            if writeToFile != "":
                writeToFile = "*, " + modeText + "," + writeToFile + ",,,,,,,"
                f.write(writeToFile)
            wx.MessageBox("schedule.conf データ修正完了しました \n " + self.schedulConfPath)
        
        print(writeToFile)

    
    def SelectOptionDate_1(self,event, idx):
        print("Day: " + event.GetEventObject().GetValue(), "idx: ",idx)
        self.scheduleOptionDic[idx] = event.GetEventObject().GetValue()
        if self.scheduleOptionDic[idx] == "":
            self.scheduleOptionDic.pop(idx)
    def SelectHour_1(self, event, idx):
        print("hour: " + event.GetEventObject().GetValue(),"idx: ",idx)
        self.scheduleHourDic[idx] = event.GetEventObject().GetValue()
    def SelectMinute_1(self, event, idx):
        print("Minute: " + event.GetEventObject().GetValue(),"idx: ",idx)
        self.scheduleMinDic[idx] = event.GetEventObject().GetValue()

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
        #os.popen(self.applicationExePath)
        self.ReadDataFile_Schedule(self.schedulConfPath)
        pass

if __name__ == '__main__':
    # Create a wx application
    app = wx.App()
    # Create the demo window
    win = MyFrame(None)
    # Show the window
    win.Show()
    # Start wx main loop
    app.MainLoop()