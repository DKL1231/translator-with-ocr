class CustomDict:
    CustomDict = {}
    def __init__(self):
        self.filename = "CustomDict/CustomDict.txt"
        self.encoding = 'UTF-8'
        self.Dictfile = None
        self.updateDict()
    
    def appendDict(self, origin, trans):
        self.Dictfile = open(self.filename, "a", encoding=self.encoding)
        self.Dictfile.write(f"{origin}\t{trans}\n")
        self.Dictfile.close()    
        
        self.updateDict()
    
    def removeDict(self, origin, trans):
        s_delete = f"{origin}\t{trans}\n"
        new_t = ""
        with open(self.filename, "r", encoding=self.encoding) as f:
            while True:
                line = f.readline()
                if not line:
                    break
                if line == s_delete:
                    new_s = ''
                else:
                    new_s = line
                if new_s:
                    new_t += new_s
        with open(self.filename,'w', encoding=self.encoding) as f:
            f.write(new_t)
        self.updateDict()

    def changeDict(self, origin, trans, c_origin, c_trans):
        s_delete = f"{origin}\t{trans}\n"
        s_insert = f"{c_origin}\t{c_trans}\n"
        new_t = ""
        with open(self.filename, "r", encoding=self.encoding) as f:
            while True:
                line = f.readline()
                if not line:
                    break
                if line == s_delete:
                    new_s = s_insert
                else:
                    new_s = line
                if new_s:
                    new_t += new_s
        with open(self.filename,'w', encoding=self.encoding) as f:
            f.write(new_t)
        self.updateDict()
    
    def updateDict(self):
        self.Dictfile = open(self.filename, "r", encoding=self.encoding)
        CustomDict.CustomDict = {}
        
        for sentence in self.Dictfile.readlines():
            if sentence == "": # 빈 라인 제외
                continue
            if sentence[:2] == "//":
                continue
            origin, trans = sentence.split("\t")
            trans = trans[:-1]
            
            if not origin in CustomDict.CustomDict:
                CustomDict.CustomDict[origin] = trans
            #print(origin, CustomDict.CustomDict[origin])

    def sentenceProcessing(self, sentence):
        newsentence = sentence
        for key, value in CustomDict.CustomDict.items():
            newsentence = newsentence.replace(key, value)
        return newsentence


if __name__ == "__main__":
    customdict = CustomDict()
    print(customdict.sentenceProcessing("天ちゃんがめぐるちゃんに向けて言った。"))