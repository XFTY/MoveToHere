import os
import json
import sys
import time
import socket
import cryptocode

# 对日志系统进行基础配置
"""logging.basicConfig(
    filename="latest.log",
    filemode="w",
    format="[%(asctime)s/%(levelname)s]%(message)s",
    datefmt="%d-%M-%Y %H:%M:%S",
    level=logging.INFO
)"""


# 定义日志类
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


# 主程序
class TCPServer:
    def __init__(self):
        self.logging = logging()
        # 读取配置文件并赋值给self.config
        # 先尝试读取文件，如果文件不存在则终止程序运行
        self.logging.info("Loading config file")
        try:
            with open("config.json", "r", encoding="utf-8") as f:
                self.config = json.loads(f.read())
            self.logging.info("config file load successfully!")
        except Exception as e:
            self.logging.error("{}".format(e))
            self.logging.info("stopping server ...")
            sys.exit()

        self.logging.info("Starting socket ...")

        try:
            # 创建socket连接并监听由配置文件提供的IP和端口
            # 当然，这和FIB和IAA没有关系，(玩5玩的)[doge]
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # self.server.bind(("127.0.0.1",25565))
            self.server.bind((self.config["ipconfig"]["server-ip"], int(self.config["ipconfig"]["server-port"])))
            self.server.listen(self.config["max_connect"])  # 监听，参数是最大连接数
        except Exception as e:
            self.logging.error("An error occurred that prevented the server from starting:")
            self.logging.error(e)
            self.logging.warning("Failed to start server! Have you set up your IP and port correctly?")
            self.close()

        # 服务器主代码
        # 无限循环，接受客户端的请求
        while True:
            # 接受客户端请求
            self.logging.info("done! waiting for client(s)")
            self.client, self.address = self.server.accept()
            # 存储获取的数据
            self.recv_data = self.client.recv(1024)
            self.recv_data.decode("utf-8")

    def testConnection(self):
        self.client.send(f"Welcome to connect {self.config['serverBasicConfig']['server-name']} server!".encode("utf-8"))

    def sendTextData(self, text):
        if self.config["serverBasicConfig"]["encryption-mode"]["enable"]:
            text = cryptocode.encrypt(text, self.config["serverBasicConfig"]["encryption-mode"]["key"])
            text = text.encode("utf-8")
        else:
            text.encode("utf-8")
        self.client.send(text)

    def close(self, code: str | int = -1):
        self.logging.info("stopping server ...")
        self.logging.close()
        sys.exit(code)

    def safeclose(self, code=0):
        self.logging.info("stopping server ...")
        self.server.close()
        self.logging.close()
        sys.exit(code)


class setup:
    # 如你所见，这是个半成品，说实话，半成品都不是。
    # 代码十分感人，不建议高血压人群观赏。
    def __init__(self):
        with open("config.json", "r", encoding="utf-8") as f:
            self.config = json.loads(f.read())
        print(
            """
====================================
Welcome to use Move-To-Here Server!
Version: {}
====================================

If you see this welcome title, the server setup is running!
And now, let's set-up your server!

Please wait a few seconds, we are setting up something ...

""".format(
                self.config["serverVersion"])
        )

        time.sleep(2)
        # print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n ")  # Why not clear the screen ???
        os.system("cls")  # That's right!

        print("I: Server EULA\n=====================\n")
        print("You need to agree our EULA to do the next setup\n")
        print("GNU-GPL: https://www.github.com/XFTY/moveToHere/LICENSE\n")
        print("Please read carefully and confirm if you agree\n\n")
        setc = input("Do you agree?(type 'y' for yes, and other keys for no): ")
        if setc == "y":
            self.config["eula"] = True
            self.set2()
        else:
            self.setfailed("EULA Not be agreed ...")

    def set2(self):
        self.clearScreen()
        setupconplete = False
        print("II: Server IP and Port config\n=====================\n")
        print("Please enter the IP address and port that needs to be listen\n")
        while not setupconplete:
            ip = input("\nServer IP: ")
            port = input("Server Port: ")

            print("\nIP: {}\nPort: {}".format(ip, port))
            if input("\n\nAre you sure you want to use this IP address and port\n(type 'y' for yes, and other keys for "
                     "no): ") == "y":
                setupconplete = True
            else:
                pass

    def setcomplete(self):
        os.system("cls")
        input(
            """
====================================
Welcome to use Move-To-Here Server!
Setup complete!
====================================

You have successfully installed this program!

Please press enter to continue

""")

    def setfailed(self, reason="reason unknown"):
        os.system("cls")
        input(
            """
====================================
Welcome to use Move-To-Here Server!
Setup failed!
====================================

reason: {}

Please press enter to continue

""".format(reason)
        )

    def clearScreen(self):
        os.system("cls")


if __name__ == "__main__":
    TCPServer()
