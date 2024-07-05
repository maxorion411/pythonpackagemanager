import tkinter as tk
from tkinter import messagebox
import subprocess

def get_installed_packages():
    result = subprocess.run(['pip', 'list'], capture_output=True, text=True)
    packages = result.stdout.split('\n')[2:]  # Bỏ qua các dòng đầu tiên chứa tiêu đề
    return [pkg.split()[0] for pkg in packages if pkg]

def refresh_package_list():
    # Xóa tất cả các phần tử con của frame_list
    for widget in frame_list.winfo_children():
        widget.destroy()
    
    packages = get_installed_packages()
    for package in packages:
        frame = tk.Frame(frame_list)
        label = tk.Label(frame, text=package, width=40, anchor="w")
        label.pack(side="left")
        button = tk.Button(frame, text="Uninstall", command=lambda pkg=package: uninstall_package(pkg))
        button.pack(side="right")
        frame.pack(fill="x", pady=2)
    
    # Cập nhật lại canvas để hiển thị danh sách
    canvas.configure(scrollregion=canvas.bbox("all"))

def uninstall_package(package_name):
    confirm = messagebox.askyesno("Confirm Uninstall", f"Are you sure you want to uninstall {package_name}?")
    if confirm:
        subprocess.run(['pip', 'uninstall', package_name, '-y'])
        refresh_package_list()

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Python Package Manager")

# Tạo canvas và scrollbar để chứa danh sách gói
canvas = tk.Canvas(root)
frame_list = tk.Frame(canvas)
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)
canvas.create_window((0,0), window=frame_list, anchor="nw")

# Thêm sự kiện để cập nhật kích thước của canvas
def on_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

frame_list.bind("<Configure>", on_frame_configure)

# Tạo nút để làm mới danh sách gói
refresh_button = tk.Button(root, text="Refresh List", command=refresh_package_list)
refresh_button.pack(pady=10)

# Tải danh sách gói ban đầu
refresh_package_list()

# Chạy vòng lặp chính của Tkinter
root.mainloop()
