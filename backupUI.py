import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import mainUI as mainUIModule
from core.Wimkit import WimBackup, WIMOperation

class BackupUI:
    def __init__(self, root):
        self.root = root
        self.root.title("DBAR Backup ToolBox")
        self.root.geometry("600x300")
        
        # Create interface components
        self.create_widgets()
        
        # Initialize backup object
        self.backup_obj = None

    def create_widgets(self):
        # Source path selection
        tk.Label(self.root, text="Source Path:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.source_path = tk.Entry(self.root, width=50)
        self.source_path.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(self.root, text="Browse", command=self.browse_source).grid(row=0, column=2, padx=5, pady=5)
        
        # Progress bar
        self.progress = ttk.Progressbar(self.root, length=400, mode='determinate')
        self.progress.grid(row=4, column=0, columnspan=3, padx=5, pady=10)
        
        # Status label
        self.status_label = tk.Label(self.root, text="Ready")
        self.status_label.grid(row=5, column=0, columnspan=3, pady=5)
        
        # Backup button
        self.backup_button = tk.Button(self.root, text="Start Backup", command=self.start_backup)
        self.backup_button.grid(row=6, column=1, pady=10)
        
    def browse_source(self):
        """Select source path"""
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.source_path.delete(0, tk.END)
            self.source_path.insert(0, folder_selected)
            
    def start_backup(self):
        """Start backup process"""
        # Get input values
        source = self.source_path.get()
        
        # Disable backup button to prevent duplicate operations
        self.backup_button.config(state=tk.DISABLED)
        self.status_label.config(text="Initializing backup...")

        self.status_label.config(text="Creating backup...")
            
            # Build complete backup file path
            
            # Create full backup
        result = mainUIModule.MainUI.readSettingsInfoFromTXT("compressLevel")
        if result == "Fast":
             global success
             success = WimBackup.creatFullBackup(source, compressLevel="1")
        elif result == "Medium":
             success = WimBackup.creatFullBackup(source, compressLevel="default")
        else:
             success = WimBackup.creatFullBackup(source, compressLevel="15")

        if success:
                self.status_label.config(text="Backup completed")
                messagebox.showinfo("Success", "Backup has been successfully completed")
                self.backup_button.config(state=tk.NORMAL)
        else:
                self.status_label.config(text="Backup failed")
                messagebox.showerror("Error", "An error occurred during backup")
                self.backup_button.config(state=tk.NORMAL)
                
    def update_progress(self, value):
        """Update progress bar"""
        self.progress['value'] = value
        self.root.update_idletasks()

if __name__ == "__main__":
    root = tk.Tk()
    app = BackupUI(root)
    root.mainloop()
