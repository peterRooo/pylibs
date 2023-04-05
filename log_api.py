import logging
import logging.handlers

# filesize: 单个日志文件的最大大小，单位为M
# filenum: 最多保持多少个文件
def init_logger(level, issave=False, filename='run', filenum=10, filesize=50):
    
    format_str = '%(asctime)s %(levelname)s [%(filename)s:%(lineno)d][%(funcName)s] %(message)s'

    if issave:
        myapp = logging.getLogger()
        myapp.setLevel(logging.INFO)
        formatter = logging.Formatter(format_str)
        max_size = filesize * 1024 * 1024
        filehandler = logging.handlers. RotatingFileHandler(filename+".log", mode='a', maxBytes=max_size, backupCount=filenum, encoding='utf-8')#每 1024Bytes重写一个文件,保留2(backupCount) 个旧文件
        filehandler.setFormatter(formatter)
        myapp.addHandler(filehandler)
    else:
        logging.basicConfig(format=format_str,
                filemode='a',
                level=level)
    
    # # 需要存储日志
    # if issave:
    #     formatter = logging.Formatter(format_str)
    #     # When字段的含义
    #     #“S”: Seconds “M”: Minutes “H”: Hours “D”: Days “W”: Week day (0=Monday) “midnight”: Roll over at midnight
    #     filehandler = logging.handlers.TimedRotatingFileHandler("myapp.log", when='M', interval=1, backupCount=filenum)#每 1(interval) 天(when) 重写1个文件,保留7(backupCount) 个旧文件；when还可以是Y/m/H/M/S
    #     filehandler.suffix = "%Y-%m-%d_%H-%M-%S.log"#设置历史文件 后缀
    #     filehandler.setFormatter(formatter)
    #     logging.getLogger('').addHandler(filehandler)

    
    logging.info(f'init log_level:{level}, issave:{issave}, filename:{filename}')
