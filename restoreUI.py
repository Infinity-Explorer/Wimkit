import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from core.Wimkit import WimRestore, WIMOperation

class RestoreUI:
    def __init__(self, root):
        self.root = root
        self.root.title("DBAR Toolbox - Restore Backup")
        self.root.geometry("600x400")
        self.root.configure(bg="#f0f0f0")
        
        # Initialize variables
        self.backup_file = tk.StringVar()
        self.restore_path = tk.StringVar()
        self.selected_backup_index = tk.IntVar()
        self.backup_info = {}  # Store backup information
        
        # Initialize restore object
        self.restore_obj = None
        
        self.create_widgets()
    
    def create_widgets(self):
        # Title
        title_label = tk.Label(self.root, text="Restore Backup", bg="#f0f0f0", font=('Arial', 16, 'bold'))
        title_label.pack(pady=20)
        
        # Main frame
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        # Select backup file frame
        backup_file_frame = tk.LabelFrame(main_frame, text="Select Backup File", bg="#f0f0f0", font=('Arial', 10, 'bold'))
        backup_file_frame.pack(fill=tk.X, pady=10)
        
        # Backup file path
        backup_path_frame = tk.Frame(backup_file_frame, bg="#f0f0f0")
        backup_path_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(backup_path_frame, text="Backup File:", bg="#f0f0f0").pack(side=tk.LEFT, padx=5)
        backup_entry = tk.Entry(backup_path_frame, textvariable=self.backup_file, width=50)
        backup_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        browse_button = tk.Button(backup_path_frame, text="Browse", command=self.browse_backup_file)
        browse_button.pack(side=tk.LEFT, padx=5)
        
        # Backup information frame
        info_frame = tk.LabelFrame(main_frame, text="Backup Information", bg="#f0f0f0", font=('Arial', 10, 'bold'))
        info_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Restore settings frame
        restore_settings_frame = tk.LabelFrame(main_frame, text="Restore Settings", bg="#f0f0f0", font=('Arial', 10, 'bold'))
        restore_settings_frame.pack(fill=tk.X, pady=10)
        
        # Restore path
        restore_path_frame = tk.Frame(restore_settings_frame, bg="#f0f0f0")
        restore_path_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(restore_path_frame, text="Restore To:", bg="#f0f0f0").pack(side=tk.LEFT, padx=5)
        restore_entry = tk.Entry(restore_path_frame, textvariable=self.restore_path, width=50)
        restore_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        browse_restore_button = tk.Button(restore_path_frame, text="Browse", command=self.browse_restore_path)
        browse_restore_button.pack(side=tk.LEFT, padx=5)
        
        # Restore options
        options_frame = tk.Frame(restore_settings_frame, bg="#f0f0f0")
        options_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Button frame
        button_frame = tk.Frame(self.root, bg="#f0f0f0")
        button_frame.pack(pady=20)
        
        restore_button = tk.Button(button_frame, text="Start Restore", command=self.start_restore, width=12)
        restore_button.pack(side=tk.LEFT, padx=10)
        
        cancel_button = tk.Button(button_frame, text="Cancel", command=self.root.destroy, width=12)
        cancel_button.pack(side=tk.LEFT, padx=10)
        
        # Progress bar
        self.progress = ttk.Progressbar(self.root, length=500, mode='determinate')
        self.progress.pack(pady=10)
        
        # Status label
        self.status_label = tk.Label(self.root, text="Ready", bg="#f0f0f0")
        self.status_label.pack()
    
    def browse_backup_file(self):
        """Browse and select backup file"""
        file_path = filedialog.askopenfilename(
            title="Select Backup File",
            filetypes=[("WIM Files", "*.wim"), ("All Files", "*.*")]
        )
        if file_path:
            self.backup_file.set(file_path)
            self.load_backup_info()
    
    def browse_restore_path(self):
        """Browse and select restore path"""
        folder_path = filedialog.askdirectory(title="Select Restore Path")
        if folder_path:
            self.restore_path.set(folder_path)
        
        # Clear backup information
        self.backup_info = {}
        
        backup_file = self.backup_file.get()
    
    def on_backup_select(self, event):
        """Handle backup selection"""
        selected_items = self.backup_tree.selection()
        if selected_items:
            item = self.backup_tree.item(selected_items[0])
            backup_index = item["values"][0]
            self.selected_backup_index.set(int(backup_index))
    
    def start_restore(self):
        """Start restore process"""
        backup_file = self.backup_file.get()
        restore_path = self.restore_path.get()
        
        if not backup_file:
            messagebox.showerror("Error", "Please select a backup file")
            return
        
        if not restore_path:
            messagebox.showerror("Error", "Please select a restore path")
            return
        
        # Confirm restore operation
        confirm = messagebox.askyesno(
            "Confirm Restore", 
            f"Are you sure you want to restore backup to path '{restore_path}'?\n\n" +
            "Warning: This operation may overwrite existing files."
        )
        
        if not confirm:
            return
        
        # Check if target path exists, create if not
        if not os.path.exists(restore_path):
            try:
                os.makedirs(restore_path)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create target directory: {str(e)}")
                return
        
        # Disable buttons to prevent duplicate operations
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, tk.Button):
                        child.config(state=tk.DISABLED)
        
        # Update status
        self.status_label.config(text="Initializing restore...")
        self.progress['value'] = 0
        self.root.update_idletasks()
        
        try:
            # Initialize restore object
            if not self.restore_obj:
                self.restore_obj = WimRestore()
            
            self.status_label.config(text="Restoring backup...")
            
            # Execute restore
            print(backup_file, restore_path)
            success = WimRestore.RestoreWim(restore_path,backup_file,autoRecoveryAllBackupFiles=False,autoRestoreBackupsToPath=False,checkHash=False)
            
           
            self.status_label.config(text="Restore completed")
            messagebox.showinfo("Success", "Backup has been successfully restored")
                
        except Exception as e:
            self.status_label.config(text="Restore failed")
            messagebox.showerror("Error", f"An error occurred during restore: {str(e)}")
        finally:
            # Restore button states
            for widget in self.root.winfo_children():
                if isinstance(widget, tk.Frame):
                    for child in widget.winfo_children():
                        if isinstance(child, tk.Button):
                            child.config(state=tk.NORMAL)
    
    def update_progress(self, value):
        """Update progress bar"""
        self.progress['value'] = value
        self.status_label.config(text=f"Restoring backup... {value}%")
        self.root.update_idletasks()

if __name__ == "__main__":
    root = tk.Tk()
    app = RestoreUI(root)
    root.mainloop()
