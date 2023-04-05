import platform
 
def is_windows():
    if platform.system().lower() == 'windows':
        return True
    return False