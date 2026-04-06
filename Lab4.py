import time
import asyncio
import network
import socket
from machine import Pin, PWM, ADC
from server import * 
MAX_DUTY = 2**16 -1
led = Pin('LED', Pin.OUT)
led_intensity = PWM(Pin(2), freq=1_500, duty_u16=MAX_DUTY)
temperature_sensor = ADC(4)

adc_to_volts = 3.3/(65535.0)

LIGHT_COMMAND = 'light'
TEMPERATURE_COMMAND= 'temperature'
LIGHT_INTENSITY = 'intensity'


def read_temp(conversion=adc_to_volts, max_temp=24, offset=0.706, alpha=0.001721):
    """
    Converts the ADC temperature readings of the built-in temperature
    sensor into degrees celcuis. 
    Source: (Nic Hourcard,  2024)
    Url: https://questdb.com/blog/build-temperature-sensor-raspberry-pi-pico-questdb/
    """
    voltage = temperature_sensor.read_u16() * conversion

    temperature =  max_temp - (voltage-offset) / alpha

    return temperature

def create_ap(ssid, password):
    access_p = network.WLAN(network.AP_IF)
    access_p.config(ssid=ssid, password=password)

    access_p.active(True)

    if access_p.status() != 3: 
        print("Failed to create an access point")
        return
    else:
        print("Successfully connected!")
        ip, _  = access_p.ipconfig('addr4')
        print(f"Access Pico on: http://{ip}/")
        return ip

def create_server_socket(ip_address):
    pass

def read_html(filename):
    html = ""
    with open(filename, 'r') as file:
        html = file.read()
    return html

def process_requests(socket):
    try:
        #print(read_temp())
        conn, addr = socket.accept()
        print(conn)
        client_ip, port = addr 
        print("Got a connection from", client_ip)
        print("Through port: ", port )

        # Generate HTML response
        request = str(conn.recv(1024))

        if "favicon" in request:
            return 
        print(request.split())
        command = request.split()[1]
        print("command",command)

        if LIGHT_COMMAND in command:
            print("Toggling LED")
            current_val = led.value()
            inverted_val = not current_val
            print(current_val, inverted_val, led.value())
            led.value(inverted_val)
        elif LIGHT_INTENSITY in command:
            value = int(command.split('=')[-1])
            print(f"Setting light intensity to {value}%")
            led_intensity.duty_u16(int(MAX_DUTY* value/100))
        else:
            print("Nothing there, just a refresh")
        
        print(f"{read_temp()} C")

        response = create_html() # Created in Step 2

        print(conn)
        # Send the HTTP response and close the connection
        conn.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        conn.send(response)
        conn.close()

    except OSError as e:
        conn.close()
        print('Connection closed')

def create_html():
    led_state = "ON" if led.value() else "OFF"
    temperature = read_temp()
    html = f"""
    <html>
        <head>
            
            <h1 style="font-size: 38px; font-family: Arial, Helvetica, sans-serif; text-align: center;">
                Welcome to the Pico Network!
            </h1>
        </head>

        <div style="text-align:center;">
            <p style="font-size: 22px; font-family: Arial, Helvetica, sans-serif; text-align: center;"> 
                LED: <strong>{led_state}</strong>
            </p>
            <form action="./{LIGHT_COMMAND}">
                <button type="submit">Toggle Light</button>
            </form>
            <p style="font-size: 22px; font-family: Arial, Helvetica, sans-serif; text-align: center;">
                Temperature: <strong>{temperature:.2f}<string> °C
            </p>
            <form action="./{TEMPERATURE_COMMAND}">
                <button type="submit">Update</button>
            </form>
            <form action="./{LIGHT_INTENSITY}">
                <label for="intensity">Light intensity (0-100%):</label>
                <input type="range" name="{LIGHT_INTENSITY}" min="0" max="100" step="5">
                <button type="submit">Apply intensity</button>
            </form>

        </form>
        </div>
        
    </html>
        """
    return html 

if __name__ == "__main__":
    server = HTTPServer()

    ip = create_ap("Pico", "Password123")

    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen()  #starts listening to incoming requests.
    while True:
        try:
            process_requests(s)     
        except Exception as error:
            print("An unknown error occured")
            print(error)
            continue