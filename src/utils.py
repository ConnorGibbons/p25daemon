import os
import shutil
import logging

def move_file(src, dest):
    try:
        if os.path.exists(src):
            shutil.move(src, dest)
            return (True, None)
        else:
            return (False, f"Source file {src} does not exist.")
    except Exception as e:
        return (False, e.__str__())


def copy_file(src, dest):
    try:
        if os.path.exists(src):
            shutil.copy(src, dest)
            return (True, None)
        else:
            return (False, f"Source file {src} does not exist.")
    except Exception as e:
        return (False, e.__str__())

def delete_file(path):
    try:
        if os.path.exists(path):
            os.remove(path)
            return (True, None)
        else:
            return (False, f"File {path} does not exist.")
    except Exception as e:
        return (False, e.__str__())
    
def truncate_file(path):
    try:
        with open(path, 'w') as f:
            f.truncate(0)
        return (True, None)
    except Exception as e:
        return (False, e.__str__())

def make_file_with_contents(path, contents):
    try:
        with open(path, 'w', encoding = 'utf-8') as f:
            f.write(contents)
        return (True, None)
    except Exception as e:
        return (False, e.__str__())
    
def log_error(prefix, result):
    logging.error(f"{prefix}: {result[1]}")