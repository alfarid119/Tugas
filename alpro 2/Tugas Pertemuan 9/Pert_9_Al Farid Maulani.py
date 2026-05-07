# 1
#my_list = [8, 10, 6, 2, 4] # list untuk diurutkan
#swapped = True # Inisiasi awal, untuk memasuki loop

#while swapped:
    #swapped = False # Untuk mengindikasi bahwa tidak ada proses penukaran elemen
    #for i in range(len(my_list) - 1): # Melakukan perulangan sepanjang banyaknya elemen dikurang 1
       #if my_list[i] > my_list[i + 1]: # Membandingkan elemen saat ini dengan elemen di depannya
            #swapped = True # Akan ada proses penukaran
            #my_list[i], my_list[i + 1] = my_list[i + 1], my_list[i] # Proses penukaran

#print(my_list)

# 2
#my_list = []
#swapped = True
#num = int(input("Masukkan panjang elemen list yang akan diurutkan: "))

#for i in range(num):
#    val = float(input("Masukkan elemen list: "))
#    my_list.append(val)

#while swapped:
#    swapped = False
#    for i in range(len(my_list) - 1):
#        if my_list[i] > my_list[i + 1]:
#            swapped = True
#            my_list[i], my_list[i + 1] = my_list[i + 1], my_list[i]

#print("\nSorted:")
#print(my_list)


# 3
#data = [5, 2, 9, 1, 5, 6]
#data.sort()
#print(data)

# 4
#data = [1, 2, 3, 4, 5]
#data.reverse()
#print(data)

# 5
#list_1 = [1]
#list_2 = list_1
#list_1[0] = 2
#print(list_2)

# 6
#data = [10, 20, 30, 40, 50, 60]
#print(data[0:4])   # [10, 20, 30, 40]

# 7
data = [10, 20, 30, 40, 50, 60]

# Ambil elemen dari indeks 1 sampai sebelum indeks 4
print(data[1:4])   # [20, 30, 40]

# Ambil elemen dari indeks 2 sampai akhir
print(data[2:])    # [30, 40, 50, 60]

# 8
# Ambil 3 elemen terakhir
#print(data[-3:])   # [40, 50, 60]

# Ambil dari indeks -5 sampai sebelum -2
#print(data[-5:-2]) # [20, 30, 40]

# 9
#data = [10, 20, 30, 40, 50, 60]

# Ambil dari indeks 0 sampai sebelum indeks 3
#print(data[0:3])   # [10, 20, 30]

# Ambil dari indeks 2 sampai sebelum indeks 5
#print(data[2:5])   # [30, 40, 50]

#10
#data = [10, 20, 30, 40, 50, 60]
#print(data[3:])    # [40, 50, 60]

#11
#data = [10, 20, 30, 40, 50, 60]
#print(data[::2])   # [10, 30, 50]


#12
#my_list = [10, 8, 6, 4, 2]
#del my_list[1:3]
#print(my_list)

# 13
#my_list = [10, 8, 6, 4, 2]
#del my_list[:]
#print(my_list)

#14
#my_list = [10, 8, 6, 4, 2]
#del my_list
#print(my_list)

#15
#data = [1, 2, 3, 4, 5]
#print(3 in data)

#16
#data = [1, 2, 3, 4, 5]
#print(10 not in data)

#17
#my_list = [17, 3, 11, 5, 1, 9, 7, 15, 13]
#largest = my_list[0]

#for i in range(1, len(my_list)):
#    if my_list[i] > largest:
#        largest = my_list[i]

#print(largest)

#18
#my_list = [17, 3, 11, 5, 1, 9, 7, 15, 13]
#largest = my_list[0]

#for i in my_list:
#    if i > largest:
#        largest = i

#print(largest)

#19
#my_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
#to_find = 5
#found = False

#for i in range(len(my_list)):
#    found = my_list[i] == to_find
#    if found:
#        break

#if found:
#    print("Elemen ditemukan pada index ke-", i)
#else:
#    print("Tidak ada di dalam list")

#20 
#lotre = [3, 7, 11, 42, 34, 49]
#keluar = [5, 9, 11, 42, 3, 49]

#benar = 0
#for num in lotre:
#    if num in keluar:
#        benar += 1

#print("Jumlah tebakan benar:", benar)

#22
#my_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
#to_find = 5
#found = False

#for i in range(len(my_list)):
#    found = my_list[i] == to_find
#    if found:
#        break

#if found:
#    print("Elemen ditemukan pada index ke-", i)
#else:
#    print("Tidak ada di dalam list")









