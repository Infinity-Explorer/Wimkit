import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os

class SettingsUI:
    def __init__(self, root):
        self.root = root
        self.root.title("DBAR Toolbox - Settings")
        self.root.geometry("580x500")
        self.root.configure(bg="#f0f0f0")
        
        self.create_widgets()
    
    def create_widgets(self):
        # Title
        title_label = tk.Label(self.root, text="Settings", bg="#f0f0f0", font=('Arial', 16, 'bold'))
        title_label.pack(pady=20)
        
        # Settings frame
        settings_frame = tk.Frame(self.root, bg="#f0f0f0")
        settings_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        # Version
        version_frame = tk.Label(settings_frame, text="Version Information\nWimkit v1.1.3", bg="#f0f0f0", font=('Arial', 10, 'bold'))
        version_frame.pack()
        
        # Backup settings
        backup_frame = tk.LabelFrame(settings_frame, text="Backup Settings", bg="#f0f0f0", font=('Arial', 10, 'bold'))
        backup_frame.pack(fill=tk.X, pady=10)
        
        # Compression level
        compression_label = tk.Label(backup_frame, text="Compression Level:", bg="#f0f0f0")
        compression_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        self.compression_var = tk.StringVar(value="Medium")
        compression_options = ["None", "Fast", "Medium", "Maximum"]
        compression_menu = ttk.Combobox(backup_frame, textvariable=self.compression_var, values=compression_options, state="readonly", width=15)
        compression_menu.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        # Verify backup
        self.verify_var = tk.BooleanVar(value=True)
        verify_check = tk.Checkbutton(backup_frame, text="Verify file integrity after backup", variable=self.verify_var, bg="#f0f0f0")
        verify_check.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="w")
        
        # Restore settings
        restore_frame = tk.LabelFrame(settings_frame, text="Restore Settings", bg="#f0f0f0", font=('Arial', 10, 'bold'))
        restore_frame.pack(fill=tk.X, pady=10)
        
        # Overwrite confirmation
        self.confirm_var = tk.BooleanVar(value=True)
        confirm_check = tk.Checkbutton(restore_frame, text="Confirm before overwriting files", variable=self.confirm_var, bg="#f0f0f0")
        confirm_check.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        # Create backup folders
        self.create_dir_var = tk.BooleanVar(value=True)
        create_dir_check = tk.Checkbutton(restore_frame, text="Automatically create non-existent folders", variable=self.create_dir_var, bg="#f0f0f0")
        create_dir_check.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        
        # Interface settings
        ui_frame = tk.LabelFrame(settings_frame, text="Interface Settings", bg="#f0f0f0", font=('Arial', 10, 'bold'))
        ui_frame.pack(fill=tk.X, pady=10)
        
        # Theme
        theme_label = tk.Label(ui_frame, text="Theme:", bg="#f0f0f0")
        theme_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        self.theme_var = tk.StringVar(value="Light")
        theme_options = ["Light", "Dark"]
        theme_menu = ttk.Combobox(ui_frame, textvariable=self.theme_var, values=theme_options, state="readonly", width=15)
        theme_menu.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        
        # Buttons
        button_frame = tk.Frame(self.root, bg="#f0f0f0")
        button_frame.pack(pady=20)
        
        save_button = tk.Button(button_frame, text="Save", command=self.save_settings, width=10)
        save_button.pack(side=tk.LEFT, padx=10)
        
        cancel_button = tk.Button(button_frame, text="Cancel", command=self.root.destroy, width=10)
        cancel_button.pack(side=tk.LEFT, padx=10)
    
    def save_settings(self):
        # Add settings save logic here
        settings = {
            "compression": self.compression_var.get(),
            "verify_backup": self.verify_var.get(),
            "confirm_overwrite": self.confirm_var.get(),
            "create_directories": self.create_dir_var.get(),
            "theme": self.theme_var.get()
        }
        
        with open("./settings/settings.txt", "w", encoding='utf-8') as f:
            f.write(str(settings))
        print("Settings saved:", settings)
        
        # Show save success message
        messagebox.showinfo("Settings", "Settings have been saved")
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = SettingsUI(root)
    root.mainloop()
