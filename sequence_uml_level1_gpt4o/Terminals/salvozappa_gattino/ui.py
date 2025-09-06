proj_clean/src/ui.py
import sys
import time
import threading


class Spinner:
    """
    Provide a visual spinner animation in the terminal to indicate ongoing background processes, 
    particularly while waiting for a subprocess to complete.
    """
    
    def __init__(self):
        """
        Initialize an instance with a list of frame characters and set the starting index to 0.
        """
        self.frames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        self.index = 0
    
    def next_frame(self):
        """
        Retrieve the next frame in a sequence of frames, cycling back to the first frame after the last one is reached.
        """
        frame = self.frames[self.index]
        self.index = (self.index + 1) % len(self.frames)
        return frame
    
    def show(self, process):
        """
        Display an animated sequence in the terminal while a subprocess is running, 
        updating the animation frame at regular intervals until the process completes.
        """
        while process.poll() is None:
            sys.stdout.write(f'\r{self.next_frame()} Processing... ')
            sys.stdout.flush()
            time.sleep(0.1)
        sys.stdout.write('\r' + ' ' * 20 + '\r')
        sys.stdout.flush()


def show_spinner(process):
    """
    Display a spinner animation while a subprocess is running to indicate ongoing activity.
    """
    spinner = Spinner()
    spinner.show(process)


def print_input_line():
    """
    Prompt the user for input by displaying a menu question and returning the entered text.
    """
    return input("What would you like to do? ")


def print_intro():
    """
    https://www.asciiart.eu/animals/cats
    http://patorjk.com/software/taag/#p=display&f=Calvin%20S&t=gattino
    """
    ascii_art = r"""
 /\_/\  
( o.o ) 
 > ^ < 
    """
    
    banner = r"""
   _____       _ _   _       
  / ____|     (_) | (_)      
 | |  __  __ _ _| |_ _  ___  
 | | |_ |/ _` | | __| |/ _ \ 
 | |__| | (_| | | |_| | (_) |
  \_____|\__,_|_|\__|_|\___/ 
    """
    
    print(ascii_art)
    print(banner)
    print("Welcome to Gattino - Your AI-powered command assistant!")
    print("Type your natural language command and I'll convert it to bash magic!")
    print("=" * 60)