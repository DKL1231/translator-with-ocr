import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import random
import time

class reviewwindows:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Review Note")
        self.root.geometry("600x400")
        self.filename = "study/reviewnote.txt"
        
        self.reviewnoteupdate()
        self.suddenpercent = 0.3
        
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
            o_input, t_input, correct_input, total_input = self.reviewtable.item(curItem)['values']
            selected_item = self.reviewtable.selection()[0] ## get selected item
            self.reviewtable.delete(selected_item)
            self.origininput.delete("1.0", "end")
            self.transinput.delete("1.0", "end")
            self.deletenote(o_input, t_input)
        
        self.deletebutton = tk.Button(addwordframe, text="삭제", command=deletefunction)
        self.deletebutton.grid(row=0, column=8, padx=(0, 5), pady=(10, 10))

        def reviewtableclick(event):
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
        self.reviewtable.bind("<Button-1>", reviewtableclick)
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
        
        self.testbutton = tk.Button(self.root, text="Review Test", command=self.teststart)
        self.testbutton.pack(pady=(10, 10))
    
    def reviewnoteupdate(self):
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
        f.close()
    
    def teststart(self):
        self.reviewnoteupdate()
        if len(self.reviewnote) == 0:
            tk.messagebox.showerror(title="Error", message="출제할 단어가 존재하지 않습니다.")
            return
        random.seed(time.time())
        self.idxlst = [i for i in range(min(20, len(self.reviewnote)))]
        random.shuffle(self.idxlst)
        if len(self.reviewnote) < 20:
            testnote = sorted(self.reviewnote)
        testnote = sorted(self.reviewnote)[:20]
        
        testwindow = tk.Tk()
        testwindow.title("ReviewTest")
        testwindow.geometry("300x100")
        
        def testchanger():
            if self.testinput.get("1.0", tk.END)[:-1] == testnote[self.idxlst[self.idx-1]][2]:
                self.score += 1
                self.corrected.append(testnote[self.idxlst[self.idx-1]])
                print(self.corrected)
            else:
                self.wrong.append(testnote[self.idxlst[self.idx-1]])
                print(self.wrong)
            if self.idx == len(self.idxlst):
                print(self.corrected)
                print(self.wrong)
                for data in self.corrected:
                    data = [((int(data[3])+1)*100/(int(data[4])+1))//1, data[1], data[2], int(data[3])+1, int(data[4])+1]
                    self.updatescore(data)
                print()
                for data in self.wrong:
                    data = [((int(data[3]))*100/(int(data[4])+1))//1, data[1], data[2], data[3], int(data[4])+1]
                    self.updatescore(data)
                
                for i in self.reviewtable.get_children():
                    self.reviewtable.delete(i)
                self.reviewnoteupdate()
                for _, [score, origin, trans, correct, total] in enumerate(self.reviewnote):
                    try:
                        self.reviewtable.insert("", "end", text="", values=(origin, trans, correct, total), iid = origin)
                    except:
                        pass
                
                resultmessage = f"{len(self.idxlst)}문제 중 {self.score}문제 맞추셨습니다."
                if self.idxlst != self.score:
                    resultmessage += "\n틀린 문제는"
                    for data in self.wrong:
                        resultmessage += f"\n{data[1]}\t{data[2]}"
                    resultmessage += "\n입니다."
                tk.messagebox.showinfo(title="Result", message=resultmessage)
                testwindow.destroy()
                return
            self.idx += 1
            self.testLabel.config(text=f"{self.idx}. {testnote[self.idxlst[self.idx-1]][1]}의 뜻은?")
            self.testinput.delete("1.0", "end")
        
        self.idx = 1
        self.score = 0
        self.testLabel = tk.Label(testwindow, text=f"{self.idx}. {testnote[self.idxlst[self.idx-1]][1]}의 뜻은?")
        self.testLabel.pack(pady=10)
        self.testinput = tk.Text(testwindow, width=10, height=1)
        self.testinput.pack(pady=10)
        self.submitbutton = tk.Button(testwindow, text="Submit", command=testchanger)
        self.submitbutton.pack()
        
        self.corrected = []
        self.wrong = []
        
    def updatescore(self, data):
        s_change = f"{data[1]}\t{data[2]}\t"
        s_insert = f"{data[1]}\t{data[2]}\t{data[0]}\t{data[3]}\t{data[4]}\n"
        new_t = ""
        with open(self.filename, "r", encoding="UTF-8") as f:
            while True:
                line = f.readline()
                if not line:
                    break
                if s_change in line:
                    new_s = s_insert
                else:
                    new_s = line
                if new_s:
                    new_t += new_s
        with open(self.filename,'w', encoding="UTF-8") as f:
            f.write(new_t)
    
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

    def checksentence(self, sentence):
        self.reviewnoteupdate()
        for [score, origin, trans, correct, total] in self.reviewnote:
            if origin in sentence:
                random.seed(time.time())
                if random.uniform(0, 1) <= self.suddenpercent:
                    self.createsuddenwindow([score, origin, trans, correct, total])

    def createsuddenwindow(self, lst):
        [score, origin, trans, correct, total] = lst
        suddenwindow = tk.Tk()
        suddenwindow.title("SuddenTest")
        suddenwindow.geometry("300x100")
        
        def singletest():
            data = lst
            if testinput.get("1.0", tk.END)[:-1] == trans:
                tk.messagebox.showinfo(title="Correct!", message="정답입니다.")
                data = [((int(data[3])+1)*100/(int(data[4])+1))//1, data[1], data[2], int(data[3])+1, int(data[4])+1]
                suddenwindow.destroy()
            else:
                tk.messagebox.showinfo(title="Wrong!", message=f"틀렸습니다.\n정답은 {trans}입니다.")
                data = [((int(data[3]))*100/(int(data[4])+1))//1, data[1], data[2], data[3], int(data[4])+1]
                suddenwindow.destroy()
            self.updatescore(data)
            for i in self.reviewtable.get_children():
                self.reviewtable.delete(i)
            self.reviewnoteupdate()
            for _, [score, origin, trans, correct, total] in enumerate(self.reviewnote):
                try:
                    self.reviewtable.insert("", "end", text="", values=(origin, trans, correct, total), iid = origin)
                except:
                    pass
        
        testLabel = tk.Label(suddenwindow, text=f"{origin}의 뜻은?")
        testLabel.pack(pady=10)
        testinput = tk.Text(suddenwindow, width=10, height=1)
        testinput.pack(pady=10)
        submitbutton = tk.Button(suddenwindow, text="Submit", command=singletest)
        submitbutton.pack()
        pass
    
if __name__ == "__main__":
    c = reviewwindows()
    c.root.mainloop()