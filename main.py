import pyperclip
import time
import os
import sqlite3

DB_name = "clipboard.db"
def create_db():
    conn = sqlite3.connect(DB_name)
    cursor = conn.cursor()
    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS clipboard_history(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        content TEXT NOT NULL,
                        timestamp TEXT NOT NULL);
                  ''')
    conn.commit()
    conn.close()
    print("database is created sucessfully")

def save_history(content):
    conn = sqlite3.connect(DB_name)
    cursor = conn.cursor()
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('''
                    INSERT INTO clipboard_history(content,timestamp)
                   values(?,?) ''',(content,timestamp))
    conn.commit()
    conn.close()
    print("history save sucessfully")

def get_history():
    conn = sqlite3.connect(DB_name)
    cursor = conn.cursor()
    cursor.execute(''' 
                    SELECT * FROM clipboard_history
                    ORDER BY timestamp ;
                  
                  ''')
    
    history = cursor.fetchall()
    conn.close()
    return history

def print_history():
    history = get_history()
    if not history:
        print("No history found.")
    else:
        while history:
            entry = history.pop(0)
            print(f"ID: {entry[0]}, Content: {entry[1]}, Timestamp: {entry[2]}")
            print("-" * 100)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def clipbord_monitor():
    print("clipbord moniter started")
    lastcopied = pyperclip.paste()

    while True:
        try:
            current_copied = pyperclip.paste()

            if current_copied != lastcopied:
                save_history(current_copied)
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
            break
        except Exception as e:
            clear_screen()
            print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    create_db()

    clipbord_monitor()
    clear_screen()
    print_history()

    print("Exiting program.")