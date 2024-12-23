# PROGRAM COFFEE MACHINE
# Deskripsi: Sistem kerja Coffee Machine dilengkapi berbagai macam fitur

# KAMUS
# coffee_list & list_order                      : Array of Str  
# harga                                         : Array of Int  
# Array bahan (cuparray, kopiarray, etc.)       : Array of Int  
# Bahan-bahan (cup, kopi, gula, etc.)           : Int           
# Count bahan (milk_count, creamer_count, etc.) : Int           
# pelanggan                                     : Int           
# keluar                                        : Boolean       
# coffeechoice, espresso, sugar_level, iced     : Str input     
# order, qris, reorder, maintenance             : Str input     

# LIBRARY
import threading      # Library untuk melakukan dua tugas secara paralel
import pyautogui      # Library untuk menekan tombol pada keyboard secara otomatis
import time           # Library berisi fungsi-fungsi waktu

# ALGORITMA
# Mendefinisikan list dan pelanggan
coffee_list = ["1. espresso", "2. americano", "3. macchiato", "4. cappucino", "5. flat white", "6. mocha", "7. latte"]
harga       = [12000, 15000, 22000, 18000, 18000, 22000, 18000]
pelanggan   = 1

# Mendefinisikan list kosong untuk update jumlah bahan
cuparray    = []
kopiarray   = []
gulaarray   = []
krimerarray = []
susuarray   = []
coklatarray = []
airarray    = []
esarray     = []

# Loop layar utama
while True:

# Mendefinisikan jumlah bahan terkini, jumlah bahan total dikurangi array bahan
    cup    = 100   - sum(cuparray)
    kopi   = 1000  - sum(kopiarray)
    gula   = 1000  - sum(gulaarray)
    krimer = 1000  - sum(krimerarray)
    susu   = 10000 - sum(susuarray)
    coklat = 1000  - sum(coklatarray)
    air    = 10000 - sum(airarray)
    es     = 100   - sum(esarray)

# Tampilan dan pesan layar utama
    print(f"Kamu adalah pelanggan ke-{pelanggan} hari ini!")
    order= input("WELCOME! Would you like to get some coffee? (yes): ")

# Loop layar order
    while order=="yes":
        
# Mendefinisikan ulang jumlah bahan terkini (perlu apabila terjadi reorder)        
        cup    = 100   - sum(cuparray)
        kopi   = 1000  - sum(kopiarray)
        gula   = 1000  - sum(gulaarray)
        krimer = 1000  - sum(krimerarray)
        susu   = 10000 - sum(susuarray)
        coklat = 1000  - sum(coklatarray)
        air    = 10000 - sum(airarray)
        es     = 100   - sum(esarray)

# Tampilan menu (dibagi menjadi beberapa kasus apabila beberapa bahan habis)
        if cup > 0:

            if kopi >= 10:

                if air >= 150:
                    print('MENU')
                    print(f"{coffee_list[0]} - {harga[0]}")

                    if air >= 450:
                        print(f"{coffee_list[1]} - {harga[1]}")

                    if krimer >= 50:
                        print(f"{coffee_list[2]} - {harga[2]}")

                        if susu >= 200:
                            print(f"{coffee_list[3]} - {harga[3]}")
                            print(f"{coffee_list[4]} - {harga[4]}")

                            if coklat >= 10:
                                print(f"{coffee_list[5]} - {harga[5]}")

                            print(f"{coffee_list[6]} - {harga[6]}")
                else:
                    print("sorry, we're running out of water.")
                    break

            else:
                print("sorry, we're running out of coffee.")
                break

        else:
            print("sorry, we're running out of cup.")
            break

# Mengosongkan list langkah langkah pembuatan kopi dan mendefinisikan keluar (cancel order)
        list_order = []
        keluar     = False

# Input 1: memilih kopi
        while True:
            coffeechoice = input("Choose coffee (1-7/cancel): ")

# Mengosongkan count bahan
            milk_count      = 0
            creamer_count   = 0
            chocolate_count = 0
            water_count     = 0

# Menambah cup dan espresso yang memerlukan sedikit air untuk setiap jenis kopi
            if coffeechoice in ['1','2','3','4','5','6','7']:
                list_order.append("add cup")
                list_order.append("add espresso")

                water_count += 0.5
                break

            elif coffeechoice=="cancel":
                keluar = True
                break

            else:
                print("Please type 1-7")

        if keluar == True:
            break

# Menambahkan bahan tertentu untuk jenis kopi tertentu
        if coffeechoice in ['4','5','6','7']:
            list_order.append("add milk")
            milk_count      +=1

        if coffeechoice in ['3','4','5','6','7']:
            list_order.append("add creamer")
            creamer_count   +=1

        if coffeechoice == '6':
            list_order.append("add chocolate")
            chocolate_count +=1

        if coffeechoice == '2':
            list_order.append("add water")
            water_count     +=1

# Input 2: menambah kadar espresso
        while True:

            while True:
                espresso= input("Add espresso shot (0-5/cancel): ")

