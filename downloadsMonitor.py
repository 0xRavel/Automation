import os
import shutil
import time
from datetime import datetime
from typing import Optional

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

class ClassifyHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            file_path = event.src_path
            classify_file(file_path)


def classify_file(file_path: str) -> None:
    file_name, file_ext = os.path.splitext(file_path)
    file_ext = file_ext.lower()
    destination = get_destination_folder(file_ext)

    if not destination:
        print(f"{file_path} has an unsupported file extension.")
        return

    destination_path = os.path.join(destination, os.path.basename(file_path))
    destination_path = check_destination_path(destination_path)
    shutil.move(file_path, destination_path)
    print(f'Moved {file_path} to {destination_path}')


def get_destination_folder(file_ext: str) -> Optional[str]:
    image_exts = ['.jpeg', '.jpg', '.png']
    pdf_exts = ['.pdf']
    script_exts = ['.py', '.js', '.rs']

    if file_ext in image_exts:
        return "Images/"
    elif file_ext in pdf_exts:
        return "PDFs/"
    elif file_ext in script_exts:
        return "Scripts/"
    else:
        return None


def check_destination_path(destination_path: str) -> str:
    if os.path.exists(destination_path):
        file_name, file_ext = os.path.splitext(destination_path)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"{file_name} {current_time}{file_ext}"
    return destination_path


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
