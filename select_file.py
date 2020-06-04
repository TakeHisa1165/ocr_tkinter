"""
ファイル選択用gui生成
"""

import sys
import PySimpleGUI as sg
import tk_canvas
import w_csv
import os
import csv


class MainWindow:
    """
    gui
    """
    def __init__(self):
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        try:
            with open('path.csv', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    self.dir_path = row["dir_path"]

        except FileNotFoundError:
            sg.popup_ok('初期設定が必要です。\n設定画面から書き出しフォルダを設定してください')
            SelectFile()

    def main_window(self):
        """
        メインwindwow
        # """
        sg.theme("systemdefault")

        frame = [
            [sg.Text('読み取る言語')],
            [sg.Radio("日本語", key="-jpn-", group_id=1)],
            [sg.Radio('英語', key="-eng-", group_id=1)],
        ]
        layout = [
            [sg.MenuBar([["設定",["フォルダ設定"]]], key="menu1")],
            [sg.Text('読み取るファイルを選択してください')],
            [sg.InputText(size=(100, 1), key="-file_path-"), sg.FileBrowse('読み取るファイルを選択')],
            [sg.Frame("言語選択", frame)],
            [sg.Submit(button_text="読み取り開始")],
            # [sg.Text('読み取り結果')],
            # [sg.Output(size=(100, 30))],
            [sg.Submit(button_text="閉じる")]

        ]
        window = sg.Window("OCR", layout)
        while True:
            event, values = window.read()
            if event is None:
                print("exit")
                sys.exit()

            if event == "読み取り開始":
                image_path = values["-file_path-"]
                if values["-jpn-"]:
                    lang = "jpn"
                elif values["-eng-"]:
                    lang = "eng"

                print(image_path)
                print(lang)
                window.close()
                tk_canvas.main_loop(select_lang=lang, image_path=image_path, dir_path=self.dir_path)

            if values["menu1"] == "フォルダ設定":
                SelectFile()

            if event == "閉じる":
                sys.exit()



        window.close()


class SelectFile:
    def __init__(self):
        self.path_dict = self.select_file()
        
    def select_file(self):

        sg.theme('SystemDefault')

        layout = [
            [sg.Text('読み取り結果を書き出すフォルダを選んでください', size=(50, 1), font=('メイリオ', 14))], 
            [sg.InputText(font=('メイリオ', 14)),sg.FolderBrowse('開く', key='File1', font=('メイリオ', 14))],
            [sg.Submit(button_text='設定', font=('メイリオ', 14)), sg.Submit(button_text="閉じる", font=('メイリオ', 14))]
        ]

        # セクション 2 - ウィンドウの生成z
        window = sg.Window('ファイル選択', layout)

        # セクション 3 - イベントループ
        while True:
            event, values = window.read()

            if event is None:
                print('exit')
                break

            if event == '設定':
                path_dict = {}
                dir_path = values[0]
                path_dict["dir_path"] = dir_path
                csv = w_csv.Write_csv()
                csv.write_csv(path_dict=path_dict)

                return path_dict
            if event == '閉じる':
                break




        #  セクション 4 - ウィンドウの破棄と終了
        window.close()

if __name__ == "__main__":
    a = MainWindow()
    a.main_window()
