
from bs4 import BeautifulSoup
from . import utils
import logging
import config
import configparser
import os

class docService():

    def __init__(self) -> None:
        self.config = config
        if not os.path.exists(config.TEMP_FOLDER):
            os.mkdir(config.TEMP_FOLDER)

        if not os.path.exists(config.DATA_FOLDER):
            os.mkdir(config.DATA_FOLDER)


    async def run(self, url):
        """ 获取网页信息 """
        logging.info("获取网页信息中！")
        # 1. 获取所有下载地址
        res = utils.http_get(url=url)
        html_obj = BeautifulSoup(res.text, "lxml")

        title = self.__get_title(html_obj)
        file =  self.__check_exists(title)
        if not file:
            jiaoan_obj = self.__jiaoan(html_obj)
            file = self.__write_downloadurl(title, jiaoan_obj)

        # 2. 下载所有文件
        file_obj = self.__read_downloadurl(file)
        await self.__downloadurl(title,file_obj)

        # 3. 合并文档
        self.__trans_doc(title)

        logging.info("获取网页信息完毕！")
        return title

    def __trans_doc(self,title):
        """ 合并文档 """
        src_doc_dir = os.path.join(self.config.TEMP_FOLDER,title)
        dest_doc_dir = os.path.join(self.config.DATA_FOLDER,title)
        if not os.path.exists(src_doc_dir):
            os.mkdir(src_doc_dir)
        if not os.path.exists(dest_doc_dir):
            os.mkdir(dest_doc_dir)
        utils.trans_doc(src_doc_dir,dest_doc_dir)


    def __check_exists(self,title):
        path = os.path.join(self.config.TEMP_FOLDER,title+".txt")
        if os.path.exists(path):
            return path

    async def __downloadurl(self,title, file_obj):
        """ 开始下载文件 """
        logging.info("文件开始下载...")

        root_dir = os.path.join(self.config.TEMP_FOLDER,title)
        if not os.path.exists(root_dir):
            os.mkdir(root_dir)

        for sections_name in file_obj.sections():
            sections = file_obj[sections_name]
            logging.info(f'下载文件中[{sections.get("title")}]--{sections.get("url")}')
            await utils.download_img(os.path.join(root_dir,sections.get("title")),sections.get("url"),sections.get("file_type"))

        logging.info("文件下载done！")
    def __read_downloadurl(self, file):
        """ 读取下载地址 """
        _config = configparser.ConfigParser()
        _config.read(file,encoding="utf8")
        return _config
    def __write_downloadurl(self, title, jiaoan_obj):
        """ 保存下载地址 """
        filepath = f"{self.config.TEMP_FOLDER}/{title}.txt"
        _config = configparser.ConfigParser()

        for i,data in enumerate(jiaoan_obj):
            _config.add_section(str(i))
            for k,v in data.items():
                _config.set(str(i), k,str(v))
        with open(filepath, "w", encoding="utf-8") as f:
            _config.write(f)
        return filepath

    def __get_title(self, html_obj):
        """ 获取标题 """
        if html_obj.find("span", class_="tit") and html_obj.find("span", class_="tit").text != '':
            return html_obj.find("span", class_="tit").text
        return html_obj.title.text
                

    def __jiaoan(self, html_obj, course_id=None):
        """
        开始处理页面数据
        """

        # 判断这个地方如果是教案，则通过下列方法进行下载
        els = html_obj.find_all('div', class_="doc-preview")

        for el in els:
            d_id = el.attrs.get("data-id")
            res = utils.http_get(url=self.config.PRE_URL.format(d_id))
            doc_js = res.json()
            for data in doc_js["data"]:
                stage_id = data['stage_id']  # 1
                subject_id = data['subject_id']  # 1017
                document_id = data['document_id']  # 12940185
                for format_subsets in data["format_subsets"]:
                    title = format_subsets["title"]
                    item_id = format_subsets["item_id"]  # 0
                    total_files_count = format_subsets["total_files_count"]
                    can_view_file_count = format_subsets["can_view_file_count"]
                    remains_files_count = format_subsets["remains_files_count"]
                    # urls = []
                    # for i in range(0,total_files_count):
                    for preview_files in format_subsets["preview_files"]:
                        # urls.append(preview_files["url"])
                        file_type = preview_files['file_type']
                        file_url = preview_files['file_url']
                        guess_type = preview_files['guess_type']
                        url = preview_files['url']

                        # csv_writer.writerow([head, stage_id, document_id, title, item_id, total_files_count,
                        #                      can_view_file_count, remains_files_count, file_type, file_url, guess_type, url])

                        yield dict(stage_id=stage_id, document_id=document_id, title=title,
                                   item_id=item_id, subject_id=subject_id, total_files_count=total_files_count, can_view_file_count=can_view_file_count,
                                   remains_files_count=remains_files_count, file_type=file_type, file_url=file_url, guess_type=guess_type, url=url, course_id=course_id)
                        # f.flush()
