# Function<br>
* **Upload_txt**：上傳txt/log檔至data/txt資料夾<br><br>
* **txt_to_csv**：從電腦中選擇txt/log檔，生成csv/xlsc檔至data/csv_xlsx資料夾<br>生成檔名為：上傳的文件名+.csv/xlsx<br>
  舉例來說：123.log生成的名字就是123.log.csv<br><br>
* **txt_to_csv_all**：將所有在data/txt的檔案，生成csv/xlsx檔至data/csv_xlsx資料夾，結束後將已使用過檔案放至data/txt/finish資料夾中<br><br>
* **GetFile/{filename}**：獲取在data裡面的txt/log/csv/xlsx檔案，輸入(檔名.副檔名)，即可檢視下載<br><br>
* **Plot**：從電腦中選擇csv/xlsx檔案，並輸入資料的起始日期(yyyyddmm)，會自動切分日期以及每一天資料的報表<br><br>
* **GetChart/{filename}**：輸入要查詢的報表 (csv/xlsx檔案名.副檔名_yyyymmdd_number)<br><br>
  舉例來說，以usage.csv生成的報表，查詢資料日期為20010101的第一張圖片則輸入為：usage.csv_20010101_1

# Operation<br>

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
