from flask import Flask, request, Response
from prefect import  client

app = Flask(__name__)

# 將以下兩行替換為您所需的帳號和密碼
USERNAME = "abc"
PASSWORD = "123"

def authenticate(username, password):
    return username == USERNAME and password == PASSWORD

@app.route('/')
def index():
    auth = request.authorization
    if not auth or not authenticate(auth.username, auth.password):
        return Response('未經授權', 401, {'WWW-Authenticate': 'Basic realm="需要登入"'})
    
    # 使用 Prefect Client 取得 UI HTML 內容
    client = client()
    html_content = client.graphql("query { ui }")
    return Response(html_content.encode("utf-8"), content_type="text/html")

if __name__ == '__main__':
    app.run(debug=True)