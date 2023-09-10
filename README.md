# Hello

This is my Fast API Exercise 

## How to Start
* **Clone this repository to your directory.**

```
git clone https://github.com/blog40813/FastAPI.git
cd FastAPI
```

## 如果想直接在電腦上使用FastAPI：
### **Step 1 :** 建立虛擬環境

<br>

* 個人習慣使用anaconda，virtualenv指令:<br>

```
virtualenv venv
```
<br>

* 根據不同系統進入虛擬環境之後，可以利用requirement.txt安裝環境<br>

```
pip install -r requirement.txt 
```
<br>

### **Step 2 :** 輸入指令執行FastAPI<br>
<br>


* 先移動到main.py所在的資料夾(Vscode等程式的terminal)<br>

```
cd application
```
<br>

* 啟用FastAPI<br>

```
uvicorn main:app --host "your IP" --port "your port" --reload
uvicorn main:app --reload 
```
<br>

* 在電腦上建立虛擬環境，執行FastAPI(影片示範)

<a href="https://www.youtube.com/watch?v=iZnWB5UkSIE&list=PLaJlXBE6wMy_gOHV2Bkvcd7eM8tpt_I1I&index=6" target="_blank">
  <img src="https://res.cloudinary.com/marcomontalbano/image/upload/v1689907729/video_to_markdown/images/youtube--iZnWB5UkSIE-c05b58ac6eb4c4700831b2b3070cd403.jpg" alt="FastAPI venv" style="width: 450px; height: auto;">
</a><br><br>

