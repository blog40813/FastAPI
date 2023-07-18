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


## Go to Web<br>

* 直接在電腦上啟用FastAPI<br>

  可以藉由自行設定的IP位置或是他給定的IP位置使用FastAPI，不設置就是預設 http://127.0.0.1:8000
* Docker 使用者<br>

  若IP設定 0.0.0.0 可以使用 ipconfig 查看自己IP位置再連上 `http://IP:8000` 或使用 `http://127.0.0.1:8000`

* **注意，127.0.0.1只能給本機使用，若要同區域網內可連接，需使用 `http://IP:8000`**
    


