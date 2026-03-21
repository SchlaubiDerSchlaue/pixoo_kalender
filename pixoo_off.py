#!/usr/bin/env python3
"""
Simple script to turn off the Pixoo64 display
"""

from pixoo import Pixoo
from config import PIXOO_IP

def main():
    try:
        # Initialize connection
        pixoo = Pixoo(PIXOO_IP)
        print(f"Connected to Pixoo at {PIXOO_IP}")
        
        # Turn off the screen
        pixoo.set_screen_off()
        print("Screen turned off successfully")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()