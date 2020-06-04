import tkinter as tk
import tkinter.ttk
from PIL import Image, ImageTk
import crop_by_pil

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack(expand=1)
        self.create_widgets()
        self.startup()

    def create_widgets(self):
        global im

        # 画像読み込み
        read_image = Image.open(path)
        # 画像のリサイズ
        self.height = 900
        self.width = round(read_image.width * self.height / read_image.height)
        resize_image = read_image.resize((self.width, self.height))
        resize_image.save(r"copy.png")


        # マウス位置を表示するラベル表記用の変数
        self.start_x = tk.StringVar()
        self.start_y = tk.StringVar()
        self.current_x = tk.StringVar()
        self.current_y = tk.StringVar()

        self.lb1 = tk.ttk.Label(self, text="マウスポジション")
        self.lb1.grid(row=0, column=1)
        # 左上Xのラベル表示
        self.label_start_x = tk.ttk.Label(self, textvariable=self.start_x)
        self.label_start_x.grid(row=1, column=1)
        # 左上yのラベル表示
        self.label_start_y = tk.ttk.Label(self, textvariable=self.start_y)
        self.label_start_y.grid(row=1, column=2)
        # 右下Xのラベル表示
        self.label_current_x = tk.ttk.Label(self, textvariable=self.current_x)
        self.label_current_x.grid(row=2, column=1)
        # 右下yのラベル表示
        self.label_current_y = tk.ttk.Label(self, textvariable=self.current_y)
        self.label_current_y.grid(row=2, column=2)
        # selct all ボタンの表示　クリックすると　関数select all を呼び出し
        self.select_all_button = tk.ttk.Button(self, text='Select All', command=self.select_all)
        self.select_all_button.grid(row=3, column=1)
        self.exit_button = tk.ttk.Button(self, text="閉じる", command=self.exit_loop)
        self.exit_button.grid(row=4, column=2)
        self.ocr_button = tk.ttk.Button(self, text="読み取り開始", command=self.ocr_start)
        self.ocr_button.grid(row=3, column=2)

        self.test_canvas = tk.Canvas(self, bg='lightblue',
            width=self.width, height=self.height,
            highlightthickness=0)
        im = ImageTk.PhotoImage(image=resize_image)
        self.test_canvas.create_image(0, 0, anchor='nw', image=im)
        self.test_canvas.grid(row=0, column=0, rowspan=30, padx=10, pady=10)
        self.test_canvas.bind('<ButtonPress-1>', self.start_pickup)
        self.test_canvas.bind('<B1-Motion>', self.pickup_position)

    # 関数でマウスで描画する枠の初期化
    def startup(self):
        self.rect_start_x = None
        self.rect_start_y = None
        self.rect = None

    def start_pickup(self, event):
        if 0 <= event.x <= self.width and 0 <= event.y <= self.height:
            # ラベル表示の文字列作成　stringvarへ
            self.start_x.set('左上X : ' + str(event.x))
            self.start_y.set('左上Y : ' + str(event.y))
            self.rect_start_x = event.x
            self.rect_start_y = event.y


    def pickup_position(self, event):
        if 0 <= event.x <= self.width and 0 <= event.y <= self.height:
            self.current_x.set('右下X : ' + str(event.x))
            self.current_y.set('右下Y : ' + str(event.y))
            self.stop_x = event.x
            self.stop_y = event.y
            if self.rect:
                self.test_canvas.coords(self.rect,
                    min(self.rect_start_x, event.x), min(self.rect_start_y, event.y),
                    max(self.rect_start_x, event.x), max(self.rect_start_y, event.y))
            else:
                self.rect = self.test_canvas.create_rectangle(self.rect_start_x,
                    self.rect_start_y, event.x, event.y, outline='red')

    def select_all(self):
        if self.rect:
            self.test_canvas.coords(self.rect, 0, 0, self.width, self.height)
        else:
            self.rect = self.test_canvas.create_rectangle(0, 0,
                self.width, self.height, outline='red')
        x0, y0, x1, y1 = self.test_canvas.coords(self.rect)
        self.start_x.set('x : ' + str(x0))
        self.start_y.set('y : ' + str(y0))
        self.current_x.set('x : ' + str(x1))
        self.current_y.set('y : ' + str(y1))






    def exit_loop(self):
        root.destroy()

    def ocr_start(self):
        root.destroy()
        crop_by_pil.crop_by_pil(select_lang=lang, start_x=self.rect_start_x, start_y=self.rect_start_y,
        current_X=self.stop_x, current_y=self.stop_y, path=path, resize_height=self.height, resize_width=self.width, dir_path=csv_dir_path)

def main_loop(select_lang, image_path, dir_path):
    global im, root, path, lang, csv_dir_path
    lang = select_lang
    path = image_path
    csv_dir_path = dir_path
    root = tk.Tk()
    app = Application(master=root)
    root.geometry(str(app.width + 400) + "x" + str(app.height + 100))
    app.mainloop()



if __name__ == "__main__":
    # main_loop("jpn", r"C:\Users\odyss\Downloads\test.png")
    pass
