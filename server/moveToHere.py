import os
import json
import time


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
    setup()
