import googletrans
import CustomDict

class googletranslator:
    def __init__(self):
        self.translator = googletrans.Translator()
        self.src = 'ja' # default src is japanese
        self.dest = 'ko' # default dest is korean
        self.CustomDict = CustomDict.CustomDict()
    
    def translate(self, text):
        text = self.CustomDict.sentenceProcessing(text)
        print(text)
        result = self.translator.translate(text, src=self.src, dest=self.dest)
        return result.text
    
    def setLanguage(self, src, dest):
        self.src = src
        self.dest = dest


if __name__ == "__main__":
    translator = googletranslator()
    print(translator.translate("天ちゃんがめぐるちゃんに向けて言った。"))
     