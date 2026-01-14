"""
Lab 1: LED Blink Sequence with Morse Code
Name 1: 
Name 2: 
Date: 
Description: This script blinks the built-in LED according to the morse code representation of a user-provided message.
"""
from machine import Pin
import time

MORSE_CODE = {
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
SHORT_BLINK: float = 1.0
LONG_BLINK: float = 3*SHORT_BLINK
BETWEEN_LETTERS: float = LONG_BLINK
BETWEEN_WORDS: float = 7*SHORT_BLINK


led = Pin(LED_PIN, Pin.OUT)


def short_blink():
    """Blink the LED for a short duration."""
    led.on()
    time.sleep(SHORT_BLINK)
    led.off()


def long_blink():
    """Blink the LED for a long duration."""
    led.on()
    time.sleep(LONG_BLINK)
    led.off()


def blink_morse_code(code):
    """Blink the LED according to the given Morse code string."""
    for symbol in code:
        if symbol == '.':
            short_blink()
        elif symbol == '-':
            long_blink()
        elif symbol == '/':
            time.sleep(BETWEEN_WORDS)  # Longer pause for space between words
        time.sleep(SHORT_BLINK)  # Pause between symbols

def main():
    print("Starting LED blink sequence...")
    while True:

        # YOUR CODE STARTS HERE
        message = input("Enter a message to blink (short and long blinks): ")

        print(message)
        if message == "-1":
            led.off()
            print("LED blink sequence finished.")
            break
        for character in message:
            morse = MORSE_CODE[character.upper()]
            blink_morse_code(morse)
            time.sleep(BETWEEN_WORDS)  # Pause between characters





if __name__ == "__main__":
    main()