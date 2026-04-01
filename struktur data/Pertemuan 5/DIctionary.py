#membuat struktur data dictionary
userLogin : dict[str, int | str] = {"name": "alfa", 
                "age": 21, 
                "role": "admin"}
print(type(userLogin))

#mengakses data dalam dictionary
print(f"Nama Akun : {userLogin['name']}")
print(f"Usia Akun : {userLogin['age']}")
print(f"Peran Akun : %s" % userLogin['role'])

print(userLogin)

#menambahkan data baru ke dalam dictionary
userLogin["email"] = "contoh@email.com"
print(userLogin)

#upadate data dalam dictionary
userLogin["role"] = "sales"
print(userLogin)

#hapus data dalam dictionary
del userLogin["role"]
print(userLogin)

#menghapus seluruh data dalam dictionary
#userLogin.clear()
#print(userLogin)

#dictionary bersarang

TabelLogin : dict[str, dict[str, int | str]] = {
    "user1": {
        "name": "alfa",
        "age": 21,
        "role": "admin"
    },
    "user2": {
        "name": "beta",
        "age": 22,
        "role": "sales"
    },
    "user3": {
        "name": "gamma",
        "age": 23,
        "role": "marketing"
    }
}
print(TabelLogin)


