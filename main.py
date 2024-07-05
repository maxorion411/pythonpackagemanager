import tkinter as tk
from tkinter import messagebox
import subprocess

def get_installed_packages():
    result = subprocess.run(['pip', 'list'], capture_output=True, text=True)
    packages = result.stdout.split('\n')[2:]  # Bỏ qua các dòng đầu tiên chứa tiêu đề
    return [pkg.split()[0] for pkg in packages if pkg]

def refresh_package_list():
    listbox.delete(0, tk.END)
    for package in get_installed_packages():
        listbox.insert(tk.END, package)

def uninstall_package():
    selected_package = listbox.get(tk.ACTIVE)
    if selected_package:
        confirm = messagebox.askyesno("Confirm Uninstall", f"Are you sure you want to uninstall {selected_package}?")
        if confirm:
            subprocess.run(['pip', 'uninstall', selected_package, '-y'])
            refresh_package_list()

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Python Package Manager")

# Tạo listbox để hiển thị các gói đã cài đặt
listbox = tk.Listbox(root, width=50, height=20)
listbox.pack(pady=20)

# Tạo nút để làm mới danh sách gói
refresh_button = tk.Button(root, text="Refresh List", command=refresh_package_list)
refresh_button.pack(pady=10)

# Tạo nút để gỡ cài đặt gói
uninstall_button = tk.Button(root, text="Uninstall Package", command=uninstall_package)
uninstall_button.pack(pady=10)

# Tải danh sách gói ban đầu
refresh_package_list()

# Chạy vòng lặp chính của Tkinter
root.mainloop()
