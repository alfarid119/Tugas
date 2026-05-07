# 1
#def cek_nilai(nilai=0):
    #if nilai > 0:
        #print("Nilai positif:", nilai)
        #return
    #print("Nilai tidak positif atau tidak diberikan")

#cek_nilai()

# 2
#def cek_nilai(nilai=0):
    #if nilai:
        #print("Nilai truthy:", nilai)
        #return
    #print("Nilai adalah False atau 0 atau kosong")

#cek_nilai(False)

# 3
#def kuadrat(angka):
    #return angka * angka

#hasil = kuadrat(5)
#print("Hasil kuadrat:", hasil)

# 4
#def kuadrat(angka):
    #return angka * angka

#kuadrat(7)
#print("Fungsi dipanggil, tapi return value tidak dipakai")

# 5
#def tanpa_return():
    #print("Fungsi ini tidak punya return eksplisit")

#hasil = tanpa_return()
#print("Nilai return:", hasil)
#print("Tipe data:", type(hasil))
#print("Apakah None?", hasil is None)

# 6
#def tampilkan_list(data):
    #print("Isi list:")
    #for item in data:
        #print("-", item)

buah = ["apel", "mangga", "jeruk"]
#tampilkan_list(buah)

# 7
#def tampilkan_list(data):
    #print("Isi list:")
    #for item in data:
        #print("-", item)

# Ganti argumen dengan list yang berbeda
#angka = [10, 20, 30, 40, 50]
#tampilkan_list(angka)

#hewan = ["kucing", "anjing", "kelinci"]
#tampilkan_list(hewan)

# 8
#def buat_list_kuadrat(n):
    #hasil = []
    #for i in range(1, n + 1):
        #hasil.append(i * i)
    #return hasil

#daftar_kuadrat = buat_list_kuadrat(5)
#print("List hasil fungsi:", daftar_kuadrat)

# kuis 23
#def tahun_kabisat(tahun):
    #if (tahun % 4 == 0 and tahun % 100 != 0) or (tahun % 400 == 0):
        #return True
    #return False

#data_uji = [1900, 2000, 2013, 1987]
#data_hasil = [False, True, True, False]

#for i in range(len(data_uji)):
    #th = data_uji[i]
    #print(th, "->", end=" ")
    #hasil = tahun_kabisat(th)
    #if hasil == data_hasil[i]:
        #print("Ok")
    #else:
        #print("Gagal")

# Kuis 24
#def tahun_kabisat(tahun):
    #if (tahun % 4 == 0 and tahun % 100 != 0) or (tahun % 400 == 0):
        #return True
    #return False

#def hari_didalam_bulan(tahun, bulan):
    #if bulan in [1, 3, 5, 7, 8, 10, 12]:
        #return 31
    #elif bulan in [4, 6, 9, 11]:
        #return 30
    #elif bulan == 2:
        #if tahun_kabisat(tahun):
            #return 29
        #else:
            #return 28

#data_uji   = [1900, 2000, 2016, 1987]
#data_bulan = [2, 2, 1, 11]
#data_hasil = [28, 29, 31, 30]

#for i in range(len(data_uji)):
    #thn = data_uji[i]
    #bln = data_bulan[i]
    #print(thn, bln, "->", end=" ")
    #hasil = hari_didalam_bulan(thn, bln)
    #if hasil == data_hasil[i]:
        #print("Ok")
    #else:
        #print("Gagal")

# Kuis 25
#def tahun_kabisat(tahun):
    #if (tahun % 4 == 0 and tahun % 100 != 0) or (tahun % 400 == 0):
        #return True
    #return False

#def hari_didalam_bulan(tahun, bulan):
    #if bulan in [1, 3, 5, 7, 8, 10, 12]:
        #return 31
    #elif bulan in [4, 6, 9, 11]:
        #return 30
    #elif bulan == 2:
        #return 29 if tahun_kabisat(tahun) else 28

#def hari_pada_tahun(tahun, bulan, hari):
    # Validasi argumen
    #if bulan < 1 or bulan > 12:
        #return None
    #maks_hari = hari_didalam_bulan(tahun, bulan)
    #if hari < 1 or hari > maks_hari:
        #return None

    # Hitung total hari dari 1 Januari
    #total = 0
    #for b in range(1, bulan):
        #total += hari_didalam_bulan(tahun, b)
    #total += hari
    #return total

#print(hari_pada_tahun(2000, 12, 31))  # Output: 366

# Kuis 26
#def cek_prima(bilangan):
    #if bilangan <= 1:
        #return False
    #for i in range(2, int(bilangan ** 0.5) + 1):
        #if bilangan % i == 0:
            #return False
    #return True

#for i in range(1, 20):
    #if cek_prima(i + 1):
        #print(i + 1, end=" ")
#print()

# Kuis 27
# sama persis seperti kuis 26

# Kuis 28
#def Liter100km_ke_mpg(liter):
    #mil_per_km = 1 / 1.609344          # 1 km = 1/1609.344 mil
    #galon_per_liter = 1 / 3.785411784  # 1 liter = 1/3.785... galon
    
    #km100 = 100                        # per 100 km
    #mil = km100 * mil_per_km           # konversi 100 km ke mil
    #galon = liter * galon_per_liter    # konversi liter ke galon
    #return mil / galon

#def mpg_ke_Liter100km(mil):
    #km_per_mil = 1.609344
    #liter_per_galon = 3.785411784
    
    #km100 = 100
    #km = mil * km_per_mil              # konversi mil ke km
    #liter = liter_per_galon            # 1 galon = x liter
    #return (liter * km100) / km

#print(Liter100km_ke_mpg(3.9))
#print(Liter100km_ke_mpg(7.5))
#print(Liter100km_ke_mpg(10.))
#print(mpg_ke_Liter100km(60.3))
#print(mpg_ke_Liter100km(31.4))
#print(mpg_ke_Liter100km(23.5))