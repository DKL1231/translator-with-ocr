import googletrans
class CustomDict:
    CustomDict = {}
    ProcessDict = {}
    process_num = 1
    process_alpha = 0
    translator = googletrans.Translator()
    def __init__(self):
        self.filename = "CustomDict/CustomDict.txt"
        self.encoding = 'UTF-8'
        self.Dictfile = None
        self.updateDict()
    
    def appendDict(self, origin, trans, type):
        self.Dictfile = open(self.filename, "a", encoding=self.encoding)
        self.Dictfile.write(f"{origin}\t{trans}\t{type}\n")
        self.Dictfile.close()    
        
        self.updateDict()
    
    def removeDict(self, origin, trans, type):
        s_delete = f"{origin}\t{trans}\t{type}\n"
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

    def changeDict(self, origin, trans, type, c_origin, c_trans, c_type):
        s_delete = f"{origin}\t{trans}\t{type}\n"
        s_insert = f"{c_origin}\t{c_trans}\t{c_type}\n"
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
            origin, trans, type = sentence.split("\t")
            type = type[:-1]
            
            if not origin in CustomDict.CustomDict:
                CustomDict.CustomDict[origin] = (trans, type)

    def sentenceProcessing(self, sentence):
        newsentence = sentence
        for key, value in CustomDict.CustomDict.items():
            process_code = f'_{chr(65+CustomDict.process_alpha)}{CustomDict.process_num}'
            newsentence = newsentence.replace(key, process_code)
            CustomDict.ProcessDict[process_code] = value[0]
            CustomDict.process_num += 1
            if CustomDict.process_num == 10:
                CustomDict.process_num = 1
                CustomDict.process_alpha += 1
        return newsentence

    def sentenceProcessing_reverse(self, sentence):
        newsentence = sentence
        for key, value in CustomDict.ProcessDict.items():
            newsentence = newsentence.replace(key, value)
        CustomDict.ProcessDict = {}
        CustomDict.process_alpha = 0
        CustomDict.process_num = 0
        return newsentence

    def sentenceProcessing_TTS(self, sentence):
        newsenetence = sentence
        for key, value in CustomDict.CustomDict.items():
            if key in newsenetence and value[1] == '원음 표기':
                newvalue = CustomDict.translator.translate(value[0])
                newvalue = newvalue.extra_data['origin_pronunciation']
                newvalue = CustomDict.translator.translate(newvalue, src='en', dest='ja').text
                newsenetence = newsenetence.replace(key, newvalue)
        return newsenetence

if __name__ == "__main__":
    customdict = CustomDict()
    process0 = customdict.sentenceProcessing_TTS("黒坂 優香子さんの別名はゆかるんです。")
    print(process0)
    process1 = customdict.sentenceProcessing("黒坂 優香子さんの別名はゆかるんです。")
    print(process1)
    process2 = customdict.sentenceProcessing_reverse(process1)
    print(process2)