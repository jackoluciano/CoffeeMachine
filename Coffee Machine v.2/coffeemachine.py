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
import sys                                                      # Library untuk melakukan sesuatu tindakan oleh system
sys.dont_write_bytecode = True                                  # agar tidak menghasilkan cache

import threading                                                # Modul untuk melakukan dua tugas secara paralel
import pyautogui                                                # Modul untuk menekan tombol pada keyboard secara otomatis
import time                                                     # Modul untuk memanipulasi nilai-nilai waktu
import qrcode                                                   # Modul berisi fungsi-fungsi QR Code
import logging                                                  # Modul berisi fungsi-fungsi mengenai log
import uuid                                                     # Modul untuk generate ID unik
import inventory                                                # File database dalam bentuk dictionary
import socket                                                   # Modul untuk mendeteksi ip host
from flask import Flask, request, redirect, render_template     # Modul untuk menjalankan dan memanipulasi aplikasi Flask

# ALGORITMA
# Mendefinisikan list dan pelanggan
coffee_list = ["1. Espresso", "2. Americano", "3. Macchiato", "4. Cappucino", "5. Flat White", "6. Mocha", "7. Latte"]
harga       = [12000, 15000, 22000, 18000, 18000, 22000, 18000]

# Mengupdate jumlah bahan
cup    = inventory.data ['cup']
kopi   = inventory.data ['kopi']
gula   = inventory.data ['gula']
krimer = inventory.data ['krimer']
susu   = inventory.data ['susu']
coklat = inventory.data ['coklat']
air    = inventory.data ['air']
es     = inventory.data ['es']

# Loop layar utama
while True:

    # Mendefinisikan jumlah bahan terkini, jumlah bahan total dikurangi array bahan
    cup    = inventory.data ['cup']
    kopi   = inventory.data ['kopi']
    gula   = inventory.data ['gula']
    krimer = inventory.data ['krimer']
    susu   = inventory.data ['susu']
    coklat = inventory.data ['coklat']
    air    = inventory.data ['air']
    es     = inventory.data ['es']

    # Penambahan karakter ke array token
    pelangganKe = inventory.data['pelanggan']
    if len(inventory.token)!= pelangganKe:          # Agar token tidak lebih banyak dari pelanggan
        inventory.token         += ['no token']
        inventory.statustoken   += ['no status']

    with open('inventory.py', 'w') as p:
        p.write(f"data = {inventory.data}\n")
        p.write(f"order = {inventory.order}\n")
        p.write(f"token = {inventory.token}\n")
        p.write(f"statustoken = {inventory.statustoken}\n")

    # Tampilan layar utama
    print(f"Kamu adalah pelanggan ke-{pelangganKe} hari ini!")
    order= input("SELAMAT DATANG! Apakah kamu ingin memesan kopi? (yes): ")

# Loop layar order
    while order=="yes":
        
        # Mendefinisikan ulang jumlah bahan terkini (perlu apabila terjadi reorder)        
        cup    = inventory.data ['cup']
        kopi   = inventory.data ['kopi']
        gula   = inventory.data ['gula']
        krimer = inventory.data ['krimer']
        susu   = inventory.data ['susu']
        coklat = inventory.data ['coklat']
        air    = inventory.data ['air']
        es     = inventory.data ['es']

        pelangganKe = inventory.data['pelanggan']
        if len(inventory.token)!= pelangganKe:
            inventory.token         += ['no token']
            inventory.statustoken   += ['no status']

        with open('inventory.py', 'w') as p:
            p.write(f"data = {inventory.data}\n")
            p.write(f"order = {inventory.order}\n")
            p.write(f"token = {inventory.token}\n")
            p.write(f"statustoken = {inventory.statustoken}\n")

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
                    print("Maaf, kami kehabisan air.")
                    break

            else:
                print("Maaf, kami kehabisan kopi.")
                break

        else:
            print("Maaf, kami kehabisan cup.")
            break

        # Mengosongkan list langkah langkah pembuatan kopi dan mendefinisikan keluar (cancel order)
        list_order = []
        keluar     = False
        selesai    = False

