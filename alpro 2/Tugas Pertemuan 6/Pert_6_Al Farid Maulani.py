from collections import Counter #memanggil library Counter untuk menghitung frekuensi elemen dalam sebuah iterable

#1. kondisi While True
#c = Counter()
#i = 8

#while True:
#    c['looping'] += 1
#    print("Angka ke -", i)
 #   i += 1

 #   if i > 7:   # berhenti setelah 7 kali
 #       break

#print(c)

#2. kondisi While dengan argumen
#c = Counter()
#i = 3

#while i <= 5:   # berhenti setelah 5 kali
#    c['jumlah looping'] += 1
#    print("Angka ke -", i)
#    i += 1

#print(c)

# mencari dan menghitung jumlah angka genap gannjil dengan while


# membaca angka pertama
#from collections import Counter
#c = Counter()
#i = 1
#while i <= 10:
    #c['looping'] += 1
    #if i % 2 == 0:
        #c['genap'] += 1
    #else:
        #c['ganjil'] += 1
    #i += 1

#print(c)


#Kuis 15
#from collections import Counter

#secret_number = 8
#c = Counter()

#print("Youkoso! Selamat datang di permainan tebak angka. Saya sudah memilih sebuah angka rahasia antara 1 dan 10. Bisakah kamu menebaknya?")

#tebakan = int(input("Masukkan tebakanmu: "))

#while tebakan <= 20:   # loop berjalan selama tebakan valid
    #c['jumlah percobaan'] += 1   # hitung jumlah percobaan

    #if tebakan == secret_number:
        #print("Selamat, Muggle! kamu bebas sekarang!")
        #break
    #else:
        #print("ahihihihi! kamu nyangkut deh di Loop saya")

 #   tebakan = int(input("Masukkan tebakanmu: "))

#print("Total jumlah percobaan:", c['jumlah percobaan'])

# Membandingkan 5 contoh range()

#print("=== Contoh 1 ===")
#for a in range(10):
    #print("nilai a saat ini adalah", a)

#print("\n=== Contoh 2 ===")
#for b in range(2, 8):
    #print("nilai b saat ini adalah", b)

#print("\n=== Contoh 3 ===")
#for c in range(2, 8, 3):
    #print("nilai c saat ini adalah", c)

#print("\n=== Contoh 4 ===")
#for d in range(1, 1):
    #print("nilai d saat ini adalah", d)

#print("\n=== Contoh 5 ===")
#for e in range(2, 1):
    #print("nilai e saat ini adalah", e)

# menghitung 2 pangkat 0 sampai 10 menggunakan for loop   
#power = 1
#for expo in range(11):
    #print("2 pangkat ", expo, " adalah ", power)
    #power *= 2

#break and continue dalam for loop
# Contoh penggunaan break dan continue dengan while loop

#i = 0
#while i < 10:
    #i += 1
    
    # Jika i sama dengan 5, lewati iterasi ini (continue)
    #if i == 5:
        #print("Lewati angka 5")
        continue
    
    # Jika i sama dengan 8, hentikan loop (break)
    #if i == 8:
        #print("Loop berhenti di angka 8")
        #break
    
    #print("Angka:", i)

#print("Selesai looping")


# kuis 16
#import random

#angka_list = list(range(1, 21))   # buat list angka 1 sampai 20
#rahasia = random.choice(angka_list)  # pilih satu elemen acak dari list

#print("Game Tebak Angka (choice)")
#while True:
    #tebakan = int(input("Masukkan tebakanmu: "))
    #if tebakan == rahasia:
        #print("Benar! Angka rahasia adalah", rahasia)
        #break
    #elif tebakan < rahasia:
        #print("Terlalu kecil!")
    #else:
        #print("Terlalu besar!")


# kuis 17
# Meminta user memasukkan kata
#user_input = input("Masukkan sebuah kata: ")

# Ubah ke huruf kapital
#user_input = user_input.upper()

# Loop setiap huruf
#for kata in user_input:
    # Jika huruf adalah vokal, lewati
    #if kata in ["A", "I", "U", "E", "O"]:
        #continue
    #else:
        # Cetak huruf konsonan
        #print(kata)

# while dengan else
#i = 1
#while i < 4:
    #print("looping ke-", i)
    #i += 1
#else:
    #print("Loop selesai")


#for dengan else

#for j in range(5, 10):
    #print("looping ke-", j)
#else:
    #print("Loop selesai")

#logika informatika
#p = True
#q = False

#print(not (p and q))   # True
#print((not p) or (not q))  # True

#print(not (p or q))    # False
#print((not p) and (not q)) # False

#perbandingan logical dan bitwise
x = 6   # biner: 00000110
y = 3   # biner: 00000011

# Logical
#print("Logical AND:", x and y)   # keduanya True → hasil y
#print("Logical OR:", x or y)     # salah satu True → hasil x

# Bitwise
#print("Bitwise AND:", x & y)     # 00000110 & 00000011 = 00000010 → 2
#print("Bitwise OR:", x | y)      # 00000110 | 00000011 = 00000111 → 7
#print("Bitwise XOR:", x ^ y)     # 00000110 ^ 00000011 = 00000101 → 5
#print("Bitwise NOT x:", ~x)      # membalik bit → -7


#var = int(input("Masukkan angka: "))  
#var_right = var >> 1  # geser ke kanan 1 bit
#var_left = var << 3   # geser ke kiri 3 bit
#print(var_right, var_left)

##kuis 18
#x = 4   
#y = 1   

#a = x & y   # AND
#b = x | y   # OR
#c = ~x      # NOT (komplemen)
#d = x ^ 5   # XOR
#e = x >> 2  # shift kanan
#f = x << 2  # shift kiri

#print(a, b, c, d, e, f)
