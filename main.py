import pyperclip
import time
from datetime import datetime
import os
import sqlite3
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QListWidget, QListWidgetItem
from PyQt6.QtCore import Qt
import sys
from PyQt6.QtCore import QThread, pyqtSignal, Qt



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

class ClipboardApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("clipboard manager")
        self.setGeometry(100,100,600,400)
        create_db()
        centralwidget = QWidget()
        self.setCentralWidget(centralwidget)
        layout = QVBoxLayout()
        centralwidget.setLayout(layout)

        self.history_widget = QListWidget()
        layout.addWidget(self.history_widget)
        self.load_history()

        self.monitor_thread = ClipboardMonitorThread()
        self.monitor_thread.new_content_copied.connect(self.add_item_to_gui_and_db)
        self.monitor_thread.start()


    def add_item_to_gui_and_db(self, content):
        """Receives new content from the monitor thread, saves to DB, and updates GUI."""
        # Save to database
        conn = sqlite3.connect(DB_name)
        cursor = conn.cursor()
        current_time = datetime.now().isoformat()
        try:
            cursor.execute("INSERT INTO history (content, timestamp) VALUES (?, ?)",
                           (content, current_time))
            conn.commit()
        except sqlite3.Error as e:
            print(f"Database error on insert from thread: {e}")
        finally:
            conn.close()

        # Add to GUI (at the top for latest items)
        display_text = f"[{datetime.fromisoformat(current_time).strftime('%H:%M:%S %m-%d')}] {content}"
        list_item = QListWidgetItem(display_text)
        list_item.setData(Qt.ItemDataRole.UserRole, content)
        self.history_list_widget.insertItem(0, list_item) # Insert at the beginning
        self.history_list_widget.scrollToTop() # Ensure latest is visible


    # NEW METHOD to stop the thread when the app quits
    def stop_monitor_thread(self):
        if self.monitor_thread and self.monitor_thread.isRunning():
            self.monitor_thread.stop()
        


    def load_history(self):
        self.history_widget.clear()
        history = get_history()
        for item_id,content,timestamp in history:
             display_text = f"[{datetime.fromisoformat(timestamp).strftime('%H:%M:%S %m-%d')}] {content}"
             list_item = QListWidgetItem(display_text)
             list_item.setData(Qt.ItemDataRole.UserRole,item_id)
             self.history_widget.addItem(list_item)


class ClipboardMonitorThread(QThread):
    new_content_copied = pyqtSignal(str)
    def __init__(self,parent=None):
        super().__init__(parent)
        self._running = True
        self.last_copied = pyperclip.paste()
    def run(self):
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

    def stop(self):
        self._running = False
        
        self.wait()

if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    window = ClipboardApp()
    window.show()
    # clipbord_monitor()
    sys.exit(app.exec())