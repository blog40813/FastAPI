from fastapi import APIRouter,FastAPI,Path


web = APIRouter()
import sys
sys.path.append("D:\Fastapi\exercise")

from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from application import main


##可以自己設置swagger UI的路徑位置，但如果是設置在docs沒有用
#抑或是這邊設置 "路徑" 但main.py裡面 "路徑" 已經有東西的話就沒辦法覆寫

#include_in_schema是指要不要把此函數顯現在網頁上

@web.get("/", response_class=HTMLResponse,include_in_schema=False)
def home():
    return """
    <html>
    <head>
        <title>FastAPI Swagger UI</title>
        <link rel="stylesheet" type="text/css" href="/sta/swagger-ui.css">
        <script src="/sta/swagger-ui-bundle.js"></script>
        <script src="/sta/swagger-ui-standalone-preset.js"></script>
    </head>
    <body>
        <div id="swagger-ui"></div>
        <script>
            const ui = SwaggerUIBundle({
                url: "/openapi.json",
                dom_id: "#swagger-ui",
                presets: [
                    SwaggerUIBundle.presets.apis,
                    SwaggerUIStandalonePreset
                ],
                layout: "BaseLayout"
            })
        </script>
    </body>
    </html>
    """



# 将静态文件夹路径指向 Swagger UI 的文件夹路径
#put the needed file to sta (index.jsx/swagger-ui.css/swagger-ui-bundle.js/swagger-ui-standalone-preset.js)
web.mount("/sta", StaticFiles(directory=main.sta_path), name="sta")

'''-----------------------2023/05/30 version-----------------------'''