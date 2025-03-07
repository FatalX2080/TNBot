import subprocess
import sys, os
import time

sys.stderr.write("!!!THIS CLI WAS CREATED ONLY FOR QUICK LINUX CONFIGURATION!!!\n")

START_FILE_NAME = "bot.service"
PROMPT = "> "
EXCLUDED_FILES = [".gitkeep"]

menu = (
    "1: run",
    "2: stop",
    "3: status",
    "4: exit",
    "5: clear data folder",
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
        print(r"\ Access denied")
        return
    print("| Enable")
    subprocess.run(["systemctl", "enable", START_FILE_NAME])
    print("| Start")
    subprocess.run(["systemctl", "start", START_FILE_NAME])
    print(r"\ Running success")


def stop():
    #TODO костыль
    is_active =status()
    if not is_active[0]: return
    iex = is_active[1].index("PID: ")
    res = is_active[1][iex:].split()[1]
    print("PPID: " + res)
    subprocess.run(["systemctl", "disable", START_FILE_NAME])
    subprocess.run(["kill", res])
    print(r"\ Stopped process")


def status()->tuple:
    res = subprocess.run(["systemctl", "status", START_FILE_NAME], capture_output=True, text=True)
    if "could not be found" in res.stderr:
        print(r"\ Process isn't running")
        return False, None
    print(r"\ It's running")
    return True, res.stdout

def clear_data_folder():
    #TODO не работает
    print("| Removing old data: ")
    for file in os.listdir("data"):
        f_name = os.path.join("data", file)
        if file in EXCLUDED_FILES:
            print("| " + f_name)
            os.remove(f_name)
    print(r"\ End of deletion")

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
                clear_data_folder()
            case '6':
                cli_help()
            case _:
                print(r"\ Command not found")
                cli_help()


if __name__ == "__main__":
    main()
