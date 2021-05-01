# Task 6:
# Создать текстовый файл test_file.txt, заполнить его тремя строками: «сетевое программирование», «сокет», «декоратор».
# Проверить кодировку файла по умолчанию.
# Принудительно открыть файл в формате Unicode и вывести его содержимое.

import locale

words = ["сетевое программирование", "сокет", "декоратор"]

file = open("lesson_1_hw/test_file.txt", "w")
for word in words:
    file.write(word + "\n")

file_cod = locale.getpreferredencoding("lesson_1_hw/test_file.txt")
print(file_cod)  # UTF-8

file = open("lesson_1_hw/test_file.txt", "r", encoding="utf-8")
for line in file:
    print(line)

file.close()
