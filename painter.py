import requests, json
from openai import OpenAI
from datetime import datetime
class Painter:
    def __init__(self):
        with open('set.json', 'r') as file:
            config = json.load(file)
        self.model = config.get('image-model')
        self.api = config.get('api_key')
        self.base_url = config.get('base_url')
    
    def response(self, prompt, filename):
        client = OpenAI(
            base_url=self.base_url,
            api_key=self.api,
        )

        resp = client.images.generate(
            prompt=prompt,
            model=self.model,
            response_format="url",
            size="1000x680",
        )
        image_url = resp.data[0].url       #获取图片URL
        headers = {"User-Agent": "Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"}
        response = requests.get(image_url, headers=headers, timeout=30)    #下载图片到本地
        with open(filename, "wb") as f:
            f.write(response.content)
        
def paint(prompt):
    try:
        painter = Painter()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        painter.response(prompt, 'user/'+now+'.png')
    except Exception as e:
        return str(e)
    return '成功生成图片并保存为' + ' user/'+now+'.png'

if __name__ == '__main__':
    paint('一只猫')