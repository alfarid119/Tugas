# 1
#membuat tuple dan menampilkan isinya
#tuple_1 = (1, 2, 4, 8)
#tuple_2 = 1., .5, .25, .125
#print(tuple_1)
#print(tuple_2)

# 2 
#menggunakan tuple
#my_tuple = (1, 10, 100, 1000)
#print(my_tuple[0])  # Output: 1
#print(my_tuple[-1])  # Output: 1000
#print(my_tuple[1:])  # Output: slice dari index 1 sampai akhir (10, 100, 1000)
#print(my_tuple[:-3])  # Output: slice sampai index -3 (1, 10)
#for element in my_tuple:
    #print(element)

# 3
#modifikasi tupple
#my_tuple = (1, 10, 100, 1000)
#try: 
    #my_tuple[1] = -10  # mencoba modifikasi
#except TypeError as e:
    #print("Error:", e)

# 4
#tuple dengan berbagai tipe data
#my_tuple = (1, 10, 100, 1000)
#t1 = my_tuple + (10000, 100000)
#t2 = my_tuple * 3
#print(len(t2))
#print(t1)
#print(t2)
#print(10 in my_tuple)
#print(-10 not in my_tuple)

# 5
#penugasan simultan pada tuple
#x, y = 1, 2
#print("Sebelum swap: x =", x, ", y =", y)
#x, y = y, x   # swap tanpa variabel sementara
#print("Setelah swap: x =", x, ", y =", y)

#var = 123
#t1 = (1, )
#t2 = (2, )
#t3 = (3, var)
#t1, t2, t3 = t2, t3, t1  # penugasan simultan
#print(t1, t2, t3)

# 6
#membuat dictionary dan menampilkan isinya
#dictionary = {"cat": "kucing", "dog": "anjing", "horse": "kuda"}
#nilai_alpro2 = {'morin': 90, 'arya': 95, 'faqih': 98}
#dictionary_kosong = {}
#print(dictionary)
#print(nilai_alpro2)
#print(dictionary_kosong)

# 7
#akses nilai dalam dictionary
#dictionary = {"cat": "kucing", "dog": "anjing", "horse": "kuda"}
#nilai_alpro2 = {'morin': 90, 'arya': 95, 'faqih': 98}
#print(dictionary['cat'])
#print(nilai_alpro2['morin'])

# 8
#metode keys
#dictionary = {"cat": "kucing", "dog": "anjing", "horse": "kuda"}
#for kunci in dictionary.keys():
    #print(kunci, "->", dictionary[kunci])

# 9
#metode values
#dictionary = {"cat": "kucing", "dog": "anjing", "horse": "kuda"}
#for indo in dictionary.values():
    #print(indo)

# 10
#metode items
#dictionary = {"cat": "kucing", "dog": "anjing", "horse": "kuda"}
#for eng, indo in dictionary.items():
    #print(eng, "->", indo)

# 11
#metode update
#dictionary = {"cat": "kucing", "dog": "anjing", "horse": "kuda"}
#dictionary.update({'duck': 'bebek'})
#print(dictionary)

# 12
#metode popitem
#dictionary = {"cat": "kucing", "dog": "anjing", "horse": "kuda"}
#item = dictionary.popitem()
#print("Item dihapus:", item)
#print("Dictionary sekarang:", dictionary)

# 13
#modifikasi dictionary
#dictionary = {"cat": "kucing", "dog": "anjing", "horse": "kuda"}
#dictionary['cat'] = 'meong'  # modifikasi nilai untuk kunci 'cat
#dictionary['duck'] = 'bebek'  # menambahkan kunci baru 'duck'
#del dictionary['dog']  # menghapus kunci 'dog'
#for key in sorted(dictionary.keys()):
    #print(key, "->", dictionary[key])

# 14
#menanggulangi Exception
#try:
    #x = int(input("Masukkan angka: "))
    #print("Hasil:", 10 / x)
#except ValueError:
    #print("Error: Input bukan angka!")
#except ZeroDivisionError:
    #print("Error: Tidak boleh dibagi nol!")

# 15
#multi-exception
#kelas_informatika = {}
#while True:
    #nama = input("Masukkan nama (kosong=selesai): ")
    #if nama == '':
        #break
    #try:
        #nilai = int(input("Masukkan nilai(0-10): "))
        #if nilai not in range(0, 11):
            #print("Nilai harus 0-10!")
            #break
    #except ValueError:
        #print("Error: Nilai harus angka!")
        #break
    #if nama in kelas_informatika:
        #kelas_informatika[nama] += (nilai, )
    #else:
        #kelas_informatika[nama] = (nilai, )
#for nama in sorted(kelas_informatika.keys()):
    #total = sum(kelas_informatika[nama])
    #jml = len(kelas_informatika[nama])
    #print(nama, ":", total/jml)
