import time
import platform
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import os

def folder_for_file(fPath):
    return os.path.basename(os.path.dirname(fPath))

def on_create_ht3_file(self):
    print(f'Sub detect: {self.src_path}')

    file_dir = os.path.dirname(self.src_path)

    file_name = os.path.basename(self.src_path)

def track_ht3_folder(dir):

    # function tracking dir in which folders will be created
    global tracked_locs
    tracked_locs = dict()

    # track only ht3 files in the folder
    patterns = ['*.ht3']
    ignore_patterns = None
    ignore_dirs = True
    case_sensitive = True
    event_handler = PatternMatchingEventHandler(None, ignore_patterns, ignore_dirs, case_sensitive)


    event_handler.on_created = on_create_ht3_file

    go_recursively = True
    my_observer = Observer()
    my_observer.schedule(event_handler, dir, recursive=go_recursively)

    my_observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        my_observer.stop()
        my_observer.join()


if __name__ == '__main__':

    # init folder
    root_dir = '/Users/philipp/Desktop/Work/WHK Schlierf Group/smFRET_Software/speed_tests/eval_folder'
    track_ht3_folder(root_dir)