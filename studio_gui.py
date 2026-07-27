import os
import sys
import json
import threading
import subprocess
import traceback
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk

# Import local backend engines
from color_analyzer_v2 import analyze_photo
from pdf_generator import generate_pdf, SUBSEASON_PALETTES
from email_service import send_pdf_email

CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"sender_email": "dkvendemais@gmail.com", "sender_pass": ""}

def save_config(cfg):
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=2)
    except Exception as e:
        print(f"Error saving config: {e}")

class ChromatypeStudioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CHROMATYPE Studio — Professional Color Analysis Generator")
        self.root.geometry("640x780")
        self.root.resizable(True, True)
        
        self.config = load_config()
        
        # Style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.selected_photo_path = ""
        self.output_dir = os.path.join(os.path.expanduser("~"), "Desktop", "CHROMATYPE_Reports")
        os.makedirs(self.output_dir, exist_ok=True)
        
        self.create_widgets()

    def create_widgets(self):
        # Header Frame
        header = tk.Frame(self.root, bg="#111827", height=65)
        header.pack(fill="x")
        
        title_label = tk.Label(header, text="CHROMATYPE STUDIO", font=("Helvetica", 18, "bold"), fg="#FFFFFF", bg="#111827")
        title_label.pack(pady=(10, 2))
        
        subtitle_label = tk.Label(header, text="Desktop Manual & Auto PDF Report Generator", font=("Helvetica", 9), fg="#9CA3AF", bg="#111827")
        subtitle_label.pack(pady=(0, 10))
        
        # Scrollable Canvas Container
        canvas = tk.Canvas(self.root, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        
        form_frame = ttk.Frame(canvas, padding="15")
        form_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=form_frame, anchor="nw", width=620)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # 1. Client Name
        ttk.Label(form_frame, text="Client Full Name:", font=("Helvetica", 10, "bold")).grid(row=0, column=0, sticky="w", pady=2)
        self.name_entry = ttk.Entry(form_frame, width=45, font=("Helvetica", 10))
        self.name_entry.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        self.name_entry.insert(0, "Diego Kasper")
        
        # 2. Client Email
        ttk.Label(form_frame, text="Client Email Address (For Delivery):", font=("Helvetica", 10, "bold")).grid(row=2, column=0, sticky="w", pady=2)
        self.email_entry = ttk.Entry(form_frame, width=45, font=("Helvetica", 10))
        self.email_entry.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        self.email_entry.insert(0, "dkvendemais@gmail.com")
        
        # 3. Season Selection
        ttk.Label(form_frame, text="Seasonal Sub-Palette:", font=("Helvetica", 10, "bold")).grid(row=4, column=0, sticky="w", pady=2)
        
        season_options = ["Auto-Detect (Optical Algorithm)"] + list(SUBSEASON_PALETTES.keys())
        self.season_var = tk.StringVar(value=season_options[0])
        self.season_combo = ttk.Combobox(form_frame, textvariable=self.season_var, values=season_options, state="readonly", font=("Helvetica", 10))
        self.season_combo.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        
        # 4. Photo Selection
        ttk.Label(form_frame, text="Client Portrait Photo:", font=("Helvetica", 10, "bold")).grid(row=6, column=0, sticky="w", pady=2)
        
        photo_btn_frame = ttk.Frame(form_frame)
        photo_btn_frame.grid(row=7, column=0, columnspan=2, sticky="ew", pady=(0, 5))
        
        self.browse_btn = ttk.Button(photo_btn_frame, text="📁 Choose Photo File...", command=self.browse_photo)
        self.browse_btn.pack(side="left", padx=(0, 10))
        
        self.photo_label = ttk.Label(photo_btn_frame, text="No photo selected", font=("Helvetica", 9, "italic"))
        self.photo_label.pack(side="left")
        
        # Thumbnail Preview Frame
        self.preview_frame = tk.Frame(form_frame, width=90, height=90, bg="#F3F4F6", highlightbackground="#D1D5DB", highlightthickness=1)
        self.preview_frame.grid(row=8, column=0, columnspan=2, pady=5)
        self.preview_label = tk.Label(self.preview_frame, text="Preview", bg="#F3F4F6", fg="#9CA3AF")
        self.preview_label.pack(expand=True)
        
        # Options Checkboxes
        self.open_pdf_var = tk.BooleanVar(value=True)
        self.remove_bg_var = tk.BooleanVar(value=True)
        self.send_email_var = tk.BooleanVar(value=True)
        
        chk_frame = ttk.Frame(form_frame)
        chk_frame.grid(row=9, column=0, columnspan=2, pady=5, sticky="w")
        
        ttk.Checkbutton(chk_frame, text="Open PDF automatically after generation", variable=self.open_pdf_var).pack(anchor="w")
        ttk.Checkbutton(chk_frame, text="Attempt Optical Background Cutout (RemBG)", variable=self.remove_bg_var).pack(anchor="w")
        ttk.Checkbutton(chk_frame, text="Send PDF via Email automatically to client", variable=self.send_email_var).pack(anchor="w")
        
        # 5. SMTP Sender Settings Panel
        smtp_labelframe = ttk.LabelFrame(form_frame, text="⚙️ Email Delivery Settings (Gmail / SMTP)", padding="10")
        smtp_labelframe.grid(row=10, column=0, columnspan=2, sticky="ew", pady=10)
        
        ttk.Label(smtp_labelframe, text="Sender Gmail Address:", font=("Helvetica", 9, "bold")).grid(row=0, column=0, sticky="w")
        self.sender_email_entry = ttk.Entry(smtp_labelframe, width=35, font=("Helvetica", 9))
        self.sender_email_entry.grid(row=0, column=1, sticky="w", padx=5, pady=2)
        self.sender_email_entry.insert(0, self.config.get("sender_email", "dkvendemais@gmail.com"))
        
        ttk.Label(smtp_labelframe, text="Gmail App Password (16-char):", font=("Helvetica", 9, "bold")).grid(row=1, column=0, sticky="w")
        self.sender_pass_entry = ttk.Entry(smtp_labelframe, width=35, font=("Helvetica", 9), show="*")
        self.sender_pass_entry.grid(row=1, column=1, sticky="w", padx=5, pady=2)
        self.sender_pass_entry.insert(0, self.config.get("sender_pass", ""))
        
        ttk.Label(smtp_labelframe, text="Need App Password? Generate one in Google Account -> Security -> App Passwords", font=("Helvetica", 8, "italic"), foreground="#6B7280").grid(row=2, column=0, columnspan=2, sticky="w", pady=(2, 0))
        
        # 6. Interactive HSL Color Mixer & 4-Season Spectrum Panel
        hsl_labelframe = ttk.LabelFrame(form_frame, text="🎨 Interactive HSL Color Mixer & 4-Season Spectrum", padding="10")
        hsl_labelframe.grid(row=11, column=0, columnspan=2, sticky="ew", pady=10)
        
        # H, S, L Variables
        self.hue_var = tk.IntVar(value=344)
        self.sat_var = tk.IntVar(value=100)
        self.light_var = tk.IntVar(value=40)
        self.hex_var = tk.StringVar(value="#CE0037")
        
        # HUE Slider
        ttk.Label(hsl_labelframe, text="H (Hue: 0°–360°):", font=("Helvetica", 9, "bold")).grid(row=0, column=0, sticky="w")
        self.hue_scale = ttk.Scale(hsl_labelframe, from_=0, to=360, variable=self.hue_var, command=self.update_hsl_from_sliders)
        self.hue_scale.grid(row=0, column=1, sticky="ew", padx=5)
        self.hue_entry = ttk.Entry(hsl_labelframe, textvariable=self.hue_var, width=6, font=("Helvetica", 9))
        self.hue_entry.grid(row=0, column=2, sticky="w")
        
        # SATURATION Slider
        ttk.Label(hsl_labelframe, text="S (Sat: 0%–100%):", font=("Helvetica", 9, "bold")).grid(row=1, column=0, sticky="w")
        self.sat_scale = ttk.Scale(hsl_labelframe, from_=0, to=100, variable=self.sat_var, command=self.update_hsl_from_sliders)
        self.sat_scale.grid(row=1, column=1, sticky="ew", padx=5)
        self.sat_entry = ttk.Entry(hsl_labelframe, textvariable=self.sat_var, width=6, font=("Helvetica", 9))
        self.sat_entry.grid(row=1, column=2, sticky="w")
        
        # LIGHTNESS Slider
        ttk.Label(hsl_labelframe, text="L (Light: 0%–100%):", font=("Helvetica", 9, "bold")).grid(row=2, column=0, sticky="w")
        self.light_scale = ttk.Scale(hsl_labelframe, from_=0, to=100, variable=self.light_var, command=self.update_hsl_from_sliders)
        self.light_scale.grid(row=2, column=1, sticky="ew", padx=5)
        self.light_entry = ttk.Entry(hsl_labelframe, textvariable=self.light_var, width=6, font=("Helvetica", 9))
        self.light_entry.grid(row=2, column=2, sticky="w")
        
        # HEX Code Entry
        ttk.Label(hsl_labelframe, text="HEX Code:", font=("Helvetica", 9, "bold")).grid(row=3, column=0, sticky="w")
        self.hex_entry = ttk.Entry(hsl_labelframe, textvariable=self.hex_var, width=12, font=("Helvetica", 9, "bold"))
        self.hex_entry.grid(row=3, column=1, sticky="w", padx=5, pady=4)
        
        # Live Color Swatch Box
        self.color_swatch_box = tk.Frame(hsl_labelframe, width=120, height=50, bg="#CE0037", relief="solid", bd=1)
        self.color_swatch_box.grid(row=0, column=3, rowspan=4, padx=10, pady=2)
        self.color_swatch_box.pack_propagate(False)
        self.swatch_text = tk.Label(self.color_swatch_box, text="#CE0037", bg="#CE0037", fg="#FFFFFF", font=("Helvetica", 9, "bold"))
        self.swatch_text.pack(expand=True)

        # Status Bar & Progress
        self.progress_bar = ttk.Progressbar(form_frame, mode="indeterminate")
        self.progress_bar.grid(row=12, column=0, columnspan=2, sticky="ew", pady=(10, 2))
        
        self.status_label = ttk.Label(form_frame, text="Ready", font=("Helvetica", 10, "bold"), foreground="#10B981")
        self.status_label.grid(row=13, column=0, columnspan=2, pady=(0, 10))
        
        # Big Generate Button
        self.generate_btn = tk.Button(
            form_frame, 
            text="✨ GENERATE COLOR DOSSIER PDF", 
            font=("Helvetica", 12, "bold"),
            bg="#10B981", 
            fg="#FFFFFF", 
            activebackground="#059669",
            activeforeground="#FFFFFF",
            relief="flat",
            pady=12,
            command=self.start_generation
        )
        self.generate_btn.grid(row=14, column=0, columnspan=2, sticky="ew", pady=(5, 15))

    def update_hsl_from_sliders(self, *args):
        try:
            h = int(self.hue_var.get()) % 360
            s = max(0, min(100, int(self.sat_var.get()))) / 100.0
            l = max(0, min(100, int(self.light_var.get()))) / 100.0
            
            import colorsys
            r, g, b = colorsys.hls_to_rgb(h / 360.0, l, s)
            hex_code = f"#{int(r * 255):02X}{int(g * 255):02X}{int(b * 255):02X}"
            
            self.hex_var.set(hex_code)
            self.color_swatch_box.config(bg=hex_code)
            self.swatch_text.config(text=hex_code, bg=hex_code, fg="#FFFFFF" if l < 0.6 else "#000000")
        except Exception:
            pass

    def browse_photo(self):
        file_path = filedialog.askopenfilename(
            title="Select Client Photo",
            filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp *.webp")]
        )
        if file_path:
            self.selected_photo_path = file_path
            self.photo_label.config(text=os.path.basename(file_path))
            self.show_preview(file_path)

    def show_preview(self, path):
        try:
            img = Image.open(path)
            img.thumbnail((80, 80))
            self.tk_img = ImageTk.PhotoImage(img)
            self.preview_label.config(image=self.tk_img, text="")
        except Exception:
            self.preview_label.config(image="", text="No Preview")

    def start_generation(self):
        if not self.selected_photo_path or not os.path.exists(self.selected_photo_path):
            messagebox.showerror("Missing Photo", "Please select a valid client photo before generating.")
            return
            
        client_name = self.name_entry.get().strip() or "Valued Client"
        client_email = self.email_entry.get().strip()
        selected_season = self.season_var.get()
        
        sender_email = self.sender_email_entry.get().strip()
        sender_pass = self.sender_pass_entry.get().strip()
        
        # Save credentials to config
        save_config({"sender_email": sender_email, "sender_pass": sender_pass})
        
        self.generate_btn.config(state="disabled")
        self.browse_btn.config(state="disabled")
        self.progress_bar.start(10)
        self.update_status("Starting color analysis...")
        
        threading.Thread(
            target=self.run_pipeline,
            args=(self.selected_photo_path, client_name, client_email, selected_season, sender_email, sender_pass),
            daemon=True
        ).start()

    def run_pipeline(self, image_path, client_name, client_email, selected_season, sender_email, sender_pass):
        try:
            # 1. Analyze colors
            self.update_status("1/3 Analyzing skin tone & color metrics...")
            analysis_data = analyze_photo(image_path, apply_white_balance=True)
            
            # Manual Season Override
            if selected_season != "Auto-Detect (Optical Algorithm)":
                analysis_data['sub_season'] = selected_season
                if "Spring" in selected_season:
                    analysis_data['season'] = "Spring"
                elif "Summer" in selected_season:
                    analysis_data['season'] = "Summer"
                elif "Autumn" in selected_season:
                    analysis_data['season'] = "Autumn"
                elif "Winter" in selected_season:
                    analysis_data['season'] = "Winter"

            # 2. Background removal (with safe fallback)
            cutout_path = image_path
            if self.remove_bg_var.get():
                self.update_status("2/3 Processing background removal...")
                temp_cutout = os.path.join(self.output_dir, "_temp_cutout.png")
                try:
                    from background_remover import remove_background
                    remove_background(image_path, temp_cutout)
                    if os.path.exists(temp_cutout) and os.path.getsize(temp_cutout) > 1000:
                        cutout_path = temp_cutout
                except Exception as bg_err:
                    print(f"Background removal skipped/fallback: {bg_err}")
                    cutout_path = image_path

            # 3. Generate PDF
            self.update_status("3/3 Rendering Color Dossier PDF...")
            safe_name = "".join(c for c in client_name if c.isalnum() or c in (' ', '_')).rstrip()
            safe_name = safe_name.replace(' ', '_')
            output_filename = f"CHROMATYPE_Report_{safe_name}.pdf"
            output_pdf_path = os.path.join(self.output_dir, output_filename)
            
            generated_path = generate_pdf(cutout_path, analysis_data, output_pdf_path, client_name=client_name)
            
            # Clean up temp cutout if created
            if cutout_path != image_path and os.path.exists(cutout_path):
                try: os.remove(cutout_path)
                except: pass

            # 4. Optional Email Delivery
            email_status_msg = ""
            if self.send_email_var.get() and client_email:
                self.update_status("Sending email with PDF attachment to client...")
                try:
                    sent_ok = send_pdf_email(client_email, generated_path, smtp_user=sender_email, smtp_pass=sender_pass)
                    if sent_ok:
                        email_status_msg = f"\n\n✉️ Email successfully sent to {client_email}!"
                except Exception as mail_err:
                    email_status_msg = f"\n\n⚠️ Could not send email: {mail_err}\n(Tip: Enter your 16-character Gmail App Password in Email Settings)."

            self.root.after(0, self.on_success, generated_path, email_status_msg)
        except Exception as e:
            traceback.print_exc()
            self.root.after(0, self.on_error, str(e))

    def update_status(self, text):
        self.root.after_idle(lambda: self.status_label.config(text=text, foreground="#2563EB"))

    def on_success(self, pdf_path, extra_msg=""):
        self.progress_bar.stop()
        self.generate_btn.config(state="normal")
        self.browse_btn.config(state="normal")
        self.status_label.config(text=f"✓ Complete: {os.path.basename(pdf_path)}", foreground="#10B981")
        
        if self.open_pdf_var.get() and os.path.exists(pdf_path):
            try:
                os.startfile(pdf_path)
            except Exception:
                subprocess.Popen(['start', pdf_path], shell=True)

        messagebox.showinfo("Report Ready!", f"Color Analysis Report successfully generated!\n\nSaved to:\n{pdf_path}{extra_msg}")

    def on_error(self, err_msg):
        self.progress_bar.stop()
        self.generate_btn.config(state="normal")
        self.browse_btn.config(state="normal")
        self.status_label.config(text="Generation Error", foreground="#EF4444")
        messagebox.showerror("Error Generating Report", f"An error occurred while building the report:\n{err_msg}")

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = ChromatypeStudioApp(root)
        root.mainloop()
    except Exception as e:
        print("Fatal error starting CHROMATYPE Studio GUI:")
        traceback.print_exc()
        input("Press Enter to exit...")
