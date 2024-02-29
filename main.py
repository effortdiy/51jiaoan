from services import doc_service
import logging
import asyncio

log_format = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.INFO,format=log_format)

if __name__ == "__main__":
    url = input("输入需要下载的URL地址:") or "https://www.51jiaoxi.com/albums-6712.html"
    ds = doc_service.docService()
    asyncio.run(ds.run(url))