<!-- [![FastAPI venv](https://res.cloudinary.com/marcomontalbano/image/upload/v1689907729/video_to_markdown/images/youtube--iZnWB5UkSIE-c05b58ac6eb4c4700831b2b3070cd403.jpg)](https://www.youtube.com/watch?v=iZnWB5UkSIE&list=PLaJlXBE6wMy_gOHV2Bkvcd7eM8tpt_I1I&index=6 "FastAPI venv")
-->


<br>

## 利用Docker啟用FastAPI：
### **Step 1 :** 下載docker desktop等docker工具<br>
* 這邊就請大家自行搜尋，或是去官網 https://www.docker.com/ 下載相關工具<br><br>

### **Step 2 :** 建立docker image並啟用<br>


* 開啟Terminal，移動到FastAPI資料夾後執行：<br>
  
```
docker-compose up
```

<br>

* 查看執行中的container<br>

```
docker ps 
```

<br>

* 查看剛剛建立的image<br>

```
docker images
```

* 藉由docker 啟動 API(影片)<br>

<a href="https://www.youtube.com/watch?v=nV48E4oxDlA&list=PLaJlXBE6wMy_gOHV2Bkvcd7eM8tpt_I1I&index=5" target="_blank">
  <img src="https://res.cloudinary.com/marcomontalbano/image/upload/v1689899668/video_to_markdown/images/youtube--nV48E4oxDlA-c05b58ac6eb4c4700831b2b3070cd403.jpg" alt="API with docker-compose up" style="width: 300px; height: auto;">
</a><br><br>

* docker重啟API(影片)<br>

<a href="https://www.youtube.com/watch?v=Qtk01MIYQr8&list=PLaJlXBE6wMy_gOHV2Bkvcd7eM8tpt_I1I&index=4" target="_blank">
  <img src="https://res.cloudinary.com/marcomontalbano/image/upload/v1689903494/video_to_markdown/images/youtube--Qtk01MIYQr8-c05b58ac6eb4c4700831b2b3070cd403.jpg" alt="docker restart" style="width: 300px; height: auto;">
</a><br><br>

<!-- [![docker restart](https://res.cloudinary.com/marcomontalbano/image/upload/v1689903494/video_to_markdown/images/youtube--Qtk01MIYQr8-c05b58ac6eb4c4700831b2b3070cd403.jpg)](https://www.youtube.com/watch?v=Qtk01MIYQr8&list=PLaJlXBE6wMy_gOHV2Bkvcd7eM8tpt_I1I&index=4 "docker restart")  -->


## Go to Web<br>

* 直接在電腦上啟用FastAPI<br>

  可以藉由自行設定的IP位置或是他給定的IP位置使用FastAPI，不設置就是預設 http://127.0.0.1:8000
* Docker 使用者<br>

  若IP設定 0.0.0.0 可以使用 ipconfig 查看自己IP位置再連上 `http://IP:8000` 或使用 `http://127.0.0.1:8000`

* **注意，127.0.0.1只能給本機使用，若要同區域網內可連接，需使用 `http://IP:8000`**


## Function<br>
* **Upload_txt**：上傳txt/log檔至data/txt資料夾<br><br>
* **txt_to_csv**：從電腦中選擇txt/log檔，生成csv/xlsc檔至data/csv_xlsx資料夾<br>生成檔名為：上傳的文件名+.csv/xlsx<br>
  舉例來說：123.log生成的名字就是123.log.csv<br><br>
* **txt_to_csv_all**：將所有在data/txt的檔案，生成csv/xlsx檔至data/csv_xlsx資料夾，結束後將已使用過檔案放至data/txt/finish資料夾中<br><br>
* **GetFile/{filename}**：獲取在data裡面的txt/log/csv/xlsx檔案，輸入(檔名.副檔名)，即可檢視下載<br><br>
* **Plot**：從電腦中選擇csv/xlsx檔案，並輸入資料的起始日期(yyyyddmm)，會自動切分日期以及每一天資料的報表<br><br>
* **GetChart/{filename}**：輸入要查詢的報表 (csv/xlsx檔案名.副檔名_yyyymmdd_number)<br><br>
  舉例來說，以usage.csv生成的報表，查詢資料日期為20010101的第一張圖片則輸入為：usage.csv_20010101_1

## Operation<br>

* 上傳txt上server以及將server上txt轉換成xlsx、csv<br>

<a href="https://youtu.be/mI39DIBPfVM?list=PLaJlXBE6wMy_gOHV2Bkvcd7eM8tpt_I1I" target="_blank">
  <img src="https://res.cloudinary.com/marcomontalbano/image/upload/v1689902835/video_to_markdown/images/youtube--mI39DIBPfVM-c05b58ac6eb4c4700831b2b3070cd403.jpg" alt="upload txt" style="width: 300px; height: auto;">
</a><br><br>

<!-- [![](https://res.cloudinary.com/marcomontalbano/image/upload/v1689902835/video_to_markdown/images/youtube--mI39DIBPfVM-c05b58ac6eb4c4700831b2b3070cd403.jpg)](https://youtu.be/mI39DIBPfVM "")  -->

* 藉由xlsc、csv產生報表<br>

<a href="https://www.youtube.com/watch?v=X5KXdItp-EA&list=PLaJlXBE6wMy_gOHV2Bkvcd7eM8tpt_I1I&index=2" target="_blank">
  <img src="https://res.cloudinary.com/marcomontalbano/image/upload/v1689903207/video_to_markdown/images/youtube--X5KXdItp-EA-c05b58ac6eb4c4700831b2b3070cd403.jpg" alt="API plot" style="width: 300px; height: auto;">
</a><br><br>

* 尋找檔案、報表功能<br>

<a href="https://www.youtube.com/watch?v=J_Ijym5zOgE&list=PLaJlXBE6wMy_gOHV2Bkvcd7eM8tpt_I1I&index=3" target="_blank">
  <img src="https://res.cloudinary.com/marcomontalbano/image/upload/v1689903372/video_to_markdown/images/youtube--J_Ijym5zOgE-c05b58ac6eb4c4700831b2b3070cd403.jpg" alt="API find" style="width: 300px; height: auto;">
</a><br><br>

<!-- [![API find](https://res.cloudinary.com/marcomontalbano/image/upload/v1689903372/video_to_markdown/images/youtube--J_Ijym5zOgE-c05b58ac6eb4c4700831b2b3070cd403.jpg)](https://www.youtube.com/watch?v=J_Ijym5zOgE&list=PLaJlXBE6wMy_gOHV2Bkvcd7eM8tpt_I1I&index=3 "API find") "API plot")  -->



