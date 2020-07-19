import queue
from threading import Thread


class MementoQueue:
    def __init__(self, crud_atweet, crud_memento, logger):
        self.__th_atweet = None
        self.__th_memento = None
        self.__qtweets = None
        self.__qmemento = None
        self.__logger = logger
        self.__crud_atweet = crud_atweet
        self.__crud_memento = crud_memento

    '''
    Function to start thread for Memento Fetch
    '''

    def start_db_thread(self, atweets_db, memento_db):
        self.__qtweets = queue.Queue()
        self.__qmemento = queue.Queue()

        if self.__th_atweet is None or not self.__th_atweet.is_alive():
            self.__logger.access_log.debug("__th_atweet created")
            self.__th_atweet = Thread(target=self.__write_atweet_queue, args=(self.__qtweets, atweets_db))
            self.__th_atweet.setDaemon(True)
            self.__th_atweet.setName("ArchiveDatabaseThread")
            self.__th_atweet.start()

        if self.__th_memento is None or not self.__th_memento.is_alive():
            self.__th_memento = Thread(target=self.__write_memento_queue, args=(self.__qmemento, memento_db))
            self.__th_memento.setDaemon(True)
            self.__th_memento.setName("MementoDatabaseThread")
            self.__th_memento.start()
        return self.__qtweets, self.__qmemento

    '''
    Function to write to Archive Tweet Database
    '''

    def __write_atweet_queue(self, qtweet, collection):
        while True:
            item = qtweet.get()
            if item is None:
                break
            self.__crud_atweet.insert_2_db(collection, item)
            qtweet.task_done()

    '''
    Function to write to Memento Database
    '''

    def __write_memento_queue(self, qmemento, collection):
        while True:
            item = qmemento.get()
            if item is None:
                break
            self.__crud_memento.insert_2_db(collection, item)
            qmemento.task_done()
