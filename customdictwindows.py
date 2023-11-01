import tkinter as tk
import tkinter.messagebox
from tkinter import ttk
import CustomDict

class customwindows:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("CustomDict")
        self.root.geometry("600x400")
        self.filename = "CustomDict/CustomDict.txt"
        f = open(self.filename, "r", encoding = "UTF-8")
        
        # CustomDict.txt 내용 불러옴
        self.c_dict = {}
        while True:
            line = f.readline()
            if not line:
                break
            if line == "": # 빈 라인 제외
                continue
            if line[:2] == "//": # 주석부분은 제외
                continue
            origin, trans, type = line.split('\t')
            print(origin, trans, type)
            self.c_dict[origin] = (trans, type[:-1])
        
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
        
        tagtext = tk.Label(addwordframe, text="유형 : ")
        tagtext.grid(row=0, column=4, padx=(0, 5), pady=(10, 10))
        values = ['의미 표기', '원음 표기']
        self.taginput = ttk.Combobox(addwordframe, height=3, width=4, values=values)
        self.taginput.grid(row=0, column=5, padx=(0, 5), pady=(10, 10))
        self.taginput.set('선택')
        
        def addfunction():
            tmpdict = CustomDict.CustomDict()
            o_input, t_input = self.origininput.get("1.0", tk.END)[:-1], self.transinput.get("1.0", tk.END)[:-1]
            type_input = self.taginput.get()
            if type_input == '선택' or o_input=='' or t_input=='':
                tkinter.messagebox.showwarning(title="입력 에러", message="모든 항목을 정확히 입력해 주세요")
                return
            try:
                self.dicttable.insert("", "end", text="", values=(o_input, t_input, type_input), iid = o_input)
            except:
                tkinter.messagebox.showwarning(title="입력 에러", message="해당 원문은 이미 존재합니다.")
                return
            tmpdict.appendDict(o_input, t_input, type_input)
        
        self.addbutton = tk.Button(addwordframe, text="추가", command=addfunction)
        self.addbutton.grid(row=0, column=6, padx=(0, 5), pady=(10, 10))
        
        def changefunction():
            try:
                curItem = self.dicttable.focus()
            except:
                return
            o_input, t_input, type_input = self.dicttable.item(curItem)['values']
            co_input, ct_input = self.origininput.get("1.0", tk.END)[:-1], self.transinput.get("1.0", tk.END)[:-1]
            ctype_input = self.taginput.get()
            tmpDict = CustomDict.CustomDict()
            tmpDict.changeDict(o_input, t_input, type_input, co_input, ct_input, ctype_input)
            self.dicttable.item(curItem, text="", values=(co_input, ct_input, ctype_input))
        
        self.changebutton = tk.Button(addwordframe, text="변경", command=changefunction)
        self.changebutton.grid(row=0, column=7, padx=(0, 5), pady=(10, 10))
        
        def deletefunction():
            try:
                curItem = self.dicttable.focus()
            except:
                return
            o_input, t_input, type_input = self.dicttable.item(curItem)['values']
            tmpDict = CustomDict.CustomDict()
            tmpDict.removeDict(o_input, t_input, type_input)
            selected_item = self.dicttable.selection()[0] ## get selected item
            self.dicttable.delete(selected_item)
            self.origininput.delete("1.0", "end")
            self.transinput.delete("1.0", "end")
        
        self.deletebutton = tk.Button(addwordframe, text="삭제", command=deletefunction)
        self.deletebutton.grid(row=0, column=8, padx=(0, 5), pady=(10, 10))
        
        def dicttableclick(event):
            item = self.dicttable.identify('item', event.x, event.y)
            try:
                o_input, t_input, type_input = self.dicttable.set(item).values()
            except:
                return
            self.origininput.delete("1.0", "end")
            self.origininput.insert("1.0", o_input)
            self.transinput.delete("1.0","end")
            self.transinput.insert("1.0", t_input)
            self.taginput.set(type_input)
        
        # 원문 - 번역문 테이블 생성
        self.dicttable = ttk.Treeview(self.root, columns=["Origin Text", "Translated Text", "Type"], displaycolumns=["Origin Text", "Translated Text", "Type"])
        self.dicttable.bind("<Button-1>", dicttableclick)
        self.dicttable.pack()
        
        self.dicttable.column("Origin Text", width="192", anchor="center")
        self.dicttable.heading("Origin Text", text="Origin Text")
        
        self.dicttable.column("Translated Text", width="192", anchor="center")
        self.dicttable.heading("Translated Text", text="Translated Text")
        
        self.dicttable.column("Type", width="100", anchor="center")
        self.dicttable.heading("Type", text="Type")
        
        self.dicttable["show"] = "headings"
        
        for origin, (trans, type) in self.c_dict.items():
            try:
                self.dicttable.insert("", "end", text="", values=(origin, trans, type), iid = origin)
            except:
                pass
    
    def destroy(self):
        self.root.destroy()
        self.root = None

if __name__ == "__main__":
    c = customwindows()
    c.root.mainloop()