# Input 1: memilih kopi
        while True:
            coffeechoice = input("Pilih kopi (1-7/cancel): ")

            # Mengosongkan count bahan
            milk_count      = 0
            creamer_count   = 0
            chocolate_count = 0
            water_count     = 0

            # Menambah cup dan espresso yang memerlukan sedikit air untuk setiap jenis kopi
            if coffeechoice in ['1','2','3','4','5','6','7']:
                list_order.append("menambah kopi")
                list_order.append("menambah espresso")

                water_count += 0.5
                break

            elif coffeechoice=="cancel":
                keluar = True
                break

            else:
                print("Ketik 1-7")

        if keluar == True:
            break

        # Menambahkan bahan tertentu untuk jenis kopi tertentu
        if coffeechoice in ['4','5','6','7']:
            list_order.append("menambah susu")
            milk_count      +=1

        if coffeechoice in ['3','4','5','6','7']:
            list_order.append("menambah krimer")
            creamer_count   +=1

        if coffeechoice == '6':
            list_order.append("menambah coklat")
            chocolate_count +=1

        if coffeechoice == '2':
            list_order.append("menambah air")
            water_count     +=1

# Input 2: menambah kadar espresso
        while True:

            while True:
                espresso= input("Tambah espresso shot (0-5/cancel): ")

                # Mengecek sisa espresso yang masih bisa ditambahkan
                if espresso in ["0", "1", "2", "3", "4", "5"]:

                    if kopi >=60:
                        break

                    elif 50 <= kopi < 60:
                        if int(espresso) > 4:
                            print("hanya tersedia sampai 4 espresso shot")
                        else:
                            break

                    elif 40 <= kopi < 50:
                        if int(espresso) > 3:
                            print("hanya tersedia sampai 3 espresso shot")
                        else:
                            break

                    elif 30 <= kopi < 40:
                        if int(espresso) > 2:
                            print("hanya tersedia sampai 2 espresso shot")
                        else:
                            break    

                    elif 20 <= kopi < 30:
                        if int(espresso) > 1:
                            print("hanya tersedia sampai 1 espresso shot")
                        else:
                            break

                elif espresso == "cancel":
                    keluar=True
                    break

                else:
                    print("ketik 0-5 atau cancel")

            if keluar == True:
                break

            if espresso in ["0", "1", "2", "3", "4", "5"]:
                list_order.append(f"menambah {int(espresso)} espresso shot")
                shot = f'{int(espresso)+1} shot'
                break

        if keluar == True:
            break

# Input 3: kadar gula
        while True:

            while True:
                sugar_level= input("Tambah kadar gula (0-5/cancel): ")

                # Mengecek sisa gula yang masih bisa ditambahkan 
                if sugar_level in ["0", "1", "2", "3", "4", "5"]:

                    if gula >= 50:
                        break

                    elif 40 <= gula < 50:
                        if int(sugar_level) > 4:
                            print("hanya tersedia sampai 4 sendok teh gula")
                        else:
                            break

                    elif 30 <= gula < 40:
                        if int(sugar_level) > 3:
                            print("hanya tersedia sampai 3 sendok teh gula")
                        else:
                            break

                    elif 20 <= gula < 30:
                        if int(sugar_level) > 2:
                            print("hanya tersedia sampai 2 sendok teh gula")
                        else:
                            break   

                    elif 10 <= gula < 20:
                        if int(sugar_level) > 1:
                            print("hanya tersedia sampai 1 sendok teh gula")
                        else:
                            break

                elif sugar_level == "cancel":
                    keluar=True
                    break

                else:
                    print("ketik 0-5 atau cancel")

            if keluar == True:
                break

            if sugar_level in ["0", "1", "2", "3", "4", "5"]:
                list_order.append(f"menambah {int(sugar_level)} sendok makan gula")
                if sugar_level in ['0']:
                    sugar= 'No sugar'
                elif sugar_level in ['1']:
                    sugar= 'Less sugar'
                elif sugar_level in ['2']:
                    sugar= 'Normal sugar'
                elif sugar_level in ['3','4','5']:
                    sugar= 'More sugar'

                break

        if keluar == True:
            break

