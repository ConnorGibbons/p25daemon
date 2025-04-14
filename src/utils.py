import os
import shutil
import logging
import subprocess
import time
import config

def DSDPlus_is_actively_decoding():
    path = os.path.join(config.DSDPLUS_INSTALL_PATH, "DSDPlus.VoiceActive")
    return os.path.exists(path)

def launch_DSDPlus():
    path = os.path.join(config.DSDPLUS_INSTALL_PATH, "DSDPlus.exe")
    args = config.DSDPLUS_LAUNCH_ARGS.split()
    try:
        subprocess.Popen(
            ["cmd", "/c", "start", "", path] + args,
            cwd=config.DSDPLUS_INSTALL_PATH,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            shell=True  # not strictly needed, but safe here
        )
        return (True, None)
    except Exception as e:
        return (False, str(e))
    
def kill_DSDPlus():
    if DSDPlus_is_actively_decoding():
        logging.info("DSDPlus is actively decoding, waiting 30 seconds and trying to kill again.")
        time.sleep(30)
        kill_DSDPlus()
        return
    path = os.path.join(config.DSDPLUS_INSTALL_PATH, "DSDPlus.exe")
    try:
        subprocess.run(["taskkill", "/F", "/IM", os.path.basename(path)], check=True)
        time.sleep(2)
        return (True, None)
    except Exception as e:
        return (False, e.__str__())

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
        with open(path, 'a', encoding = 'utf-8') as f:
            f.write(contents)
        return (True, None)
    except Exception as e:
        return (False, e.__str__())
    
def log_error(prefix, result):
    logging.error(f"{prefix}: {result[1]}")