# Mengecek sisa espresso yang masih bisa ditambahkan
                if espresso in ["0", "1", "2", "3", "4", "5"]:

                    if kopi >=60:
                        break

                    elif 50 <= kopi < 60:
                        if int(espresso) > 4:
                            print("available only up to 4 shot of espresso")
                        else:
                            break

                    elif 40 <= kopi < 50:
                        if int(espresso) > 3:
                            print("available only up to 3 shot of espresso")
                        else:
                            break

                    elif 30 <= kopi < 40:
                        if int(espresso) > 2:
                            print("available only up to 2 shot of espresso")
                        else:
                            break    

                    elif 20 <= kopi < 30:
                        if int(espresso) > 1:
                            print("available only up to 1 shot of espresso")
                        else:
                            break

                elif espresso == "cancel":
                    keluar=True
                    break

                else:
                    print("should be between 0-5 or cancel")

            if keluar == True:
                break

            if espresso in ["0", "1", "2", "3", "4", "5"]:
                list_order.append(f"add {int(espresso)} shot of espresso")
                break

        if keluar == True:
            break

# Input 3: kadar gula
        while True:

            while True:
                sugar_level= input("Input sugar level (0-5/cancel): ")

# Mengecek sisa gula yang masih bisa ditambahkan 
                if sugar_level in ["0", "1", "2", "3", "4", "5"]:

                    if gula >= 50:
                        break

                    elif 40 <= gula < 50:
                        if int(sugar_level) > 4:
                            print("available only up to 4 teaspoon of sugar")
                        else:
                            break

                    elif 30 <= gula < 40:
                        if int(sugar_level) > 3:
                            print("available only up to 3 teaspoon of sugar")
                        else:
                            break

                    elif 20 <= gula < 30:
                        if int(sugar_level) > 2:
                            print("available only up to 2 teaspoon of sugar")
                        else:
                            break   

                    elif 10 <= gula < 20:
                        if int(sugar_level) > 1:
                            print("available only up to 1 teaspoon of sugar")
                        else:
                            break

                elif sugar_level == "cancel":
                    keluar=True
                    break

                else:
                    print("should be between 0-5 or cancel")

            if keluar == True:
                break

            if sugar_level in ["0", "1", "2", "3", "4", "5"]:
                list_order.append(f"add {int(sugar_level)} teaspoon of sugar")
                break

        if keluar == True:
            break

# Input 4: es batu
        while True:
            iced = input("Iced or hot (iced/hot/cancel): ")
            ice_count= 0

# Mengecek apakah menggunakan es atau tidak
            if iced.lower() == "iced":
                list_order.append("add ice")
                ice_count+=1
                break

            elif iced.lower() == "hot":
                break

            elif iced.lower() == "cancel":
                keluar= True
                break

            else:
                print("Please type 'iced' or 'hot'.")

        if keluar == True:
            break

# Input 5: pembayaran
# Menampilkan total harga yang harus dibayarkan
        print(f"the price is {harga[int(coffeechoice)-1]}")

# Mendefinisikan fungsi input qris untuk dijadikan target Thread
        def getinput():
            global qris
            qris = input("Qris only (input anything/cancel): ")

# Algoritma timeout, akan kembali ke layar utama bila tidak diberi input selama 10 detik
        qris   = None
        thread = threading.Thread(target = getinput)
        thread.start()
        thread.join(timeout = 60)

        if qris == None:
            pyautogui.press('enter')
            break

        if qris == "cancel" :
            break

# Algoritma pembuatan kopi
# Mengurangi bahan yang telah digunakan dalam proses
        cuparray    .append(1)
        kopiarray   .append(10*(int(espresso)+1))
        susuarray   .append(200*milk_count)
        krimerarray .append(50*creamer_count)
        coklatarray .append(10*chocolate_count)
        airarray    .append(300*water_count)
        gulaarray   .append(10*int(sugar_level))
        esarray     .append(2*ice_count)

# Menginisiasi langkah-langkah orderan
        print(list_order)
        time.sleep(10)

# Menambah jumlah pelanggan
        pelanggan += 1

# Input 6: memesan kembali
# Mendefinisikan fungsi input reorder untuk dijadikan target Thread
        def getinput2():
            global reorder
            reorder= input("Do you want to reorder? (yes/no): ")

# Algoritma timeout, akan kembali ke layar utama bila tidak diberi input selama 10 detik
        reorder = None
        thread2 = threading.Thread(target = getinput2)
        thread2.start()
        thread2.join(timeout = 10)

        if reorder == None:
            pyautogui.press('enter')
            break

        if reorder == "no":
            break

# Algoritma maintenance
    while order == "AKUMAUKOPI":

# Tampilan menu maintenance
        print("1. Cek sisa bahan")
        print("2. Pembersihan mesin kopi")
        print("3. Keluar")

        maintenance = input("Masukkan pilihan: ")

# Pengecekan bahan
        if maintenance   == '1':
            print(f"Cup    = {cup} buah") 
            print(f"kopi   = {kopi} g")
            print(f"gula   = {gula} g")
            print(f"krimer = {krimer} g")
            print(f"susu   = {susu} ml")
            print(f"coklat = {coklat} g")
            print(f"air    = {air} ml") 
            print(f"es     = {es} balok")

# Pembersihan mesin kopi     
        elif maintenance == '2':
            print("sedang dibersihkan...")

            time.sleep(10)
            print("Pembersihan selesai!")

# Keluar dari menu maintenance dan kembali ke layar utama
        elif maintenance == "3":
            break

# Input selain pilihan
        else:
            print("masukkan 1-3")