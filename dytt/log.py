'''
Created on 2018年11月24日

@author: Administrator
'''
import logging;

class Log(object):
    '''
    日志模块
    '''

    def __init__(self):
        self._logger = logging.getLogger('MovieCrane_Log')
        self._logger.setLevel(level=logging.INFO)
        handler = logging.FileHandler("log.txt", encoding='utf-8')
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self._logger.addHandler(handler)
        
    def debug(self, msg):
        self._logger.debug(msg)
        
    def info(self, msg):
        self._logger.info(msg)
    
    def error(self, msg):
        self._logger.error(msg)
