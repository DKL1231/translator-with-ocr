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
    
    def updateDict(self):
        self.Dictfile = open(self.filename, "r", encoding=self.encoding)
        CustomDict.CustomDict = {}
        
        for sentence in self.Dictfile.readlines():
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