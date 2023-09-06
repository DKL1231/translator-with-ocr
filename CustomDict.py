class CustomDict:
    def __init__(self):
        self.filename = "CustomDict/CustomDict.txt"
        self.encoding = 'UTF-8'
        self.Dictfile = None
        self.CustomDict = {}
        self.updateDict()
    
    def appendDict(self, origin, trans):
        self.Dictfile = open(self.filename, "a", encoding=self.encoding)
        self.Dictfile.write(f"\n{origin}\t{trans}")
        self.Dictfile.close()    
        
        self.updateDict()
    
    def updateDict(self):
        self.Dictfile = open(self.filename, "r", encoding=self.encoding)
        self.CustomDict = {}
        
        for sentence in self.Dictfile.readlines():
            origin, trans = sentence.split("\t")
            trans = trans[:-1]
            
            if not origin in self.CustomDict:
                self.CustomDict[origin] = trans
            #print(origin, self.CustomDict[origin])

    
    def sentenceProcessing(self, sentence):
        newsentence = sentence
        for key, value in self.CustomDict.items():
            newsentence = newsentence.replace(key, value)
        return newsentence


if __name__ == "__main__":
    customdict = CustomDict()
    print(customdict.sentenceProcessing("天ちゃんがめぐるちゃんに向けて言った。"))