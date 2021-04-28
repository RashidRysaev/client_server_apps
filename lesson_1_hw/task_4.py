# Task 4:
# Преобразовать слова «разработка», «администрирование», «protocol», «standard»
# из строкового представления в байтовое и выполнить обратное преобразование (используя методы encode и decode)

w_1 = "разработка"
w_1_enc = str.encode(w_1, encoding="utf-8")
print(w_1_enc)

w_1_dec = bytes.decode(w_1_enc, encoding="utf-8")
print(w_1_dec)


w_2 = "администрирование"
w_2_enc = str.encode(w_2, encoding="utf-8")
print(w_2_enc)

w_2_dec = bytes.decode(w_2_enc, encoding="utf-8")
print(w_2_dec)


w_3 = "protocol"
w_3_enc = str.encode(w_3, encoding="utf-8")
print(w_3_enc)

w_3_dec = bytes.decode(w_3_enc, encoding="utf-8")
print(w_3_dec)


w_4 = "standard"
w_4_enc = str.encode(w_4, encoding="utf-8")
print(w_4_enc)

w_4_dec = bytes.decode(w_4_enc, encoding="utf-8")
print(w_4_dec)
