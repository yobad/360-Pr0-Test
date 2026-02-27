"""
Lab 1: LED Blink Sequence with Morse Code
Author: Youmna Badawy
Date: Jan 23, 2026
Description: This script blinks the Pico's built-in LED according to the morse code representation of a user-provided message.
"""
from machine import Pin
import time

# Defining all the constants 
MORSE_CODE: dict = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..',
    '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....',
    '6': '-....', '7': '--...', '8': '---..', '9': '----.', '0': '-----',
    ' ': '/' # Space between words is often represented by a single slash
}

LED_PIN:int = 16
SHORT_BLINK: float =0.2
LONG_BLINK: float = 3*SHORT_BLINK
BETWEEN_LETTERS: float = LONG_BLINK
BETWEEN_WORDS: float = 7*SHORT_BLINK

# Global variables
led = Pin('LED', Pin.OUT)


# Functions
def blink_led(delay:float):
    """Blinks the LED for a given duration in seconds"""
    led.on()
    time.sleep(delay)
    led.off()


def blink_morse(code:str):
    """Blink the LED according to the given Morse code string ex: '-.-.' """
    for symbol in code:
        if symbol == '.':
            blink_led(SHORT_BLINK)
        elif symbol == '-':
            blink_led(LONG_BLINK)
        elif symbol == '/':
            time.sleep(BETWEEN_WORDS)  # Longer pause for space between words
        time.sleep(SHORT_BLINK)  # Pause between symbols

def main():
    
    # Main loop 
    while True:
        message = input("Enter a message to blink (short and long blinks) or -1 to exit: ")

        print(message)
        print()
        if message == "-1": # Part added to exit the infinite loop when user inputs -1
            led.off()
            print("Bye Bye!")
            break
            
        print()
        print("Starting LED blink sequence...")
        # Processing each character in the message 
        for character in message:
            morse = MORSE_CODE[character.upper()] #Finds each letter in the dictionary
            print(f"{character} => {morse}") #For debugging purposes 
            blink_morse(morse)
            time.sleep(BETWEEN_WORDS)  # Pause between characters




# Entry point
if __name__ == "__main__":
    main()