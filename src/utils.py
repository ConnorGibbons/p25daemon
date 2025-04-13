import os
import shutil
import logging

def move_file(src, dest, remove_src=False):
    try:
        if os.path.exists(src):
            if remove_src:
                shutil.move(src, dest)
            else:
                shutil.copy(src, dest)
            logging.info(f"Moved file from {src} to {dest}")
            return (True, None)
        else:
            return (False, f"Source file {src} does not exist.")
    except Exception as e:
        return (False, e.__str__())

def delete_file(path):
    try:
        if os.path.exists(path):
            os.remove(path)
            logging.info(f"Deleted file {path}")
            return (True, None)
        else:
            return (False, f"File {path} does not exist.")
    except Exception as e:
        return (False, e.__str__())
    
def truncate_file(path):
    try:
        with open(path, 'w') as f:
            f.truncate(0)
        logging.info(f"Truncated file {path}")
        return (True, None)
    except Exception as e:
        return (False, e.__str__())

def make_file_with_contents(path, contents):
    try:
        with open(path, 'w') as f:
            f.write(contents)
        logging.info(f"Created file with contents at {path}")
        return (True, None)
    except Exception as e:
        return (False, e.__str__())
    
def log_error(prefix, result):
    logging.error(f"{prefix}: {result[1]}")