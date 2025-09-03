import tkinter as tk
import tkinter.font as tkfont
from tkinter import ttk

class PawSenseWindow:
    def __init__(self, on_close_callback=None, on_terminate_callback=None):
        self.on_close_callback = on_close_callback
        self.on_terminate_callback = on_terminate_callback
        self.window = tk.Tk()
        self.window.title("PawSense")
        self.window.withdraw()
        
        # variables
        self.im_a_human = tk.StringVar()
        
        preferred = "Noto Sans"
        available = tkfont.families()
        self.chosen = preferred if any(preferred in f for f in available) else ("DejaVu Sans" if any("DejaVu" in f for f in available) else "TkDefaultFont")
        
        self.setup_window()
        self.create_components()
        
        self.window.protocol("WM_DELETE_WINDOW", self.on_window_close)
    
    def show(self):
        """Show the window"""
        self.window.deiconify()
        self.window.lift()
        self.window.attributes('-topmost', True)
        self.window.focus_force()
    
    def hide(self):
        """Hide the window"""
        self.window.withdraw()
    
    def setup_window(self):
        """Configure window properties"""
        self.window.attributes('-topmost', 1)
        self.window.geometry("700x450")
        self.window.resizable(False, False)
        
        style = ttk.Style()
        style.configure('Paw.TButton', font=(self.chosen, 14))
        style.configure('PawVerify.TButton', font=(self.chosen, 10))
    
    def create_components(self):
        """Create all window components"""
        # top part
        ttk.Label(self.window, text="CAT-LIKE TYPING DETECTED", font=(self.chosen, 32)).pack(pady=(20, 10))
        ttk.Label(self.window, text="To protect other programs, PawSense is diverting keyboard input", font=(self.chosen, 14)).pack(pady=(0, 6))
        ttk.Label(self.window, text="Click the button below to close this window.", font=(self.chosen, 14)).pack(pady=(0, 12))

        top_btn_frame = tk.Frame(self.window)
        top_btn_frame.pack(pady=12)
        ttk.Button(top_btn_frame, text="Let me use the computer!", style='Paw.TButton', command=self.allow_use).pack(padx=8)

        # bottom part
        ttk.Label(self.window, text='You can also exit this window by typing the word "human".', font=(self.chosen, 12)).pack(pady=(100, 0))

        self.entry = ttk.Entry(self.window, textvariable=self.im_a_human)
        self.entry.pack()
        self.entry.bind("<Return>", lambda e: self.check_text())
        
        bottom_btn_frame = tk.Frame(self.window)
        bottom_btn_frame.pack(pady=6)
        ttk.Button(bottom_btn_frame, text="Verify", style='PawVerify.TButton', command=self.check_text).pack(padx=8)
        ttk.Label(self.window, text='If you want to terminate PawSense, type "terminate".', font=(self.chosen, 12)).pack(pady=(0, 6))
    
    def allow_use(self):
        """Allow user to use the computer (close window)"""
        self.on_window_close()
    
    def check_text(self):
        """Check the text entered by user"""
        text = self.entry.get()
        
        if text.lower() == "human":
            self.on_window_close()
            
        if text.lower() == "terminate":
            if self.on_terminate_callback:
                self.on_terminate_callback()
            else:
                # Fallback to regular close if no terminate callback
                self.on_window_close()
    
    def on_window_close(self):
        """Handle window close event"""
        self.hide()
        if self.on_close_callback:
            self.on_close_callback()

def run_standalone():
    """Run the window standalone for testing"""
    root = tk.Tk()
    root.withdraw()
    
    def dummy_callback():
        root.quit()
    
    app = PawSenseWindow(dummy_callback)
    app.show()
    root.mainloop()

if __name__ == "__main__":
    run_standalone()
