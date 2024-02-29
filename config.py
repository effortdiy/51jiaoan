URLS= ["https://www.51jiaoxi.com/albums-1607.html","https://www.51jiaoxi.com/albums-212.html"]

PRE_URL = "https://www.51jiaoxi.com/api/document/preview?document_id={}&all=1"
HEADER = {          
"ACCPET":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
"Accept-Encoding":"gzip",
"Accept-Language":"zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.62",
}

DATA_FOLDER = r"./.data" # 临时文件转正后的数据
TEMP_FOLDER = r"./.temp" # 临时路径，随时可以删除，用于做文件缓存