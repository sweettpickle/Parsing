import pyodbc
import json
import time
from monitor import Monitor

m = Monitor({"id_and_picture.json", "id_and_text.json", "id_and_link.json"})

#mySQLServer = "LAPTOP-KR7NAT1J"  # Никита
# mySQLServer = "DESKTOP-VUVSNTH"  # НикитаP
mySQLServer = "DESKTOP-SMA2M6N"  # Даша
DataBase = "Barsing"
driver = "{SQL Server}"

connection = pyodbc.connect('Driver=' + driver + ';'
                                                 'Server=' + mySQLServer + ';'                                                                           
                                                                           'DataBase=' + DataBase + ';')

cursor = connection.cursor()  # подключение


def insert(table, in_boof):
    cursor.executemany("insert into boof values (?, ?);", in_boof)
    cursor.execute("select id_post, data FROM boof WHERE boof.id_post NOT IN (SELECT id_post  FROM " + table + ")")
    results = cursor.fetchall()  # возвращает список! []
    cursor.execute("truncate table boof")
    add = tuple(results)

    if add:
        cursor.executemany("insert into " + table + " values (?, ?);", add)
        print("Новые записи добавлены в таблицу " + table)
    else:
        print("Новых записей нет. В таблицу " + table + " ничего не добавлено")

    cursor.execute("truncate table boof")
    connection.commit()


def text_json(file_name, table):
    try:
        m.monitor_close('BDReader', file_name)  # ставит метку что файл открыт на чтение
        ola = open(file_name, 'r+')
        from_json = json.loads(json.load(ola))
        ola.close()
        m.monitor_open(file_name)  # ставит метку что файл освободился и любой поток может получить к нему доступ
    except FileNotFoundError:
        m.monitor_open(file_name)
        print('Джисон файлы не найдены. Попробуйте заново')
        return 0
  
    mas = []
    for k, v in from_json.items():
        val = str(v)
        k_val = (k, val)
        mas.append(k_val)
    new_data = tuple(mas)
    insert(table, new_data)


def links_and_pic_json(file_name, table):
    try:
        m.monitor_close('BDReader', file_name)
        ola = open(file_name, 'r+')
        from_json = json.loads(json.load(ola))
        ola.close()
        m.monitor_open(file_name)
    except FileNotFoundError:
        m.monitor_open(file_name)
        print('Джисон файлы не найдены. Попробуйте заново')
        return 0

    mas = []
    for k, v in from_json.items():
        for one in v:
            k_val = (k, one)
            mas.append(k_val)
    new_data = tuple(mas)
    insert(table, new_data)


print('Запись в базу данных началась...')
# time.sleep(5)

while __name__ == "__main__":
    time.sleep(1)
    try:
        text_json('id_and_text.json', 'posts')
        links_and_pic_json('id_and_link.json', 'links')
        links_and_pic_json('id_and_picture.json', 'pictures')
    except pyodbc.DatabaseError:
        print('Ошибка при записи в БД!!!')
        

connection.close()
cursor.close()
print("""Выполнение программы закончено.""")


