# membuat fungsi input
#nama = input("Masukkan nama: ") 
#21print("Halo,", nama)

# membuat fungsi input dengan tambahan argumen
#usia = input("Masukkan usia Anda: ")
#print("Usia Anda adalah", usia, "tahun")

#
#angka = input("Masukkan angka: ")
#print("Tipe data dari input adalah:", type(angka))

# Mengkonversi tipe data 1: Membuat konversi tipe data float pada fungsi input
#nilai = float(input("Masukkan nilai desimal: "))
#print("Nilai yang dimasukkan:", nilai)

#5.	Mengkonversi tipe data 2: Membuat program untuk menghitung sisi miring segitiga dengan variable hypo untuk menampung hasil rumus pitagoras
#import math
#a = float(input("Masukkan sisi a: "))
#b = float(input("Masukkan sisi b: "))
#hypo = math.sqrt(a**2 + b**2)
#print("Sisi miring segitiga adalah:", hypo)

# Mengkonversi tipe data 2: Membuat program untuk menghitung sisi miring segitiga tanpa membuat variable untuk menampung hasil operasi
#import math
#a = float(input("Masukkan sisi a: "))
#b = float(input("Masukkan sisi b: "))
#print("Sisi miring segitiga adalah:", math.sqrt(a**2 + b**2))

# operator kokutensi
#nama_depan = "Al"
#nama_belakang = "Farid"
#print(nama_depan + " " + nama_belakang)

# operator replikasi
#kata = "Python "
#print(kata * 3)

# Mengkonversi Tipe data 3: konversi ke string 
#angka = 123
#print("Angka dalam string:", str(angka))

# melihat tipe data suatu variable
#x = 10
#print(type(x))
#y = "Halo"
# print(type(y))

# Kuis 7
# menerima input dari user
#a = int(input("Masukkan nilai a: "))
#b = int(input("Masukkan nilai b: "))

# operasi matematika
#print("Hasil penjumlahan:", a + b)
#print("Hasil pengurangan:", a - b)
#print("Hasil pembagian:", a / b)
#print("Hasil perkalian:", a * b)

# kalimat motivasi
#print("Selamat kamu sudah pintar matematika")

# kuis 8 dengan pembulatan
# menerima input dari user
#x = float(input("Masukkan nilai x: "))

# menghitung persamaan
#y = 1.0 / (x + (1.0 / (x + (1.0 / (x + (1.0 / x))))))

# menampilkan hasil asli
#print("Hasil y (asli):", y)

# menampilkan hasil dibulatkan ke 2 angka desimal
#print("Hasil y (dibulatkan 2 desimal):", round(y, 2))

# kuis 9
# input dari user
jam = int(input("Waktu mulai (jam): "))
menit = int(input("Waktu mulai (menit): "))
durasi = int(input("Durasi acara (menit): "))

# hitung total menit dari waktu mulai
total_menit = jam * 60 + menit

# tambahkan durasi
total_menit += durasi

# konversi kembali ke jam dan menit
jam_selesai = total_menit // 60
menit_selesai = total_menit % 60

# tampilkan hasil
print("Acara selesai pada pukul:", jam_selesai, ":", menit_selesai)
