import getpass
from prettytable import PrettyTable
import locale

# Set locale untuk pemformatan angka
locale.setlocale(locale.LC_ALL, '')

class ActionFigure:
    def __init__(self, name, brand, price, quantity, description=""):
        self.name = name
        self.brand = brand
        self.price = float(price)  # Ubah string harga menjadi float
        self.quantity = int(quantity)  # Ubah string stok menjadi integer
        self.description = description

    def to_dict(self):
        return {
            "Name": self.name,
            "Brand": self.brand,
            "Price": locale.currency(self.price, grouping=True),
            "Quantity": self.quantity,
            "Description": self.description
        }

class ActionFigureStore:
    def __init__(self):
        self.action_figures = {}
        self.cart = []
        self.balance = 1000000  # Saldo default
        self.add_default_action_figures()

    def add_default_action_figures(self):
        default_figures = [
            ActionFigure("Iron Man", "Marvel", 1500000, 10, "Baju besi keren untuk bertarung melawan penjahat."),
            ActionFigure("Batman", "DC", 1200000, 8, "Pahlawan gelap yang melawan kejahatan di Gotham City."),
            ActionFigure("Goku", "Dragon Ball", 1000000, 15, "Pahlawan Saiyan yang bertarung untuk melindungi bumi dari kejahatan.")
        ]
        for figure in default_figures:
            self.action_figures[figure.name] = figure

    def add_action_figure(self, action_figure):
        if action_figure.name not in self.action_figures:
            self.action_figures[action_figure.name] = action_figure
            print(f"{action_figure.name} ditambahkan ke toko.")
        else:
            print(f"{action_figure.name} sudah ada di toko.")

    def update_action_figure(self, name, field, value):
        if name in self.action_figures:
            if hasattr(self.action_figures[name], field):
                # Ubah harga dan stok menjadi float dan integer jika bidang yang diperbarui adalah "price" atau "quantity"
                if field == "price":
                    value = float(value)
                elif field == "quantity":
                    value = int(value)
                setattr(self.action_figures[name], field, value)
                print(f"{field} untuk {name} diperbarui.")
            else:
                print(f"{field} tidak valid.")
        else:
            print(f"{name} tidak ditemukan.")

    def delete_action_figure(self, name):
        if name in self.action_figures:
            del self.action_figures[name]
            print(f"{name} dihapus dari toko.")
        else:
            print(f"{name} tidak ditemukan.")

    def display_action_figures(self):
        table = PrettyTable()
        table.field_names = ["Name", "Brand", "Price", "Quantity", "Description"]
        for action_figure in self.action_figures.values():
            table.add_row(list(action_figure.to_dict().values()))
            table.add_row(["-" * 20] * len(table.field_names))  # Menambahkan garis pemisah setelah setiap action figure
        print(table)

    def purchase_action_figure(self, name, quantity):
        if name in self.action_figures:
            if self.action_figures[name].quantity >= quantity:
                self.action_figures[name].quantity -= quantity
                print(f"{quantity} {name} telah dibeli.")
                return True
            else:
                print("Stok tidak cukup untuk pembelian ini.")
                return False
        else:
            print(f"{name} tidak ditemukan.")
            return False

    def top_up_balance(self, amount):
        self.balance += amount
        print(f"Saldo Anda berhasil ditambahkan sebesar {locale.currency(amount, grouping=True)}. Saldo sekarang: {locale.currency(self.balance, grouping=True)}")

    def add_to_cart(self, name, quantity):
        if name in self.action_figures:
            if self.action_figures[name].quantity >= quantity:
                self.cart.append((name, quantity))
                print(f"{quantity} {name} telah ditambahkan ke keranjang belanja.")
            else:
                print("Stok tidak cukup untuk menambahkan item ini ke keranjang.")
        else:
            print(f"{name} tidak ditemukan.")

    def view_cart(self):
        if not self.cart:
            print("Keranjang belanja kosong.")
        else:
            print("Isi Keranjang Belanja:")
            for item in self.cart:
                print(f"{item[1]} {item[0]}")

    def buy_from_cart(self):
        total_price = sum(self.action_figures[item[0]].price * item[1] for item in self.cart)
        if total_price > self.balance:
            print("Saldo tidak mencukupi untuk pembelian ini.")
        else:
            for item in self.cart:
                if not self.purchase_action_figure(item[0], item[1]):
                    return
            self.balance -= total_price
            self.cart.clear()
            print(f"Pembelian berhasil. Saldo sekarang: {locale.currency(self.balance, grouping=True)}")

def admin_login(store):
    username = input("Masukkan username: ")
    password = getpass.getpass("Masukkan password: ")
    # Di sini Anda dapat memeriksa username dan password
    if username == "admin" and password == "password":
        print("Login berhasil!")
        admin_menu(store)
    else:
        print("Login gagal. Coba lagi.")

def admin_menu(store):
    while True:
        print("\nPilih tindakan Admin:")
        print("1. Tambah Action Figure")
        print("2. Perbarui Action Figure")
        print("3. Hapus Action Figure")
        print("4. Tampilkan Semua Action Figure")
        print("5. Keluar ke Menu Utama")

        choice = input("Masukkan pilihan (1/2/3/4/5): ")

        if choice == '1':
            name = input("Masukkan nama Action Figure: ")
            brand = input("Masukkan brand Action Figure: ")
            price = locale.atof(input("Masukkan harga Action Figure (format x.xxx.xxx,xx): "))
            quantity = int(input("Masukkan jumlah Action Figure: "))
            description = input("Masukkan deskripsi Action Figure (opsional): ")
            action_figure = ActionFigure(name, brand, price, quantity, description)
            store.add_action_figure(action_figure)
        elif choice == '2':
            name = input("Masukkan nama Action Figure yang ingin diperbarui: ")
            field = input("Masukkan bidang yang ingin diperbarui (brand/price/quantity/description): ")
            value = input("Masukkan nilai baru: ")
            store.update_action_figure(name, field, value)
        elif choice == '3':
            name = input("Masukkan nama Action Figure yang ingin dihapus: ")
            store.delete_action_figure(name)
        elif choice == '4':
            store.display_action_figures()
        elif choice == '5':
            print("Kembali ke Menu Utama.")
            break
        else:
            print("Pilihan tidak valid. Silakan masukkan pilihan yang benar.")


def main():
    store = ActionFigureStore()
    while True:
        print("\nWELCOME TO ADMIN PANEL")
        print("\nPilih tindakan:")
        print("1. Login sebagai Admin")
        print("2. Keluar")

        choice = input("Masukkan pilihan (1/2): ")

        if choice == '1':
            admin_login(store)
        elif choice == '2':
            print("Terima kasih, sampai jumpa!")
            break
        else:
            print("Pilihan tidak valid. Silakan masukkan pilihan yang benar.")

if __name__ == "__main__":
    main()
