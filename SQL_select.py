import pyodbc


#mySQLServer = "LAPTOP-KR7NAT1J"  # Никита
# mySQLServer = "DESKTOP-VUVSNTH"  # НикитаP
mySQLServer = "DESKTOP-SMA2M6N"  # Даша
DataBase = "Barsing"
driver = "{SQL Server}"

connection = pyodbc.connect('Driver=' + driver + ';'
                                                 'Server=' + mySQLServer + ';'
                                                                           'DataBase=' + DataBase + ';')
cursor = connection.cursor()  # подключение


if __name__ == "__main__":
    working = True
    while working:
        try:
            N = int(input("""Какие данные необходимо вывести ? 
Текст, ссылки или картинки ?
Введите цифру от 1 до 3 соотвественно.
***Для очистки всех бд нажмите 0.\n"""))
        except ValueError:
            print('Попробуйте снова: \n ')
            N = int(input())

        if N == 1:
            cursor.execute(""" select *
            from posts
            order by id""")
            results = cursor.fetchall()
            for i in results:
                print(i)
            print('Все данные выведены.\n')

        elif N == 2:
            cursor.execute(""" select *
                    from links
                    order by id""")
            results = cursor.fetchall()
            for i in results:
                print(i)
            print('Все данные выведены.\n')

        elif N == 3:
            cursor.execute(""" select *
                    from pictures
                    order by id""")
            results1 = cursor.fetchall()
            for i in results1:
                print(i)
            print('Все данные выведены.\n')
        elif N == 0:
            cursor.execute("""truncate table posts""")
            cursor.execute("""truncate table links""")
            cursor.execute("""truncate table pictures""")
            connection.commit()
            print("Таблицы очищены.\n")
        else:
            print('Вы ввели неверное число. Попробуйте снова. \n')
        working = int(input('Для выхода нажмите 0. Если хотите продолжить - любую цифру.\n'))
