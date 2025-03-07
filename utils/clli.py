import subprocess
import sys
import time

sys.stderr.write("!!!THIS CLI WAS CREATED ONLY FOR QUICK LINUX CONFIGURATION!!!\n")

START_FILE_NAME = "bot.service"
PROMPT = "> "

menu = (
    "1: run",
    "2: stop",
    "3: status",
    "4: exit",
    "5: help",
)


def cli_help():
    print("-" * 20 + "\n| ", end="")
    print("\n| ".join(menu))
    print("-" * 20)


def run():
    print("| Reload")
    res = subprocess.run(["systemctl", "daemon-reload"], capture_output=True, text=True)
    if "Access denied" in res.stderr:
        print("> Access denied")
        return
    print("| Enable")
    subprocess.run(["systemctl", "enable", START_FILE_NAME])
    print("| Start")
    subprocess.run(["systemctl", "start", START_FILE_NAME])
    print("> Running success")


def stop():
    subprocess.run(["systemctl", "disable", START_FILE_NAME])
    print("> Stopped process")


def status():
    res = subprocess.run(["systemctl", "status", "bot.service"], capture_output=True, text=True)
    if "could not be found" in res.stderr:
        print("> Process isn't running")
    else:
        print("> It's running ({0})".format(res.stdout))


def main():
    time.sleep(0.5)
    cli_help()
    while True:
        command = input(PROMPT)
        match command:
            case "1":
                run()
            case "2":
                stop()
            case "3":
                status()
            case "4":
                exit()
            case '5':
                cli_help()
            case _:
                print("> Command not found")
                cli_help()


if __name__ == "__main__":
    main()
