import requests
import json

# papago language code : https://developers.naver.com/docs/papago/papago-nmt-api-reference.md#%EC%98%A4%EB%A5%98-%EC%BD%94%EB%93%9C


class papagotranslator:
    def __init__(self):
        self.url = "https://openapi.naver.com/v1/papago/n2mt"
        self.client_id = "YOUR_CLIENT_ID" # 개발자센터에서 발급받은 Client ID 값
        self.client_secret = "YOUR_CLIENT_SECRET" # 개발자센터에서 발급받은 Client Secret 값
        self.headers = {
            'Content-Type':'application/json',
            'X-Naver-Client-Id':self.client_id,
            'X-Naver-Client-Secret':self.client_secret
        }
        
        self.text = ""
        self.data = { # default : ja -> ko
            'source': 'ja',
            'target': 'ko',
            'text': self.text
        }

    def setId(self, id, secret):
        self.client_id = id
        self.client_secret = secret
        self.headers['X-Naver-Client-Id'] = self.client_id
        self.headers['X-Naver-Client-Secret'] = self.client_secret
    
    def setLanguage(self, source, target):
        self.data['source'] = source
        self.data['target'] = target
    
    def translate(self, text):
        self.text = text
        self.data['text'] = self.text
        
        response = requests.post(self.url, json.dumps(self.data), headers=self.headers)
        try:
            return response.json()['message']['result']['translatedText']
        except KeyError:
            return self.errorMessage(response.json())
    
    def errorMessage(self, err):
        return err['errorMessage']

if __name__ == "__main__":
    translator = papagotranslator()
    id, secret = input('Input id and secret>>').split()
    translator.setId(id, secret)
    print(translator.translate("天ちゃんがめぐるちゃんに向けて言った。"))
    