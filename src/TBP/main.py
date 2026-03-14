import os
import subprocess
import tkinter as tk
from tkinter import messagebox


DEVICE_PATH = "/dev/sda" # Pfad zum Diskettenlaufwerk, z.B. "/dev/sda" oder "/dev/fd0"
MOUNT_POINT = "/media/pi/DISKETTE"

def create_image():
    img_name = img_entry.get().strip()
    if not img_name:
        messagebox.showerror("Fehler", "Bitte gib einen Namen für das Image ein.")
        return

    img_path = os.path.expanduser(f"~/DiskettenImages/{img_name}.img")
    os.makedirs(os.path.dirname(img_path), exist_ok=True)

    cmd = f"sudo dd if={DEVICE_PATH} of='{img_path}' bs=512 count=2880 conv=noerror,sync status=progress"
    output_text.insert(tk.END, f">> Erzeuge Image: {img_path}\n")
    output_text.insert(tk.END, f">> Befehl: {cmd}\n")
    output_text.see(tk.END)

    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        output_text.insert(tk.END, result.stdout + result.stderr)
    except Exception as e:
        output_text.insert(tk.END, f"Fehler: {str(e)}\n")

def open_mounted():
    if not os.path.exists(MOUNT_POINT):
        messagebox.showerror("Nicht gemountet", f"{MOUNT_POINT} existiert nicht.")
        return
    os.system(f"xdg-open {MOUNT_POINT}")

# GUI
root = tk.Tk()
root.title("BitPreserver")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack()

tk.Label(frame, text="Name der Image-Datei (ohne .img):").grid(row=0, column=0, sticky="w")
img_entry = tk.Entry(frame, width=40)
img_entry.grid(row=1, column=0, pady=5)

btn_frame = tk.Frame(frame)
btn_frame.grid(row=2, column=0, pady=10)

tk.Button(btn_frame, text="Diskette öffnen (wenn gemountet)", command=open_mounted).pack(side=tk.LEFT, padx=5)
tk.Button(btn_frame, text="Image erstellen", command=create_image).pack(side=tk.LEFT, padx=5)

output_text = tk.Text(root, height=12, width=80)
output_text.pack(padx=10, pady=10)

root.mainloop()