# Input 4: es batu
        while True:
            iced = input("Iced atau Hot (iced/hot/cancel): ")
            ice_count= 0

            # Mengecek apakah menggunakan es atau tidak
            if iced.lower() == "iced":
                list_order.append("menambah es")
                ice_count+=1
                aise = 'Iced'
                break

            elif iced.lower() == "hot":
                aise = 'Hot'
                break

            elif iced.lower() == "cancel":
                keluar= True
                break

            else:
                print("tolong ketik 'iced' or 'hot'.")

        if keluar == True:
            break

# Input 5: pembayaran
        # Menampilkan total harga yang harus dibayarkan
        print(f"Harganya {harga[int(coffeechoice)-1]}")

        # Loop validasi metode pembayaran
        while True:
            metodepembayaran= input('Masukkan metode pembayaran (QRIS/Cash/Debit): ')

        # METODE PEMBAYARAN QRIS            
            if metodepembayaran.lower() == 'qris':

                # Menyembunyikan pesan bawaan flask
                log = logging.getLogger('werkzeug')
                log.disabled = True

                # Membuat aplikasi Flask
                app = Flask(__name__)

                # Memonitor apakah pembayaran selesai
                pembayaran_selesai = threading.Event()  # untuk timeout

                # Menginisiasi fungsi untuk generate token
                def generate_token():
                    return str(uuid.uuid4())

                token = generate_token()

                # Menginisiasi fungsi untuk scan QR
                def scan_qr(token):
                    url = f"http://{socket.gethostbyname(socket.gethostname())}:8080/konfirmasi/{token}"
                    qr = qrcode.QRCode(
                        version=1,
                        box_size=5,
                        border=4,
                    )
                    qr.add_data(url)
                    qr.make(fit=True)
                    qr.print_ascii()

                # Menambahkan Order Details untuk ditampilkan di receipt/halaman konfirmasi pembayaran
                inventory.order['total']                = f'{harga[int(coffeechoice)-1]}'
                inventory.order['nama barang']          = f'{coffee_list[int(coffeechoice)-1].split(". ")[1]}'
                inventory.order['ice']                  = aise
                inventory.order['Sugar']                = sugar
                inventory.order['Coffee']               = shot

                # Menyimpan data ke file inventory.py
                with open('inventory.py', 'w') as p:
                    p.write(f"data = {inventory.data}\n")
                    p.write(f"order = {inventory.order}\n")
                    p.write(f"token = {inventory.token}\n")
                    p.write(f"statustoken = {inventory.statustoken}\n")

                # Tampilan layar konfirmasi berupa hasil render templates/konfirmasi.html
                @app.route('/konfirmasi/<token>', methods=['GET','POST'])
                def konfirmasi(token):
                    if token in inventory.token:
                        if inventory.statustoken[pelangganKe-1] == 'valid':
                        # Ketika pengguna menekan 'lanjut ke pembayaran'                    
                            if request.method == 'POST':
                                return redirect(f"/PIN/{token}")
                            return render_template("konfirmasi.html", 
                                                Total      = inventory.order['total'], 
                                                namaBarang = inventory.order['nama barang'], 
                                                orderID    = inventory.order['orderID'], 
                                                ice        = inventory.order['ice'], 
                                                sugar      = inventory.order['Sugar'], 
                                                shot       = inventory.order['Coffee'])
                        elif inventory.statustoken[pelangganKe-1] == 'berhasil':
                            return render_template("berhasil.html", 
                                                Total      = inventory.order['total'], 
                                                namaBarang = inventory.order['nama barang'], 
                                                orderID    = inventory.order['orderID'], 
                                                time       = inventory.order['time'], 
                                                date       = inventory.order['date'], 
                                                ice        = inventory.order['ice'], 
                                                sugar      = inventory.order['Sugar'], 
                                                shot       = inventory.order['Coffee'])
                        elif inventory.statustoken[pelangganKe-1] == 'invalid':
                            return render_template("https408.html")
                    else:
                        return render_template('https401.html')

                # Menambahkan tanggal dan waktu konfirmasi
                inventory.order['date'] = time.strftime("%A, %B %d, %Y")
                inventory.order['time'] = time.strftime("%H:%M")

                # Menyimpan data ke file inventory.py
                with open('inventory.py', 'w') as p:
                    p.write(f"data = {inventory.data}\n")
                    p.write(f"order = {inventory.order}\n")
                    p.write(f"token = {inventory.token}\n")
                    p.write(f"statustoken = {inventory.statustoken}\n")

                # Tampilan layar masukkan PIN berupa hasil render templates/pin.html
                @app.route('/PIN/<token>', methods=['GET','POST'])
                def PIN(token):

                    # Ketika pengguna menekan 'konfirmasi'
                    if request.method == 'POST':
                        return redirect(f"/berhasil/{token}")   
                    return render_template("pin.html")             

                # Tampilan layar pembayaran berhasil
                @app.route('/berhasil/<token>', methods=['GET'])
                def berhasil(token):
                    print(f"Pembayaran berhasil dengan order ID: {token}")

                    inventory.statustoken[pelangganKe-1] = 'berhasil'

                    # Menyimpan data ke file inventory.py
                    with open('inventory.py', 'w') as p:
                        p.write(f"data = {inventory.data}\n")
                        p.write(f"order = {inventory.order}\n")
                        p.write(f"token = {inventory.token}\n")
                        p.write(f"statustoken = {inventory.statustoken}\n")

                    # Sampai set belum terjadi, wait terus dilakukan
                    pembayaran_selesai.set()
                    return render_template("berhasil.html", 
                                           Total      = inventory.order['total'], 
                                           namaBarang = inventory.order['nama barang'], 
                                           orderID    = inventory.order['orderID'], 
                                           time       = inventory.order['time'], 
                                           date       = inventory.order['date'], 
                                           ice        = inventory.order['ice'], 
                                           sugar      = inventory.order['Sugar'], 
                                           shot       = inventory.order['Coffee'])

                # Menginisiasi fungsi untuk menjalankan server Flask di thread terpisah
                def start_server():
                    app.run(host='0.0.0.0', port=8080)

                # Algoritma utama untuk mengeksekusi fungsi-fungsi yang ada
                while True:
                    # Apabila Flask dijalankan dan tidak diimpor
                    if __name__ == "__main__":
                        
                        # Membuat model QR dengan url yang diberikan token
                        inventory.token[pelangganKe-1]          = generate_token()
                        inventory.statustoken[pelangganKe-1]    = 'valid'
                        inventory.order['orderID']              = inventory.token[pelangganKe-1]

                        with open('inventory.py', 'w') as p:
                            p.write(f"data = {inventory.data}\n")
                            p.write(f"order = {inventory.order}\n")
                            p.write(f"token = {inventory.token}\n")
                            p.write(f"statustoken = {inventory.statustoken}\n")

                        scan_qr(inventory.token[pelangganKe-1])

                        # Membuka server Flask
                        server_thread = threading.Thread(target=start_server)
                        server_thread.daemon = True
                        server_thread.start()

                        # Menunggu sampai pembayaran selesai (timeout 60 detik menunggu sampai pembayaran_selesai.set() dijalankan)
                        print("Menunggu konfirmasi pembayaran...")
                        selesai = pembayaran_selesai.wait(timeout=60) 
                        
                        if selesai:
                            print("Proses pembuatan kopi dimulai!")
                            break
                        
                        # Konfirmasi regenerate kode QRIS
                        else:
                            inventory.statustoken[pelangganKe-1] = 'invalid'

                            with open('inventory.py', 'w') as p:
                                p.write(f"data = {inventory.data}\n")
                                p.write(f"order = {inventory.order}\n")
                                p.write(f"token = {inventory.token}\n")
                                p.write(f"statustoken = {inventory.statustoken}\n")

                            while True:
                                lanjut = input('Mengulang pembayaran?(Yes/No):')
                                if lanjut.lower() == 'no':
                                    keluar = True
                                    break
                                elif lanjut.lower() == 'yes':
                                    break
                                else:
                                    print('Ketik Yes/no')
                            if keluar == True:
                                break
                if keluar==True:
                    break
                if selesai == True:
                    break

        # METODE PEMBAYARAN CASH            
            elif metodepembayaran.lower() == 'cash':
                uangjumlah = 0

                # Loop nominal uang
                while True:
                    uang = input("Masukkan uang (atau cancel): ")
                    
                    try:
                        uangjumlah += int(uang)

                        # Uang kurang dari harga kopi (minta lagi)
                        if uangjumlah< harga[int(coffeechoice)-1]:
                            print(f"Uang yang anda masukkan kurang Rp. {(harga[int(coffeechoice)-1])-uangjumlah}")
                        
                        # Uang sama dengan harga kopi (membuat kopi)
                        elif uangjumlah == harga[int(coffeechoice)-1]:
                            print("Proses pembuatan kopi dimulai!")
                            selesai = True
                            break

                        # Uang lebih dari harga kopi (memberi kembalian dan membuat kopi)
                        else:
                            print(f"Uang yang anda masukkan lebih, anda akan menerima kembalian sebanyak Rp. {uangjumlah-(harga[int(coffeechoice)-1])}")
                            print("Proses pembuatan kopi dimulai!")
                            selesai = True
                            break

                    # Apabila batal melakukan transaksi, uang akan dikembalikan
                    except ValueError:
                        if uang == 'cancel':
                            print("Uang akan dikembalikan...")
                            print("")
                            keluar = True
                            break
                        else:
                            print("Hanya dapat memasukkan integer/cancel")
                if selesai== True:
                    break
                if keluar == True:
                    break
        
        # METODE PEMBAYARAN DEBIT
            elif metodepembayaran.lower() == 'debit':

                # Memasukkan nomor kartu
                while True:
                    nomorKartu= input("Masukkan nomor Kartu or cancel: ")
                    try:
                        nomorBaru= int(nomorKartu)
                        if len(nomorKartu) != 16:
                            print("Masukkan 16 digit nomor kartu anda!")
                        else:
                            break
                    except ValueError:
                        if nomorKartu=='cancel':
                            keluar= True
                            break
                        else:
                            print("Hanya bisa memasukkan karakter angka!")
                if keluar== True:
                    break
                
                # Memasukkan nomor CVV
                while True:
                    CVVnomor= input("Masukkan nomor CVV or cancel: ")
                    try:
                        CVVBaru= int(CVVnomor)
                        if len(CVVnomor) != 3 and len(CVVnomor) != 4:
                            print("Masukkan 3-4 digit nomor CVV anda!")
                        else:
                            break
                    except ValueError:
                        if CVVnomor == 'cancel':
                            keluar= True
                            break
                        else:
                            print("Hanya bisa memasukkan karakter angka!")
                if keluar==True:
                    break

                # Memasukkan expiry date
                while True:
                    expiryDate= input("Masukkan tanggal expiry date (DDMMYY) or cancel: ")
                    try:
                        expirybaru= int(expiryDate)
                        if len(expiryDate) != 6:
                            print("Masukkan  6 karakter DDMMYY (contoh 1 januari 2025 maka 010125)!")
                        else:
                            print("Proses pembuatan kopi dimulai!")
                            selesai = True
                            break
                    except ValueError:
                        if expiryDate== 'cancel':
                            keluar= True
                            break
                        else:
                            print("Hanya bisa memasukkan karakter angka!")
                if selesai == True:
                    break                
                if keluar==True:
                    break

            else:
                print('hanya menerima pembayaran QRIS/Cash/Debit!')
            
        if keluar == True:
            break

