"""
画像をOCRでテキストに変換
"""
import sys
import os
from PIL import Image
import PySimpleGUI as sg
import pyocr
import pyocr.builders
import select_file
import csv

# import cv2


class Image_to_Text:
    """
    画像からテキストを抽出
    """
    def image_to_text(self, image_path_list, select_lang, dir_path):
        """
        画像からテキストを抽出
        """
        print("文字認識中")
        if select_lang == "jpn":
            lang_index = 2
        elif select_lang == "eng":
            lang_index = 0
        tools = pyocr.get_available_tools()
        if len(tools) == 0:
            print("OCRツールがありません")
            sys.exit()

        tool = tools[0]
        print("使用するOCRツール{}".format(tool.get_name()))

        langs = tool.get_available_languages()
        print("選択可能な言語{}".format(langs))
        lang = langs[lang_index]
        print("選択した言語={}".format(lang))

        for path in image_path_list:
            txt = tool.image_to_string(
                Image.open(path),
                lang=lang,
                builder=pyocr.builders.TextBuilder(tesseract_layout=3))
            print(txt)
            with open("test.txt", "w") as f:
                print(txt, file=f)

        datas = "test.txt"
        file_csv = datas.replace('txt', "csv")

        with open(datas) as rf:
            csv_path = dir_path + "\\読み取り結果.csv"
            with open(csv_path, "w", newline="") as wf:
                readfile = rf.readlines()
                for read_text in readfile:
                    read_text = read_text.split()
                    writer = csv.writer(wf, delimiter=",")
                    writer.writerow(read_text)

        for path in image_path_list:
            pass
            # os.remove(path)
        sg.popup('完了しました')
        a = select_file.MainWindow()
        a.main_window()



