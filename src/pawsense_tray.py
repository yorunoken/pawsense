import pystray
import threading
import random
import tkinter as tk
from PIL import Image, ImageDraw
from pawsense_window import PawSenseWindow

class PawSenseTray:
    def __init__(self):
        self.window = None
        self.icon = None
        self.running = True
        self.root = None
        
        # Create a simple paw icon
        self.create_icon_image()
        
    def create_icon_image(self):
        """Create a simple paw icon for the system tray"""
        image = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        draw.ellipse([20, 35, 44, 55], fill=(0, 0, 0, 255))
        
        draw.ellipse([15, 20, 25, 30], fill=(0, 0, 0, 255))
        draw.ellipse([28, 15, 38, 25], fill=(0, 0, 0, 255))
        draw.ellipse([41, 20, 51, 30], fill=(0, 0, 0, 255))
        
        self.icon_image = image
        
    def show_window(self, icon=None, item=None):
        """Show the PawSense window"""
        if self.root:
            self.root.after(0, self._show_window_main_thread)
    
    def _show_window_main_thread(self):
        """Show window"""
        try:
            if self.window is None:
                self.window = PawSenseWindow(
                    on_close_callback=self.hide_window, 
                    on_terminate_callback=self.terminate_application
                )
            self.window.show()
        except Exception as e:
            print(f"Error showing window: {e}")
    
    def hide_window(self):
        """Hide the window (called when window is closed)"""
        if self.window:
            self.window.hide()
    
    def terminate_application(self):
        """Terminate the entire application (called when 'terminate' is entered)"""
        self.exit_application()
    
    def exit_application(self, icon=None, item=None):
        """Exit the application completely"""
        self.running = False
        if self.root:
            self.root.after(0, self._exit_main_thread)
    
    def _exit_main_thread(self):
        """Actually exit (runs on main thread)"""
        if self.window and self.window.window.winfo_exists():
            self.window.window.destroy()
        if self.root:
            self.root.quit()
        if self.icon:
            self.icon.stop()
    
    def schedule_random_popup(self):
        """Schedule the next random popup"""
        if self.running and self.root:
            wait_time = random.randint(1000 * 60 * 1, 1000 * 60 * 6)
            self.root.after(wait_time, self._random_popup_callback)
    
    def _random_popup_callback(self):
        """Callback for random popup (runs on main thread)"""
        if self.running:
            try:
                if self.window is None or self.window.window.state() == 'withdrawn':
                    self._show_window_main_thread()
            except:
                pass
            
            self.schedule_random_popup()
    
    def run(self):
        """Start the system tray application"""
        self.root = tk.Tk()
        self.root.withdraw()
        
        menu = pystray.Menu(
            pystray.MenuItem("Show Window", self.show_window, default=True),
            pystray.MenuItem("Exit", self.exit_application)
        )
        
        self.icon = pystray.Icon(
            "PawSense",
            self.icon_image,
            "PawSense - Cat Detection",
            menu=menu
        )
        
        self.schedule_random_popup()
        
        self.root.after(1000, self._show_window_main_thread)  # show after 1 second
        
        icon_thread = threading.Thread(target=self.icon.run, daemon=True)
        icon_thread.start()
        
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.exit_application()

if __name__ == "__main__":
    app = PawSenseTray()
    app.run()
