import tkinter as tk
from tkinter import ttk
import ezOCR
import googletranslator
import resultwindows
import selectwindowsEx
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
        self.resultwindow = None
        self.selectwindow = None
        
        
        # variables for loop
        self.x, self.y, self.width, self.height = None, None, None, None
        self.selectthread = None
        self.selectthreadcheck = False
        self.befor_text = ""
        
        self.trans_from, self.trans_to = self.translator.src, self.translator.dest
        self.sleeptime = 0.3
        
        #------------ mainwindow UI --------------#
        self.pad_x = 15
        self.pad_y = 30
        
        self.root = tk.Tk()
        self.root.title("Main window")
        self.root.geometry("200x100+50+50")
        #icon = ImageTk.PhotoImage(file="icon\\icon1.jpg")
        #self.root.iconphoto(False, icon)
        
        
        #----------- LanguageSelect(ResultWindow Setting) -----------#
        self.menu = tk.Listbox(self.root, height=0, selectmode="browse", activestyle="none", font="TkDefaultFont 14")
        self.menu.insert(0, "Open Selectbox")
        self.menu.insert(1, "Open ResultWindow")
        self.menu.insert(2, "Open Translate Setting")
        self.menu.pack(padx=(self.pad_x,self.pad_x), pady=(self.pad_x, self.pad_x))
        
        
        def on_double_click(event):
            selected_index = self.menu.curselection()
            
            if selected_index:
                selected_index = int(selected_index[0])
                
                index_to_func = {
                    0:self.selectThreadOn,
                    1:self.openResultWindow
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
    
    def openResultWindow(self):
        if self.resultwindow is None:
            self.resultwindow = resultwindows.resultwindows()
        else:
            try:
                self.resultwindow.__del__()
            except:
                pass
            finally:
                self.resultwindow = resultwindows.resultwindows()
    
    def openTranslateSetting(self):
        # 구현예정
        pass
    
    def start(self):
        self.root.mainloop()
        
if __name__ == "__main__":
    window = mainwindows()
    
    window.start()