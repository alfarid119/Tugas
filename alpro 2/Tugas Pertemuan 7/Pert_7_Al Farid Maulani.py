#indexing text
#angka = [10, 20, 30, 40, 50]
#print(angka[0])   # elemen pertama
#print(angka[4])   # elemen kelima

#megakses isi list
#buah = ["apel", "jeruk", "mangga"]
#for item in buah:
    #print(item)

#fungsi Len()
#buah = ["apel", "jeruk", "mangga"]
#print(len(buah))

#menghapus elemen dalam list
#angka = [1, 2, 3, 4, 5]
#del angka[2]
#print(angka)

#negative indexing
#angka = [10, 20, 30, 40, 50]
#print(angka[-1])   # elemen terakhir
#print(angka[-2])   # elemen kedua terakhir

#kuis 19
#topi_list = [1, 2, 3, 4, 5]  # Angka yang tersembunyi di dalam topi pesulap

# Langkah 1: Meminta user memasukkan angka integer untuk mengganti nilai tengah
#topi_list[len(topi_list)//2] = int(input("Masukkan angka untuk mengganti nilai tengah: "))

# Langkah 2: Menghapus elemen terakhir pada list
#topi_list.pop()

# Langkah 3: Menampilkan panjang dari list
#print("Panjang list:", len(topi_list))

#print("Isi list:", topi_list)


#append() dan insert()
#angka = [1, 2, 3]
#angka.append(4)
#angka.insert(1, 10)
#print(angka)

#contoh 2 penggunaan insert() dengan list
#my_list = []
#for i in range(5):
    #my_list.insert(0, i + 1)
#print(my_list)


#contoh 2 penggunaan append() dengan list
#my_list = []
#for i in range(5):
    #my_list.append(i + 1)
#print(my_list)

#use list contoh 1
#my_list = [15, 1, 2, 3, 4]
#total = 0

#for i in range(len(my_list)):
    #total += my_list[i]

#print(total)

#use list contoh 2
#my_list = [15, 1, 2, 3, 4]
#total = 0
#for i in my_list:
    #total += i
#print(total)

#list in action 2
#my_list = [1, 2, 3, 4, 5]
#for i in range(len(my_list)):
    #my_list[i] = my_list[i] * 2
#print(my_list)


#kuis 20
#exo = []  # Langkah 1: list kosong

# Langkah 2: append anggota awal
#exo.append("Suho")
#exo.append("Kai")
#exo.append("Chanyeol")
#exo.append("Sehun")
#print("Langkah 2:", exo)

# Langkah 3: for loop menambahkan anggota lain
#for anggota in ["DO", "Baekhyun", "Kris", "Lay", "Luhan", "Tao", "Chen"]:
    #exo.append(anggota)
#print("Langkah 3:", exo)

# Langkah 4: hapus Kris, Luhan, Tao
#exo.remove("Kris")
#exo.remove("Luhan")
#exo.remove("Tao")
#print("Langkah 4:", exo)

# Langkah 5: insert Xiumin di posisi ke-3 dari terakhir
#exo.insert(len(exo)-3, "Xiumin")
#print("Langkah 5:", exo)

#print("Jumlah anggota exo:", len(exo))
