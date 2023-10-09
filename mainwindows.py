import pyautogui
import tkinter as tk
from tkinter import ttk
import ezOCR
import googletranslator
import resultwindows
import selectwindowsEx
import customdictwindows
from PIL import ImageTk
import time
import threading
# mainwindows. 현재 main.py에 있는 여러 스레드들을 여기서 관장해야할듯. 
# 얘가 selectwindowsEx, resultwindows도 켜고 끌 수 있어야 하고...
# 기존 설정도 저장되도록 하면 좋을 것 같음 <- 이건 추후 천천히 개발해보도록
class mainwindows:
    def __init__(self):
        self.text_extractor = ezOCR.TextExtractionApp()
        self.translator = googletranslator.googletranslator()
        self.trans_from, self.trans_to = self.translator.src, self.translator.dest
        self.resultwindow = None
        self.selectwindow = None
        self.transsettingwindow = None
        self.customdictwindow = None
        
        # variables for loop
        self.x, self.y, self.width, self.height = None, None, None, None
        self.selectthread = None
        self.selectthreadcheck = False
        self.resultthread = None
        self.mainthread = None
        self.before_text = ""
        self.automode = True
        
        self.trans_from, self.trans_to = self.translator.src, self.translator.dest
        self.sleeptime = 0.3
        
        #------------ mainwindow UI --------------#
        self.pad_x = 15
        self.pad_y = 30
        
        self.root = tk.Tk()
        self.root.title("Main window")
        self.root.geometry("200x130+50+50")
        #icon = ImageTk.PhotoImage(file="icon\\icon1.jpg")
        #self.root.iconphoto(False, icon)
        
        
        #----------- LanguageSelect(ResultWindow Setting) -----------#
        self.menu = tk.Listbox(self.root, height=0, selectmode="browse", activestyle="none", font="TkDefaultFont 14")
        self.menu.insert(0, "Open Selectbox")
        self.menu.insert(1, "Open ResultWindow")
        self.menu.insert(2, "Open Translate Setting")
        self.menu.insert(3, "Open CustomDict")
        self.menu.pack(padx=(self.pad_x,self.pad_x), pady=(self.pad_x, self.pad_x))
        
        
        def on_double_click(event):
            selected_index = self.menu.curselection()
            
            if selected_index:
                selected_index = int(selected_index[0])
                
                index_to_func = {
                    0:self.selectThreadOn,
                    1:self.resultThreadOn,
                    2:self.openTranslateSetting,
                    3:self.openCustomDict
                }
                
                if selected_index in index_to_func:
                    index_to_func[selected_index]()
        
        self.menu.bind("<Double-Button-1>", on_double_click)
    
    def selectThreadOn(self):
        self.selectthread = threading.Thread(target=self.selectWindowThread)
        self.selectthread.start()
    
    def selectWindowThread(self):
        if self.selectwindow is None:
            self.selectwindow = selectwindowsEx.ResizableWindow()
        else:
            try:
                self.selectwindow.__del__()
            except:
                pass
            finally:
                self.selectwindow = selectwindowsEx.ResizableWindow()
        while True:
            if self.selectwindow.isStopped:
                break
            self.x, self.y, self.width, self.height = self.selectwindow.get_window_position_and_size()
            self.selectwindow.start()
            time.sleep(self.sleeptime)
    
    def resultThreadOn(self):
        self.resultthread = threading.Thread(target=self.openResultWindow)
        self.resultthread.start()
        
    def openResultWindow(self):
        if self.resultwindow is None:
            self.resultwindow = resultwindows.resultwindows()
            self.mainthread = threading.Thread(target=self.mainThread)
            self.mainthread.start()
            self.resultwindow.start()
        else:
            try:
                self.resultwindow.__del__()
            except:
                pass
            finally:
                self.resultwindow = resultwindows.resultwindows()
                self.mainthread = threading.Thread(target=self.mainThread)
                self.mainthread.start()
                self.resultwindow.start()
    
    def openTranslateSetting(self):
        # 구현예정
        try:
            if self.transsettingwindow:
                self.transsettingwindow.destroy()
        except:
            pass
        self.transsettingwindow = tk.Tk()
        self.transsettingwindow.title("TranslateSetting")
        
        textmodeLabel = tk.Label(self.transsettingwindow, text="Translate mode Select")
        textmodeLabel.grid(row=1, column=0, columnspan=2)
        
        def mode_change():
            if textmode.get() == 0:
                self.automode = True
            else:
                self.automode = False
                
        
        textmode = tk.StringVar()
        
        automode = ttk.Radiobutton(self.transsettingwindow, text="Auto", variable=textmode, value="Auto", command=mode_change)
        clickmode = ttk.Radiobutton(self.transsettingwindow, text="Click", variable=textmode, value="Click", command=mode_change)
        
        automode.grid(row=2, column=0)
        clickmode.grid(row=2, column=1)
        
        self.transsettingwindow.mainloop()
    
    def openCustomDict(self):
        try:
            if self.customdictwindow:
                self.customdictwindow.destroy()
        except:
            pass
        self.customdictwindow = customdictwindows.customwindows()
        self.customdictwindow.root.mainloop()

    
    def mainThread(self):
        while True:
            if self.resultwindow.isStopped:
                break
            try:
                screenshot = pyautogui.screenshot(region=(self.x, self.y, self.width, self.height))
            except:
                break
            screenshot.save("captureimg/window_capture.png")

            if (self.trans_from, self.trans_to) != self.resultwindow.return_combobox():
                self.trans_from, self.trans_to = self.resultwindow.return_combobox()
                self.translator.setLanguage(self.trans_from, self.trans_to)
                self.text_extractor.setLanguage(self.trans_from)
                self.before_text = ""
    
    
    
            # Call the extract_text_from_image method to extract text from the saved image
            origin_text = self.text_extractor.extract_text_from_image()
            if origin_text == []:
                origin_text = [""]
            if len(origin_text[0])<10:
                if len(origin_text) > 1:
                    origin_text = origin_text[0]+"\n"+" ".join(origin_text[1:])
                else:
                    origin_text = origin_text[0]
            else:
                origin_text = " ".join(origin_text)

            # Display the extracted text in the Tkinter window
            if self.before_text != origin_text:
                self.before_text = origin_text
                self.resultwindow.input_origin(origin_text)

                trans_text = self.translator.translate(origin_text)
                self.resultwindow.input_trans(trans_text)
            # Adjust the sleep time to control the capture frequency
            time.sleep(self.sleeptime)
    
    def start(self):
        self.root.mainloop()
        
if __name__ == "__main__":
    window = mainwindows()
    
    window.start()