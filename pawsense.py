#!/usr/bin/env python3
from pawsense_tray import PawSenseTray

def main():
    """Main entry point for PawSense"""
    
    print("Starting PawSense...")
    app = PawSenseTray()
    app.run()

if __name__ == "__main__":
    main()
