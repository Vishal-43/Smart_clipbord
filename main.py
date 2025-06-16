import pyperclip
import time
import os


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def clipbord_monitor():
    print("clipbord moniter started")
    lastcopied = pyperclip.paste()

    while True:
        try:
            current_copied = pyperclip.paste()
            if current_copied != lastcopied:
                clear_screen()
                print(f"latest containt is {time.strftime('%H:%M:%S')}")
                print("_"*100)
                print(current_copied)
                print("_"*100)
                
                lastcopied = current_copied
            time.sleep(1)
        except KeyboardInterrupt:
            clear_screen()
            print("\nclipboard moniter stopped")
        except Exception as e:
            clear_screen()
            print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    clipbord_monitor()
    print("Exiting program.")