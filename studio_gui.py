import os
import sys
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

class ChromatypeStudioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CHROMATYPE Studio — Professional Color Analysis Generator")
        self.root.geometry("640x740")
        self.root.resizable(False, False)
        
        # Style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.selected_photo_path = ""
        self.output_dir = os.path.join(os.path.expanduser("~"), "Desktop", "CHROMATYPE_Reports")
        os.makedirs(self.output_dir, exist_ok=True)
        
        self.create_widgets()

    def create_widgets(self):
        # Header Frame
        header = tk.Frame(self.root, bg="#111827", height=80)
        header.pack(fill="x")
        
        title_label = tk.Label(header, text="CHROMATYPE STUDIO", font=("Helvetica", 20, "bold"), fg="#FFFFFF", bg="#111827")
        title_label.pack(pady=(15, 2))
        
        subtitle_label = tk.Label(header, text="Desktop Manual & Auto PDF Report Generator", font=("Helvetica", 10), fg="#9CA3AF", bg="#111827")
        subtitle_label.pack(pady=(0, 15))
        
        # Main Form Container
        form_frame = ttk.Frame(self.root, padding="20")
        form_frame.pack(fill="both", expand=True)
        
        # 1. Client Name
        ttk.Label(form_frame, text="Client Full Name:", font=("Helvetica", 11, "bold")).grid(row=0, column=0, sticky="w", pady=5)
        self.name_entry = ttk.Entry(form_frame, width=45, font=("Helvetica", 11))
        self.name_entry.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 15))
        self.name_entry.insert(0, "Jane Doe")
        
        # 2. Client Email (Optional for sending)
        ttk.Label(form_frame, text="Client Email Address (Optional):", font=("Helvetica", 11, "bold")).grid(row=2, column=0, sticky="w", pady=5)
        self.email_entry = ttk.Entry(form_frame, width=45, font=("Helvetica", 11))
        self.email_entry.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 15))
        self.email_entry.insert(0, "client@example.com")
        
        # 3. Season Selection (Auto or Manual Override)
        ttk.Label(form_frame, text="Seasonal Sub-Palette:", font=("Helvetica", 11, "bold")).grid(row=4, column=0, sticky="w", pady=5)
        
        season_options = ["Auto-Detect (AI Algorithm)"] + list(SUBSEASON_PALETTES.keys())
        self.season_var = tk.StringVar(value=season_options[0])
        self.season_combo = ttk.Combobox(form_frame, textvariable=self.season_var, values=season_options, state="readonly", font=("Helvetica", 10))
        self.season_combo.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(0, 15))
        
        # 4. Photo Selection
        ttk.Label(form_frame, text="Client Portrait Photo:", font=("Helvetica", 11, "bold")).grid(row=6, column=0, sticky="w", pady=5)
        
        photo_btn_frame = ttk.Frame(form_frame)
        photo_btn_frame.grid(row=7, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        
        self.browse_btn = ttk.Button(photo_btn_frame, text="📁 Choose Photo File...", command=self.browse_photo)
        self.browse_btn.pack(side="left", padx=(0, 10))
        
        self.photo_label = ttk.Label(photo_btn_frame, text="No photo selected", font=("Helvetica", 9, "italic"))
        self.photo_label.pack(side="left")
        
        # Thumbnail Preview Frame
        self.preview_frame = tk.Frame(form_frame, width=120, height=120, bg="#F3F4F6", highlightbackground="#D1D5DB", highlightthickness=1)
        self.preview_frame.grid(row=8, column=0, columnspan=2, pady=5)
        self.preview_label = tk.Label(self.preview_frame, text="Preview", bg="#F3F4F6", fg="#9CA3AF")
        self.preview_label.pack(expand=True)
        
        # Options
        self.open_pdf_var = tk.BooleanVar(value=True)
        self.remove_bg_var = tk.BooleanVar(value=True)
        self.send_email_var = tk.BooleanVar(value=False)
        
        chk_frame = ttk.Frame(form_frame)
        chk_frame.grid(row=9, column=0, columnspan=2, pady=10, sticky="w")
        
        ttk.Checkbutton(chk_frame, text="Open PDF automatically after generation", variable=self.open_pdf_var).pack(anchor="w")
        ttk.Checkbutton(chk_frame, text="Attempt AI Background Cutout (RemBG)", variable=self.remove_bg_var).pack(anchor="w")
        ttk.Checkbutton(chk_frame, text="Send PDF via Email automatically (Requires SMTP credentials)", variable=self.send_email_var).pack(anchor="w")
        
        # Status Bar & Progress
        self.progress_bar = ttk.Progressbar(form_frame, mode="indeterminate")
        self.progress_bar.grid(row=10, column=0, columnspan=2, sticky="ew", pady=(15, 5))
        
        self.status_label = ttk.Label(form_frame, text="Ready", font=("Helvetica", 10, "bold"), foreground="#10B981")
        self.status_label.grid(row=11, column=0, columnspan=2)
        
        # Big Generate Button
        self.generate_btn = tk.Button(
            self.root, 
            text="✨ GENERATE 3-PAGE PDF REPORT", 
            font=("Helvetica", 12, "bold"),
            bg="#10B981", 
            fg="#FFFFFF", 
            activebackground="#059669",
            activeforeground="#FFFFFF",
            relief="flat",
            padding=12,
            command=self.start_generation
        )
        self.generate_btn.pack(fill="x", padx=20, pady=(0, 20))

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
            img.thumbnail((110, 110))
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
        
        self.generate_btn.config(state="disabled")
        self.browse_btn.config(state="disabled")
        self.progress_bar.start(10)
        self.update_status("Starting color analysis...")
        
        threading.Thread(
            target=self.run_pipeline,
            args=(self.selected_photo_path, client_name, client_email, selected_season),
            daemon=True
        ).start()

    def run_pipeline(self, image_path, client_name, client_email, selected_season):
        try:
            # 1. Analyze colors
            self.update_status("1/3 Analyzing skin tone & color metrics...")
            analysis_data = analyze_photo(image_path, apply_white_balance=True)
            
            # Manual Season Override
            if selected_season != "Auto-Detect (AI Algorithm)":
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
            self.update_status("3/3 Rendering 3-Page PDF Dossier...")
            safe_name = "".join(c for c in client_name if c.isalnum() or c in (' ', '_')).rstrip()
            safe_name = safe_name.replace(' ', '_')
            output_filename = f"CHROMATYPE_Report_{safe_name}.pdf"
            output_pdf_path = os.path.join(self.output_dir, output_filename)
            
            generated_path = generate_pdf(cutout_path, analysis_data, output_pdf_path, client_name=client_name)
            
            # Clean up temp cutout if created
            if cutout_path != image_path and os.path.exists(cutout_path):
                try: os.remove(cutout_path)
                except: pass

            # 4. Optional Email
            email_status_msg = ""
            if self.send_email_var.get() and client_email:
                self.update_status("Sending email to client...")
                try:
                    sent_ok = send_pdf_email(client_email, generated_path)
                    if not sent_ok:
                        email_status_msg = "\n(Note: Email delivery failed. Please check SMTP settings)."
                except Exception as mail_err:
                    email_status_msg = f"\n(Note: Email skipped: {mail_err})"

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
