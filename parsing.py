from selenium import webdriver
import time, json, threading, os
from selenium.webdriver.common.keys import Keys
from monitor import Monitor
import selenium

# os.startfile(r'SQL_insert.py')

m = Monitor({"id_and_picture.json", "id_and_text.json", "id_and_link.json"})

print("Идет открытие браузера")
driver = webdriver.Chrome()
driver.get("http://www.vk.com")

driver.find_element_by_id("index_email").send_keys("79670595561")  # выбираем поле логина в вводим логин
driver.find_element_by_id("index_pass").send_keys("immoth")  # выбираем поле пароля и вводим его
driver.find_element_by_id("index_login_button").send_keys(Keys.ENTER)  # кнопка "вход" и клик по ней
time.sleep(1)  # выжидаем время, пока прогрузится страница
print("Вход на сайт выполнен")
print("Ждем, пока прогрузится страница\n")


try:
    for i in range(2):
        driver.find_element_by_id("show_more_link").click()  # три раза прокручиваем новости
        time.sleep(1)  # ждем, пока прогрузится страница
    time.sleep(2)
except selenium.common.exceptions.WebDriverException:
    print("Ошибка при прокрутке")


# нажатие всех кнопок показать полностью
driver.execute_script(""" 
bt = document.getElementsByClassName('wall_post_more');
btLen = bt.length;
for(i = 0; i < btLen; i++){bt[i].click();}""")

all_posts = driver.find_elements_by_class_name("post")  # после фид_роу(обертка поста), класс, в котором наход id поста


def json_write(data, fp):
    try:
        f = open(fp, "r")  # открываем файл на чтение
        from_json = json.loads(json.load(f))  # выгружаем старые данные и кодируем в формат python
        f.close()

        from_json.update(data)  # формируем новый словарь с новыми данными
        f = open(fp, 'w')  # открываем файл на запись
        json.dump(json.dumps(from_json), f)  # загружаем старые+новые данные
        f.close()
    except FileNotFoundError:  # если файл создается впервые
        f = open(fp, 'w')  # то создаем его на запись
        json.dump(json.dumps(data), f, indent=2)  # и загружаем новые данные
        f.close()


def process_1():
    print("Запись изображений в файл началась")
    fp = "id_and_picture.json"
    to_json = {}
    counter = 0
    for post11 in all_posts:
        id_post = post11.get_attribute('id')  # получаем айди поста из атрибута в коде страницы
        picture = post11.find_elements_by_class_name("page_post_thumb_wrap")  # класс c ссылками на картинки

        if not id_post:
            id_post = "У поста нет id"

        mas_picture = []  # лист либо создается, либо очищается
        for post12 in picture:
            mas_picture.append(post12.value_of_css_property('background-image'))

        if not mas_picture:
            mas_picture = ["Отсутсвуют изображения"]

        to_json.update({id_post: mas_picture})
        counter += 1

        if not (counter % 10):
            m.monitor_close(pr1.name, fp)  # ставит метку что файл открыт на чтение
            json_write(to_json, fp)
            m.monitor_open(fp)  # ставит метку что файл освободился и любой поток может получить к нему доступ
            to_json = {}


def process_2():
    print("Запись текста в файл началась")
    fp = "id_and_text.json"
    to_json = {}
    counter = 0

    for post21 in all_posts:
        id_post = post21.get_attribute('id')  # получаем айди поста из атрибута в коде страницы
        teeext = post21.find_elements_by_class_name("wall_post_text")  # класс с текстом поста

        if not id_post:
            id_post = "У поста нет id"

        if not teeext:  # если нет текста
            teeext = ['not text']
        else:
            teeext = [teeext[0].text]  # выводим весь текст в посте

        to_json.update({id_post: teeext})
        counter += 1

        if not (counter % 10):
            m.monitor_close(pr2.name, fp)
            json_write(to_json, fp)
            m.monitor_open(fp)


def process_3():
    print("Запись внешних ссылок в файл началась\n")
    fp = "id_and_link.json"
    to_json = {}
    counter = 0

    for post31 in all_posts:
        id_post = post31.get_attribute('id')  # получаем айди поста из атрибута в коде страницы
        teeext = post31.find_elements_by_class_name("wall_post_text")
        if not id_post:
            id_post = "У поста нет id"

        mas_links = []
        if len(teeext) != 0:
            links = teeext[0].find_elements_by_partial_link_text("/")  # класс, в котором находится текст поста
            links += (teeext[0].find_elements_by_partial_link_text("#"))  # класс, в котором находится текст поста

            for l in links:
                to_append = l.text
                mas_links.append(to_append)

        if len(mas_links) == 0:
            mas_links.append('not links and hashtag')

        to_json.update({id_post: mas_links})
        counter += 1

        if not (counter % 10):
            m.monitor_close(pr3.name, fp)
            json_write(to_json, fp)
            m.monitor_open(fp)
            to_json = {}


iimg = 0
itext = 0
ilink = 0
play = True


def simple_reader():
    print("Процесс считывания и вывод в консоль начался")
    global play
    while play:
        json_reader("id_and_picture.json")
        json_reader("id_and_text.json")
        json_reader("id_and_link.json")


def json_reader(fn):
    global iimg
    global itext
    global ilink
    if fn == "id_and_picture.json":
        n = iimg
    if fn == "id_and_text.json":
        n = itext
    if fn == "id_and_link.json":
        n = ilink

    try:
        file = open(fn, 'r', encoding="UTF-8")
    except FileNotFoundError:
        time.sleep(0.01)
        return 0
    m.monitor_close("reader <-", fn)

    lst = list(json.loads(json.load(file)).items())
    file.close()
    time.sleep(0.1)

    m.monitor_open(fn)
    run = len(lst)

    if n+1 < run:
        for i in range(n+1, run):
            print(lst[i])

        if fn == "id_and_picture.json":
            iimg = run  
        if fn == "id_and_text.json":
            itext = run
        if fn == "id_and_link.json":
            ilink = run


start = time.time()

pr1 = threading.Thread(target=process_1, name='picture')
pr2 = threading.Thread(target=process_2, name='text')
pr3 = threading.Thread(target=process_3, name='links')
pr4 = threading.Thread(target=simple_reader, name='reader')

pr1.start()
pr2.start()
pr3.start()
pr4.start()

pr1.join()
pr2.join()
pr3.join()


time.sleep(2)
play = False
pr4.join()
driver.quit()
print("\nПарсинг закончен")
print("Браузер закрыт")
print("Время работы составило: ", (time.time() - start))


