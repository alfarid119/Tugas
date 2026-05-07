# comparasion operator
#x = 10
#y = 5
#print(x > y)
#print(x < y)
#print(x == y)
#print(x != y)
#print(x >= y)
#print(x <= y)

#Kuis 11
#n = int(input("Masukkan sebuah angka: "))
#if n > 100:
    #print(True)
#else:
       #print( False)

# conditional statement : if tunggal
#n = 75
#if n > 10:
    #print("n lebih besar dari 10")

# conditional statement : rangkaian if
# = 5
#f n > 10:
   #print("n lebih besar dari 10")
#f n > 5:
    #rint("n lebih besar dari 5")
#f n == 5:
    #rint("n sama dengan 5")

# conditional statement : if else
#n = 5
#if n > 10:
    #print("n lebih besar dari 10")
#else:
    #print("n tidak lebih besar dari 10")

# conditional statement : if elif else
#n = 75
#if n > 100: 
 #   print("n lebih besar dari 100")
#elif n > 50:
 #   print("n lebih besar dari 50")      
#elif n > 10:
#    print("n lebih besar dari 10")
#else:   
#  print("n tidak lebih besar dari 10")

# membadingkan 2 buah angka
#angka1 = int(input("Masukkan angka pertama: "))
#angka2 = int(input("Masukkan angka kedua: "))

# memilih angka yang lebih kecil
#if angka1 > angka2: angka_kecil = angka2
#else: angka_kecil = angka1
#print("Angka yang lebih kecil adalah:", angka_kecil)
    
# mecari angka yang lebih besar dari 3 buah angka input
#angka1 = int(input("Masukkan angka pertama: "))
#angka2 = int(input("Masukkan angka kedua: "))
#angka3 = int(input("Masukkan angka ketiga: "))

# memilih angka yang lebih besar
#if angka1 >= angka2 and angka1 >= angka3:
    #angka_besar = angka1
#elif angka2 >= angka1 and angka2 >= angka3:
   # angka_besar = angka2
#else:
   # angka_besar = angka3

#rint("Angka yang lebih besar adalah:", angka_besar)

# fungsi max() untuk mencari angka terbesar
#angka1 = int(input("Masukkan angka pertama: "))
#angka2 = int(input("Masukkan angka kedua: "))
#angka3 = int(input("Masukkan angka ketiga: "))

#angka_besar = max(angka1, angka2, angka3)
#print("Angka yang lebih besar adalah:", angka_besar)

# pajak
#nama = input("Masukkan nama: ")
#penghasilan = int(input("Masukkan penghasilan: "))
#if penghasilan <= 60000000:
    #pajak = 0.05 * penghasilan
    #print("besar pajak yang kenai oleh", nama, "adalah:", "5%")
    #print("Pajak yang harus dibayar oleh", nama, "adalah:", pajak)
    #print("Penghasilan setelah dipotong pajak:", penghasilan - pajak)
#elif penghasilan <= 250000000:
    #pajak = 0.15 * penghasilan
    #print("besar pajak yang kenai oleh", nama, "adalah:", "15%")
    #print("Pajak yang harus dibayar oleh", nama, "adalah:", pajak)
    #print("Penghasilan setelah dipotong pajak:", penghasilan - pajak)
#elif penghasilan <= 500000000:
    #pajak = 0.25 * penghasilan
    #print("besar pajak yang kenai oleh", nama, "adalah:", "25%")
    #print("Pajak yang harus dibayar oleh", nama, "adalah:", pajak)
    #print("Penghasilan setelah dipotong pajak:", penghasilan - pajak)
#else:    
 #   pajak = 0.30 * penghasilan
 #   print("besar pajak yang kenai oleh", nama, "adalah:", "30%")
 #   print("Pajak yang harus dibayar oleh", nama, "adalah:", pajak)
#    print("Penghasilan setelah dipotong pajak:", penghasilan - pajak)