# Algoritma pembuatan kopi

        # Mengurangi bahan yang telah digunakan dalam proses
        inventory.data['cup']        -= 1
        inventory.data['kopi']       -= 10 * (int(espresso) + 1)
        inventory.data['susu']       -= 200 * milk_count
        inventory.data['krimer']     -= 50 * creamer_count
        inventory.data['coklat']     -= 10 * chocolate_count
        inventory.data['air']        -= 300 * water_count
        inventory.data['gula']       -= 10 * int(sugar_level)
        inventory.data['es']         -= 2 * ice_count

        # Menambah jumlah pelanggan dan pendapatan
        inventory.data['pelanggan'] += 1
        inventory.data['pendapatan'] += harga[int(coffeechoice)-1]

        # Menyimpan data ke file inventory.py
        with open('inventory.py', 'w') as p:
            p.write(f"data = {inventory.data}\n")
            p.write(f"order = {inventory.order}\n")
            p.write(f"token = {inventory.token}\n")
            p.write(f"statustoken = {inventory.statustoken}\n")

        # Mengerjakan langkah-langkah orderan
        print(list_order)
        time.sleep(10)

# Input 6: memesan kembali
        # Mendefinisikan fungsi input reorder untuk dijadikan target Thread
        def getinput2():
            global reorder
            reorder= input("Apakah kamu mau memesan ulang? (yes/no): ")

        # Algoritma timeout, akan kembali ke layar utama bila tidak diberi input selama 10 detik
        reorder = None
        thread2 = threading.Thread(target = getinput2)
        thread2.start()
        thread2.join(timeout = 10)

        if reorder == None:
            pyautogui.press('enter')
            print("")
            break

        if reorder == "no":
            print("")
            break

        print('')

