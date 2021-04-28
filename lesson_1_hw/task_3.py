# Task_3:
# Определить, какие из слов «attribute», «класс», «функция», «type» невозможно записать в байтовом типе.

print(b"attribute")
print(b"класс")
print(b"функция")
print(b"type")

# 'класс' и 'функция' - выдает ошибку "SyntaxError: bytes can only contain ASCII literal characters."