# 1
#def penjumlahan(x):
    #bilangan = 7
    #return x + 7

#print(penjumlahan(4))
#print(bilangan)  # Ini akan error karena 'bilangan' bersifat lokal

# 2
# Contoh 1
#bilangan = 2
#def perkalian_bilangan(x):
    #return x * bilangan

#print(perkalian_bilangan(7))  # Output: 14

# Contoh 2
#def perkalian_bilangan(x):
    #bilangan = 5
    #return x * bilangan

#print(perkalian_bilangan(7))  # Output: 35

# Contoh 3
#def perkalian_bilangan(x):
    #bilangan = 7
    #return x * bilangan

#bilangan = 3
#print(perkalian_bilangan(7))  # Output: 49

# 3
#bilangan = 2
#print(bilangan)

#def return_bilangan():
    #global bilangan
    #bilangan = 5
    #return bilangan

#print(return_bilangan())  # Output: 5
#print(bilangan)           # Output: 5 (karena global)

# 4
#x = 10  # variable global

#def hitung():
    #global x  # deklarasi bahwa x yang dimaksud adalah x global
    #x = 20    # mengubah nilai x global
    #print("Nilai x di dalam fungsi:", x)

#hitung()
#print("Nilai x di luar fungsi:", x)

#5
#def hitung_imt(berat, tinggi):
    #imt = berat / (tinggi * tinggi)
    #return imt

#berat = float(input("Masukkan berat badan (kg): "))
#tinggi = float(input("Masukkan tinggi badan (m): "))

#index_massa_tubuh = hitung_imt(berat, tinggi)
#kategori = ["Normal", "Gemuk", "Obesitas"]

#if 18.5 <= index_massa_tubuh <= 25.0:
    #print("IMT:", index_massa_tubuh, "- Kategori:", kategori[0])
#elif 25.0 < index_massa_tubuh <= 27.0:
    #print("IMT:", index_massa_tubuh, "- Kategori:", kategori[1])
#else:
    #print("IMT:", index_massa_tubuh, "- Kategori:", kategori[2], ". Anda harus diet!")

#6
#def luas_segitiga(alas, tinggi):
    #luas = 0.5 * alas * tinggi
    #return luas

#a = float(input("Masukkan alas: "))
#t = float(input("Masukkan tinggi: "))
#print("Luas segitiga:", luas_segitiga(a, t))

#7
#def luas_segitiga(alas, tinggi=5):  # tinggi punya nilai default
    #luas = 0.5 * alas * tinggi
    #return luas

#print("Luas (alas=6):", luas_segitiga(6))          # pakai default tinggi=5
#print("Luas (alas=6, tinggi=4):", luas_segitiga(6, 4))  # override tinggi

#8
#def luas_segitiga(alas, tinggi):
    #return 0.5 * alas * tinggi

#def keliling_segitiga(a, b, c):
    #return a + b + c

#alas = float(input("Alas: "))
#tinggi = float(input("Tinggi: "))
#sisi_a = float(input("Sisi a: "))
#sisi_b = float(input("Sisi b: "))
#sisi_c = float(input("Sisi c: "))

#print("Luas:", luas_segitiga(alas, tinggi))
#print("Keliling:", keliling_segitiga(sisi_a, sisi_b, sisi_c))

#9
#def faktorial(n):
    #if n < 0:
        #return None
    #if n < 2:
        #return 1

    #hasil = 1
    #for i in range(2, n + 1):
        #hasil = hasil * i
    #return hasil

#n = int(input("Masukkan nilai yang ingin di faktorial: "))
#print(n, "! =", faktorial(n))

#10
def fibonacci(n):
    if n < 1:
        return None
    if n < 3:
        return 1

    elem_1 = elem_2 = 1
    hasil_jumlah = 0
    for i in range(n - 2):
        hasil_jumlah = elem_1 + elem_2
        elem_1 = elem_2
        elem_2 = hasil_jumlah
    return hasil_jumlah

for n in range(1, 10):
    print(n, "->", fibonacci(n))
    
#11
#def faktorial(n):
    #if n == 0 or n == 1:  # base case
        #return 1
    #else:
        #return n * faktorial(n - 1)  # recursive case

#n = int(input("Masukkan bilangan: "))
#print(f"Faktorial dari {n} adalah: {faktorial(n)}")

#12
#def fibonacci(n):
    #if n == 0:      # base case 1
        #return 0
    #elif n == 1:    # base case 2
        #return 1
    #else:
        #return fibonacci(n - 1) + fibonacci(n - 2)  # recursive case

#n = int(input("Masukkan n: "))
#print(f"Fibonacci ke-{n} adalah: {fibonacci(n)}")