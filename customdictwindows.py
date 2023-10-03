import tkinter as tk
from tkinter import ttk
import CustomDict

class customwindows:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("CustomDict")
        self.root.geometry("500x400")
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
        
        f.close()
        
        tableLabel = tk.Label(self.root, text="CustomDict")
        tableLabel.pack(pady=(10, 10))
        
        addwordframe = tk.LabelFrame(self.root, text="단어 추가/변경")
        addwordframe.pack(pady=(0,10))
        
        origintext = tk.Label(addwordframe, text="원문 :")
        origintext.grid(row=0, column=0, padx=(5, 5), pady=(10, 10))
        self.origininput = tk.Text(addwordframe, width=10, height=1)
        self.origininput.grid(row=0, column=1, padx=(0, 5), pady=(10, 10))
        
        transtext = tk.Label(addwordframe, text="번역문 :")
        transtext.grid(row=0, column=2, padx=(0, 5), pady=(10, 10))
        self.transinput = tk.Text(addwordframe, width=10, height=1)
        self.transinput.grid(row=0, column=3, padx=(0, 5), pady=(10, 10))
        
        def addfunction():
            tmpdict = CustomDict.CustomDict()
            o_input, t_input = self.origininput.get("1.0", tk.END)[:-1], self.transinput.get("1.0", tk.END)[:-1]
            tmpdict.appendDict(o_input, t_input)
            self.dicttable.insert("", "end", text="", values=(o_input, t_input), iid = o_input)
        
        self.addbutton = tk.Button(addwordframe, text="추가", command=addfunction)
        self.addbutton.grid(row=0, column=4, padx=(0, 5), pady=(10, 10))
        
        def changefunction():
            pass
        
        self.changebutton = tk.Button(addwordframe, text="변경")
        self.changebutton.grid(row=0, column=5, padx=(0, 5), pady=(10, 10))
        
        def deletefunction():
            pass
        
        self.deletebutton = tk.Button(addwordframe, text="삭제")
        self.deletebutton.grid(row=0, column=6, padx=(0, 5), pady=(10, 10))
        
        # 원문 - 번역문 테이블 생성
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