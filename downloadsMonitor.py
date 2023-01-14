import os
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
from datetime import datetime

class ClassifyHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return None
        file_path = event.src_path
        classify_file(file_path)


def classify_file(file_path):
    file_name, file_ext = os.path.splitext(file_path)
    file_ext = file_ext.lower()
    image_exts = ['.jpeg', '.jpg', '.png']
    pdf_exts = ['.pdf']
    script_exts = ['.py', '.js', '.rs']

    if file_ext in image_exts:
        destination = "Images/"
    elif file_ext in pdf_exts:
        destination = "PDFs/"
    elif file_ext in script_exts:
        destination = "Scripts/"
    else:
        print(f"{file_path} has an unsupported file extension.")
        return

    destination_path = os.path.join(destination, file_name + file_ext)
    if os.path.exists(destination_path):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_file_name = f"{file_name} {current_time}{file_ext}"
        destination_path = os.path.join(destination, new_file_name)

    shutil.move(file_path, destination_path)
    print(f'Moved {file_path} to {destination_path}')

downloads_path = "/path/to/Downloads/"

for filename in os.listdir(downloads_path):
    file_path = os.path.join(downloads_path, filename)
    classify_file(file_path)

event_handler = ClassifyHandler()
observer = Observer()
observer.schedule(event_handler, path=downloads_path, recursive=False)
observer.start()

try:
    while True:
        time.sleep(60)
except KeyboardInterrupt:
    observer.stop()
observer.join()