# Algoritma maintenance
    while order == "AKUMAUKOPI":

        # Tampilan menu maintenance
        print("1. Cek Sisa dan Menambahkan Bahan")
        print("2. Cek Pendapatan")
        print("3. Pembersihan Mesin Kopi")
        print("4. Keluar")

        maintenance = input("Masukkan pilihan: ")

        # Pengecekan bahan
        if maintenance   == '1':
            print(f"1. Cup    = {inventory.data ['cup']} buah") 
            print(f"2. kopi   = {inventory.data ['kopi']} g")
            print(f"3. gula   = {inventory.data ['gula']} g")
            print(f"4. krimer = {inventory.data ['krimer']} g")
            print(f"5. susu   = {inventory.data ['susu']} ml")
            print(f"6. coklat = {inventory.data ['coklat']} g")
            print(f"7. air    = {inventory.data ['air']} ml") 
            print(f"8. es     = {inventory.data ['es']} balok")
            print("")

            # Penambahan bahan
            while True:
                mauTambah = input("Apakah mau menambahkan bahan? (Yes/No): ")

                if mauTambah.lower() == 'yes':
                    bahanBahan = ['cup', 'kopi', 'gula', 'krimer', 'susu', 'coklat', 'air', 'es']

                    # Membuat fungsi untuk mempermudah penambahan bahan dan harga
                    def tambahbahan(a,b):
                        inventory.data [f'{bahanBahan[a-1]}'] += b

                    tambahan = int(input("Masukkan nomor bahan yang ingin ditambahkan: "))
                    jumlahBahan = int(input("Masukkan tambahan jumlah bahan: "))

                    tambahbahan(tambahan, jumlahBahan)

                    # Menyimpan data ke inventory.py
                    with open('inventory.py', 'w') as p:
                        p.write(f"data = {inventory.data}\n")
                        p.write(f"order = {inventory.order}\n")
                        p.write(f"token = {inventory.token}\n")
                        p.write(f"statustoken = {inventory.statustoken}\n")

                    print('Jumlah bahan telah diupdate!')

                elif mauTambah.lower() == 'no':
                    print("")
                    break

                else: 
                    print("Ketik Yes/No.")

        # Cek Pendapatan
        elif maintenance == '2':
            print(f"Pendapatan total adalah Rp. {inventory.data['pendapatan']}")
            print("")

        # Pembersihan mesin kopi     
        elif maintenance == '3':
            print("sedang dibersihkan...")

            time.sleep(10)
            print("Pembersihan selesai!")
            print("")

        # Keluar dari menu maintenance dan kembali ke layar utama
        elif maintenance == "4":
            print("")
            break

        # Input selain pilihan
        else:
            print("masukkan 1-4")
            print("")