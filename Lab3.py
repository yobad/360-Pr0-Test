import network 
import time 


SSID:str = "Your team name's Pico"
PASSWORD:str = "ChangeMe123"

def create_access_point(ssid=SSID, password=PASSWORD, TIMEMOUT=5):
    """This function create a local wifi access point for clients to connect 
    to the Pico W
    """
    access_point = network.WLAN(network.AP_IF)
    access_point.config(essid=SSID, password=PASSWORD)
    access_point.active(True)

    time_left = TIMEMOUT
    while (not access_point.active() and TIMEMOUT>0):
        time.sleep(1)
        time_left-=1
    
    if access_point.active():
       ip_address= access_point.ifconfig()[0]
       print(f"Access Point sucessfully created: //{ip_address}")
    else:
         #timeout without proper connection 
        raise Exception("The pico failed to create an access point")


def html_page(led_status:bool):
    return f"""
            <html>
             <div><Welcome to {SSID} Local Network/div>
             <div>LED</div>
             <Button></Button>
            </html>
            """

if __name__ == "__main__":
    create_access_point()