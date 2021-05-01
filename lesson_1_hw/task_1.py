# Task_1:

# Каждое из слов «разработка», «сокет», «декоратор» представить в строковом формате и
# проверить тип и содержание соответствующих переменных.
# Затем с помощью онлайн-конвертера преобразовать строковые представление в формат Unicode и
# также проверить тип и содержимое переменных.

w_1 = "разработка"
w_2 = "сокет"
w_3 = "декоратор"

print(w_1, type(w_1))
print(w_2, type(w_2))
print(w_3, type(w_3))

w_1_u = (
    "\u0440\u0430\u0437\u0440\u0430\u0431\u043E\u0442\u043A\u0430"  # разработка
)
w_2_u = "\u0441\u043E\u043A\u0435\u0442"  # сокет
w_3_u = "\u0434\u0435\u043A\u043E\u0440\u0430\u0442\u043E\u0440"  # декоратор

print(w_1_u, type(w_1_u))
print(w_2_u, type(w_2_u))
print(w_3_u, type(w_3_u))

print(w_1 == w_1_u)
print(w_2 == w_2_u)
print(w_3 == w_3_u)