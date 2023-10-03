import tkinter as tk
from tkinter import ttk

class customwindows:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("CustomDict")
        self.root.geometry("500x300")
        self.filename = "CustomDict/CustomDict.txt"
        f = open(self.filename, "r", encoding = "UTF-8")
        
        # CustomDict.txt 내용 불러옴
        self.c_dict = {}
        while True:
            line = f.readline()
            if not line:
                break
            if line[:2] == "//": # 주석부분은 제외
                continue
            origin, trans = line.split('\t')
            print(origin, trans[:-1])
            self.c_dict[origin] = trans[:-1]
        
        
        
        # 원문 - 번역문 테이블 생성
        tableLabel = tk.Label(self.root, text="CustomDict")
        tableLabel.pack(pady=(10, 10))
        
        self.dicttable = ttk.Treeview(self.root, columns=["Origin Text", "Translated Text"], displaycolumns=["Origin Text", "Translated Text"])
        self.dicttable.pack()
        
        self.dicttable.column("Origin Text", width="200", anchor="center")
        self.dicttable.heading("Origin Text", text="Origin Text")
        
        self.dicttable.column("Translated Text", width="200", anchor="center")
        self.dicttable.heading("Translated Text", text="Translated Text")
        
        self.dicttable["show"] = "headings"
        
        for origin, trans in self.c_dict.items():
            self.dicttable.insert("", "end", text="", values=(origin, trans), iid = origin)
        

if __name__ == "__main__":
    c = customwindows()
    c.root.mainloop()