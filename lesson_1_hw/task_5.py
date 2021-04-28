# Task 5:
# Выполнить пинг веб-ресурсов yandex.ru, youtube.com и преобразовать результаты из
# байтовового в строковый тип на кириллице.

import subprocess

# В моем случае, признаюсь, вывод в кириллице не сработал: выводит строки, а не байты - без проблем, но
# только в латинице.
# Связываю с тем, что у меня mac и виндовые кодировки могут не дать эффекта.
# Буду рад, если подскажите возможное решение.


args_yandex = ["ping", "yandex.ru"]

subproc_ping_ya = subprocess.Popen(args=args_yandex, stdout=subprocess.PIPE)
for line in subproc_ping_ya.stdout:
    line = line.decode("cp866").encode("utf-8")
    print(line.decode("utf-8"))


args_youtube = ["ping", "youtube.com"]

subproc_ping_you = subprocess.Popen(args=args_youtube, stdout=subprocess.PIPE)
for line in subproc_ping_you.stdout:
    line = line.decode("cp1251").encode("utf-8")
    print(line.decode("utf-8"))
