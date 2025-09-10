import qrcode
from PIL import Image, ImageTk
import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import threading

class QRGeneratorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("📷 QR Code Generator with Logo")
        self.geometry("950x600")
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")
        self.logo_path = None
        self.save_dir = os.getcwd()
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.left_frame = ctk.CTkFrame(self.main_frame, width=500)
        self.left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        self.right_frame = ctk.CTkFrame(self.main_frame, width=400)
        self.right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        self.build_left_ui()
        self.build_right_ui()
    
    def build_left_ui(self):
        title = ctk.CTkLabel(self.left_frame, text="QR Code Generator", font=("Arial", 22, "bold"))
        title.pack(pady=10)
        self.text_area = ctk.CTkTextbox(self.left_frame, width=450, height=180, font=("Arial", 13))
        self.text_area.pack(pady=10)
        self.text_area.insert("1.0", "Enter data (one per line)...")
        info_frame = ctk.CTkFrame(self.left_frame)
        info_frame.pack(pady=10, fill="x")
        self.logo_label = ctk.CTkLabel(info_frame, text="Logo: None", anchor="w")
        self.logo_label.pack(fill="x", padx=10, pady=5)
        self.folder_label = ctk.CTkLabel(info_frame, text=f"Save Folder: {self.save_dir}", anchor="w")
        self.folder_label.pack(fill="x", padx=10, pady=5)
        btn_frame = ctk.CTkFrame(self.left_frame)
        btn_frame.pack(pady=10)
        ctk.CTkButton(btn_frame, text="Choose Logo", command=self.choose_logo, width=120).grid(row=0, column=0, padx=10, pady=10)
        ctk.CTkButton(btn_frame, text="Choose Folder", command=self.choose_directory, width=120).grid(row=0, column=1, padx=10, pady=10)
        ctk.CTkButton(btn_frame, text="Generate QRs", command=self.start_generation, width=120).grid(row=0, column=2, padx=10, pady=10)
        self.progress = ctk.CTkProgressBar(self.left_frame, width=400)
        self.progress.set(0)
        self.progress.pack(pady=10)
        self.status_label = ctk.CTkLabel(self.left_frame, text="Idle", font=("Arial", 12))
        self.status_label.pack(pady=5)
    
    def build_right_ui(self):
        preview_title = ctk.CTkLabel(self.right_frame, text="Preview", font=("Arial", 18, "bold"))
        preview_title.pack(pady=10)
        self.preview_label = ctk.CTkLabel(self.right_frame, text="QR Preview will appear here")
        self.preview_label.pack(pady=20)

    def choose_logo(self):
        path = filedialog.askopenfilename(title="Select Logo", filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
        if path:
            self.logo_path = path
            self.logo_label.configure(text=f"Logo: {os.path.basename(path)}")

    def choose_directory(self):
        path = filedialog.askdirectory(title="Select Directory")
        if path:
            self.save_dir = path
            self.folder_label.configure(text=f"Save Folder: {path}")

    def start_generation(self):
        thread = threading.Thread(target=self.generate_qr_codes)
        thread.start()

    def generate_qr_codes(self):
        data_list = self.text_area.get("1.0", "end").strip().split("\n")
        data_list = [d for d in data_list if d.strip()]
        if not data_list:
            messagebox.showerror("Error", "Please enter some data!")
            return
        total = len(data_list)
        self.progress.set(0)
        self.status_label.configure(text="Generating QR Codes...")
        for i, data in enumerate(data_list, start=1):
            qr = qrcode.QRCode(
                version=4,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=10,
                border=4,
            )
            qr.add_data(data)
            qr.make(fit=True)
            qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
            if self.logo_path:
                logo = Image.open(self.logo_path)
                qr_width, qr_height = qr_img.size
                logo_size = qr_width // 4
                logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
                pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
                white_box = Image.new("RGB", (logo_size, logo_size), "white")
                qr_img.paste(white_box, pos)
                qr_img.paste(logo, pos, mask=logo if logo.mode == "RGBA" else None)
            safe_text = "".join([c if c.isalnum() else "_" for c in data[:15]]) or f"QRCode_{i}"
            file_path = os.path.join(self.save_dir, f"{safe_text}.png")
            qr_img.save(file_path)
            self.progress.set(i / total)
            self.status_label.configure(text=f"Generated {i}/{total} QR Codes")
            self.update_idletasks()
            if i == total:
                img_tk = ImageTk.PhotoImage(qr_img.resize((250, 250)))
                self.preview_label.configure(image=img_tk, text="")
                self.preview_label.image = img_tk
        self.status_label.configure(text="✅ Completed!")
        messagebox.showinfo("Success", f"Generated {total} QR Codes!")

if __name__ == "__main__":
    app = QRGeneratorApp()
    app.mainloop()
