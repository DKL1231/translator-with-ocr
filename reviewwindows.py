import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

class reviewwindows:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Review Note")
        self.root.geometry("600x400")
        self.filename = "study/reviewnote.txt"
        f = open(self.filename, "r", encoding = "UTF-8")
        self.reviewnote = []
        
        while True:
            line = f.readline()
            if not line:
                break
            if line == "":
                continue
            if line[:2] == "//":
                continue
            origin, trans, score, correct, total = line.split('\t')
            print(origin, trans, score, correct, total)
            self.reviewnote.append([score, origin, trans, correct, total[:-1]])
        
        f.close
        
        tableLabel = tk.Label(self.root, text="ReviewNote")
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
            o_input, t_input = self.origininput.get("1.0", tk.END)[:-1], self.transinput.get("1.0", tk.END)[:-1]
            if o_input=='' or t_input=='':
                tk.messagebox.showwarning(title="입력 에러", message="모든 항목을 정확히 입력해 주세요")
                return
            try:
                self.reviewtable.insert("", "end", text="", values=(o_input, t_input, 0, 0), iid = o_input)
            except:
                tk.messagebox.showwarning(title="입력 에러", message="해당 원문은 이미 존재합니다.")
                return
            self.addnote(o_input, t_input)
        
        self.addbutton = tk.Button(addwordframe, text="추가", command=addfunction)
        self.addbutton.grid(row=0, column=6, padx=(0, 5), pady=(10, 10))
        
        def changefunction():
            try:
                curItem = self.reviewtable.focus()
            except:
                return
            o_input, t_input, correct_input, total_input = self.reviewtable.item(curItem)['values']
            co_input, ct_input = self.origininput.get("1.0", tk.END)[:-1], self.transinput.get("1.0", tk.END)[:-1]
            self.reviewtable.item(curItem, text="", values=(co_input, ct_input, correct_input, total_input))
            self.changenote(o_input, t_input, co_input, ct_input)
        
        self.changebutton = tk.Button(addwordframe, text="변경", command=changefunction)
        self.changebutton.grid(row=0, column=7, padx=(0, 5), pady=(10, 10))
        
        def deletefunction():
            try:
                curItem = self.reviewtable.focus()
            except:
                return
            o_input, t_input, correct_input, total_input = self.dicttable.item(curItem)['values']
            selected_item = self.reviewtable.selection()[0] ## get selected item
            self.reviewtable.delete(selected_item)
            self.origininput.delete("1.0", "end")
            self.transinput.delete("1.0", "end")
            self.deletenote(o_input, t_input)
        
        self.deletebutton = tk.Button(addwordframe, text="삭제", command=deletefunction)
        self.deletebutton.grid(row=0, column=8, padx=(0, 5), pady=(10, 10))

        def dicttableclick(event):
            item = self.reviewtable.identify('item', event.x, event.y)
            try:
                o_input, t_input = self.reviewtable.set(item).values()
            except:
                return
            self.origininput.delete("1.0", "end")
            self.origininput.insert("1.0", o_input)
            self.transinput.delete("1.0","end")
            self.transinput.insert("1.0", t_input)

        
        # 원문 - 번역문 테이블 생성
        self.reviewtable = ttk.Treeview(self.root, columns=["Origin Text", "Translated Text", "Correct", "Total"], displaycolumns=["Origin Text", "Translated Text", "Correct", "Total"])
        self.reviewtable.bind("<Button-1>", dicttableclick)
        self.reviewtable.pack()
        
        self.reviewtable.column("Origin Text", width="192", anchor="center")
        self.reviewtable.heading("Origin Text", text="Origin Text")
        
        self.reviewtable.column("Translated Text", width="192", anchor="center")
        self.reviewtable.heading("Translated Text", text="Translated Text")
        
        self.reviewtable.column("Correct", width="50", anchor="center")
        self.reviewtable.heading("Correct", text="Correct")
        
        self.reviewtable.column("Total", width="50", anchor="center")
        self.reviewtable.heading("Total", text="Total")
        
        self.reviewtable["show"] = "headings"
        
        for i, [score, origin, trans, correct, total] in enumerate(self.reviewnote):
            try:
                self.reviewtable.insert("", "end", text="", values=(origin, trans, correct, total), iid = origin)
            except:
                pass
        
    
    def addnote(self, origin, trans):
        f = open(self.filename, "a", encoding = "UTF-8")
        f.write(f"{origin}\t{trans}\t{0}\t{0}\t{0}\n")
        f.close()

    def changenote(self, origin, trans, c_origin, c_trans):
        s_delete = f"{origin}\t{trans}\t"
        s_insert = f"{c_origin}\t{c_trans}\t"
        new_t = ""
        with open(self.filename, "r", encoding="UTF-8") as f:
            while True:
                line = f.readline()
                if not line:
                    break
                if s_delete in line:
                    p_origin, p_trans, score, correct, total = line.split('\t')
                    new_s = s_insert+f'{score}\t{correct}\t{total}'
                else:
                    new_s = line
                if new_s:
                    new_t += new_s
        with open(self.filename,'w', encoding="UTF-8") as f:
            f.write(new_t)
    
    def deletenote(self, origin, trans):
        s_delete = f"{origin}\t{trans}\t"
        new_t = ""
        with open(self.filename, "r", encoding="UTF-8") as f:
            while True:
                line = f.readline()
                if not line:
                    break
                if s_delete in line:
                    new_s = ""
                else:
                    new_s = line
                if new_s:
                    new_t += new_s
        with open(self.filename, "w", encoding="UTF-8") as f:
            f.write(new_t)

if __name__ == "__main__":
    c = reviewwindows()
    c.root.mainloop()