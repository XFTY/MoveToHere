import json
import socket
import tkinter
import tkinter.messagebox
import time

import cryptocode


class logging:
    def __init__(self):
        with open("latest.log", "a", encoding="utf-8") as f:
            f.write(
                "\n==========[Start in {}]==========\n".format(time.strftime("%Y/%m/%d %H:%m:%S", time.localtime())))

    # 写入文件并打印，私有函数
    def write(self, level, text):
        with open("latest.log", "a", encoding="utf-8") as f:
            log = "[{}/{}] {}".format(time.strftime("%Y/%m/%d %H:%m:%S", time.localtime()), level, text)
            f.write(log + "\n")
            print(log)

    def close(self):
        with open("latest.log", "a", encoding="utf-8") as f:
            f.write(
                "==========[End in {}]============\n\n\n".format(time.strftime("%Y/%m/%d %H:%m:%S", time.localtime())))

    # 类的接口
    def debug(self, text: str = None):
        self.write("DEBUG", text)

    def info(self, text=None):
        self.write("INFO", text)

    def warning(self, text: str = None):
        self.write("WARNING", text)

    def error(self, text: str = None):
        self.write("ERROR", text)

    def failed(self, text: str = None):
        self.write("FAILED", text)


class socketConnection:
    def __init__(self):
        self.logging = logging()
        with open("config.json", "a", encoding="utf-8") as f:
            self.config = json.loads(f.read())

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.config["ipconfig"]["server-ip"], self.config["ipconfig"]["server-port"]))

    def sendTextData(self, text: str):
        try:
            if self.config["encryption-mode"]["enable"]:
                text = cryptocode.encrypt(text)
                text = text.encode("utf-8")
            else:
                text.encode("utf-8")
            self.client.send(text)
        except Exception as e:
            self.logging.error(e)

    def normalConnection(self, code):
        self.sendTextData(code)
        self.client.recv()



class tkinterGUI(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.title("MovetoHere Client")
        self.width = 1024
        self.height = 512
        self.x_way = 10
        self.left = (self.winfo_screenwidth() - self.width) / 2
        self.top = (self.winfo_screenheight() - self.height) / 2
        self.geometry("{}x{}+{}+{}".format(int(self.width), int(self.height), int(self.left), int(self.top)))
        self.resizable(False, False)

        self.mainloop()

    # 警告返回，socketConnection事先记录日志
    def warningCallback(self, text: str, title: str = "警告"):
        tkinter.messagebox.showwarning(title, text)
