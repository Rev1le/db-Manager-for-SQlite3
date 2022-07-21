import sqlite3
import uuid
import requests


class dbManager():
    dbName = 'dsDB'

    def __init__(self, table_name :str = None, table_fields :dict= None):
        
        if  table_name is None or \
            table_fields is None:
            raise Exception('Введите данные для table_name и table_fields')
        
        self.__connection = sqlite3.connect(self.dbName + '.db')
        self.__cur :Cursor = self.__connection.cursor()
        
        self.table_fields :dict = table_fields
        self.table_name :str = table_name

        fields_sql_request = ""

        for field_name in table_fields.keys():
            fields_sql_request += f"{field_name} {table_fields[field_name]}, "
        
        fields_sql_request = fields_sql_request[:-2]

        execute_sql_requst = f"""CREATE TABLE IF NOT EXISTS {table_name}({fields_sql_request});"""
        print(f"Запрос для создания таблицы {self.table_name}: ",execute_sql_requst)

        self.__cur.execute(execute_sql_requst)
        self.__connection.commit()

    def close_DB(self):
        '''
        Закрывает базу данных
        '''
        self.__connection.close()
 
    def table_column(self):
        '''
        Возвращает columns из таблицы
        '''
        return self.table_fields
    
    def get_unique_value(self, column_name:str):
        self.__cur.execute(f'''SELECT DISTINCT {column_name} FROM {self.table_name}''')
        self.__connection.commit()
        return self.__cur.fetchall()

    def data_entry(self, **kwargs):
        '''
        Отправляет запрос в БД для добавления записи
        '''
        mass_values :list = []

        for key in self.table_fields.keys():
            # При отсутсвии значения длля колонки происходит ошибка
            mass_values.append(kwargs[key])
        
        tmp :str = str("?, " * len(self.table_fields.keys()))[:-2]
        ## Формирование строкуЮ состоящую из ?, для SQl запроса

        try:
            self.__cur.execute(f"INSERT INTO {self.table_name} VALUES({tmp});", mass_values)
        except :
            raise Exception('Введенные данные не соответсвуют столбцам таблицы')
        self.__connection.commit()
    
    #ПЕРЕПИСАТЬ
    def get_data_from_db(self, iter_cur :bool = False, **kwargs):
        try:
            sql_request :Cursor = self.__cur.execute(f"SELECT * FROM {self.table_name}")
            self.__connection.commit()
        except :
            raise Exception('Введенные данные не соответсвуют столбцам таблицы')
        
        if iter_cur:
            return sql_request

        return self.__cur.fetchall()
    

    def get_data_from_db(self, iter_cur :bool = False, **kwargs):
        '''
        Отправляет запрос в БД для получения записи по ключевым значениям
        '''
        
        db_request :str = " ".join([f"{key} = '{kwargs[key]}' AND" for key in kwargs.keys()])[:-4]
        ## Генерирует массив с ключами и значениями,
        ## после чего преобразовывает в массив и удаляет последнее слово  AND
        
        try:
            sql_request :Cursor = self.__cur.execute(f"SELECT * FROM {self.table_name} WHERE {db_request}")
            self.__connection.commit()
        except :
            raise Exception('Введенные данные не соответсвуют столбцам таблицы')

        if iter_cur: return sql_request
        
        return self.__cur.fetchall()

    
    #При формировании новый класс методов, можно делать новые таблицы

    @classmethod
    def MemsDB(ctx):  #, table_fields={"name" : "TEXT", "url" : "TEXT", "id_user" : "INT"}):
        """Данный метод класса отправляет параметры в __init__ класса для создания таблицы с мемами"""
        
        table_name :str = "memSaved"
        
        return ctx(table_name = table_name,\
            table_fields = {"name" : "TEXT", "url" : "TEXT", "id_user" : "INT"})
    

    @classmethod
    def academicDB(ctx):
        table_name :str = "academicSugjects" # ТУПОЕ ГОВНО Sugjects нет такого слово, есть Subjects
        
        return ctx(table_name = table_name,\
            table_fields = {
                "id_user" : "INT NOT NULL", 
                "subject" : "TEXT NOT NULL",
                "url" : "TEXT UNIQUE NOT NULL", 
                "type_work" : "TEXT NOT NULL", 
                "num_work" : "INT NOT NULL",
                "author" : "TEXT",
                "notes" : "TEXT"
                })
