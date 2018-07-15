# FabLab CircuitPython Watch

# pripojeni pouzitych knihoven
import time
import board
import busio as io
import adafruit_ds3231
from analogio import AnalogIn
import touchio
import digitalio
import neopixel

# Nastaveni cisla analogoveho pinu pro cteni napeti baterie
analog_in = AnalogIn(board.A1)

# Nastaveni cisel pinu s dotykovymi tlacitky
touch_pad_A = board.A3
touch_pad_B = board.A2

# Nastaveni tlacitek jako objektu z knihovny touchio
touchA = touchio.TouchIn(touch_pad_A)
touchB = touchio.TouchIn(touch_pad_B)

# Vytvoreni LED diody na pinu D13 a nastaveni jako vystupu
led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT

# 12 NeoPixel LED diod) pripojenych na pin D8
NUMPIXELS = 12
pixels = neopixel.NeoPixel(board.D8, NUMPIXELS, brightness=0.1, auto_write=False)

# Vytvoreni I2C instance
i2c = io.I2C(board.SCL, board.SDA)
# Vytvoreni RTC instance
rtc = adafruit_ds3231.DS3231(i2c)

# Barevny mod
barevny_mod = 0
animace_pred_casem = 0
animace_po_casu = 0

if False:   # Pro nastaveni casu zmente podminku na "if True"
    #                      rok, mesic, den, hod, min, sek, wday, yday, isdst
    t = time.struct_time((2018,  06,   24,   11,  45,  55,    0,   -1,    -1))
    print("Cas nastaven na:", t)
    rtc.datetime = t

################### Definice podprogramu ###############
def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 85:
        return (int(pos * 3), int(255 - (pos * 3)), 0)
    elif pos < 170:
        pos -= 85
        return (int(255 - (pos * 3)), 0, int(pos * 3))
    else:
        pos -= 170
        return (0, int(pos * 3), int(255 - pos * 3))

def rainbow_cycle(wait):
    for j in range(0, 255, 2):
        for i in range(len(pixels)):
            idx = int((i * 256 / len(pixels)) + j * 10)
            pixels[i] = wheel(idx & 255)
        pixels.show()
        time.sleep(wait)

def rainbow(wait):
    for j in range(0, 255, 2):
        for i in range(len(pixels)):
            idx = int(i + j)
            pixels[i] = wheel(idx & 255)
        pixels.show()
        time.sleep(wait)

def simpleCircle(wait):
    RED = ((255, 0, 0))
    GREEN = ((0, 255, 0))
    BLUE = ((0, 0, 255))

    for i in range(len(pixels)):
        pixels[i] = RED
        pixels.show()
        time.sleep(wait)
    time.sleep(0.4)

    for i in range(len(pixels)):
        pixels[i] = GREEN
        pixels.show()
        time.sleep(wait)
    time.sleep(0.4)

    for i in range(len(pixels)):
        pixels[i] = BLUE
        pixels.show()
        time.sleep(wait)
    time.sleep(0.4)

def neopixels_clear():
    for p in range(NUMPIXELS):
        pixels[p] = ((0,0,0))
        pixels.show()

# Ziskani napeti z analogoveho pinu
def get_voltage(pin):
    # vraceni hodnoty *2, protoze napeti z baterie je odporovym delicem polovicni
    return (pin.value * 3.33 * 2) / 65536

# Vytvoreni barevneho efektu
def barevny_efekt(cislo):
    if (cislo == 0):
        print('Simple demo')
        pixels[0] = ((150,0,0))
        pixels[3] = ((0,150,0))
        pixels[6] = ((0,0,150))
        pixels[9] = ((150,150,150))
        pixels.show()
        time.sleep(1)
        neopixels_clear()
    if (cislo == 1):
        print('Simple Circle Demo')
        simpleCircle(.01)
        neopixels_clear()
    if (cislo == 2):
        print('Flash Demo')
        pixels.fill((255, 0, 0))
        pixels.show()
        time.sleep(.25)

        pixels.fill((0, 255, 0))
        pixels.show()
        time.sleep(.25)

        pixels.fill((0, 0, 255))
        pixels.show()
        time.sleep(.25)

        pixels.fill((255, 255, 255))
        pixels.show()
        time.sleep(.25)
        neopixels_clear()
    if (cislo == 3):
        print('Rainbow Demo')
        rainbow(.001)
        neopixels_clear()
    if (cislo == 4):
        print('Rainbow Cycle Demo')
        rainbow_cycle(.001)
        neopixels_clear()

def ukaz_cas():
    # Provedeni nastavene animace
    if (animace_pred_casem):
        barevny_efekt(barevny_mod)
    # Nacteni casu do promenne
    t = rtc.datetime
    print("Aktualni cas je {}:{:02}:{:02}".format(t.tm_hour, t.tm_min, t.tm_sec))
    # Hodiny
    # Nacteni poctu hodin po zbytku deleni 12 - cas ma 24h format
    hodiny = t.tm_hour%12;
    # Postupne rozsviceni LEDky s udanou hodinou, modra barva
    for p in range(0, 255, 5):
        pixels[hodiny] = ((0,0,p))
        pixels.show()
    # Pauza po dobu 1 sekundy
    time.sleep(1)
    # Postupne zhasnuti LEDky s udanou hodinou, modra barva
    for p in range(255, 0, -5):
        pixels[hodiny] = ((0,0,p))
        pixels.show()
    # Pauza po dobu 400ms
    time.sleep(0.4)
    # Minuty
    # Nacteni poctu minut do promenne
    minuty = t.tm_min;
    # Nacteni cisla minutoveho policka pomoci deleni 5
    minutyPolicko = int(minuty/5);
    # Postupne rozsviceni LEDky s udanou hodinou, zelena barva
    for p in range(0, 255, 5):
        pixels[minutyPolicko] = ((0,p,0))
        pixels.show()
    # Pauza pred dalsim vykonavanim
    time.sleep(0.4)
    # Bliknuti polickem dle poctu minut
    if (minuty-(minutyPolicko*5) > 0):
        # Bliknuti LED diodou
        pixels[minutyPolicko] = ((0,0,0))
        pixels.show()
        time.sleep(0.4)
        pixels[minutyPolicko] = ((0,255,0))
        pixels.show()
        time.sleep(0.4)
        # Pripadne bliknuti zbytku minut
        for p in range(0, (minuty-(minutyPolicko*5)-1), 1):
            pixels[minutyPolicko] = ((0,0,0))
            pixels.show()
            time.sleep(0.4)
            pixels[minutyPolicko] = ((0,255,0))
            pixels.show()
            time.sleep(0.4)
    # Pokud je pocet minut presne dle policka,
    # rovnou provedeme zhasnuti LED diody
    time.sleep(0.6)
    for p in range(255, 0, -5):
        pixels[minutyPolicko] = ((0,p,0))
        pixels.show()
    # Provedeni nastavene animace
    if (animace_po_casu):
        barevny_efekt(barevny_mod)
########################################################
# Nekonecna smycka
while True:
    # Pri stisku tlacitka A provedeme nasledujici:
    if touchA.value:
        #print("Stisknuto tlacitko A!")
        ukaz_cas()

    # Pri stisku tlacitka B provedeme nasledujici:
    if touchB.value:
        #print("Stisknuto tlacitko B!")
        barevny_mod += 1
        if (barevny_mod > 4):
            barevny_mod = 0
        barevny_efekt(barevny_mod)
        time.sleep(0.5)

    # Nacteni napeti na baterii
    napeti = get_voltage(analog_in)
    # Kontrola nizkeho napeti na baterii
    if (napeti < 3.6):
        # Bliknuti cervenou LED diodou pro vystrahu
        led.value = True
        time.sleep(0.3)
        led.value = False
        time.sleep(0.2)
        print("Baterie ma {} V".format(napeti))
    # Pauza 500ms pred dalsim zavolami while True
    barevny_efekt(0)
    time.sleep(0.5)
    barevny_efekt(1)
    time.sleep(0.5)
    barevny_efekt(2)
    barevny_efekt(3)
    time.sleep(0.5)
    barevny_efekt(4)
    time.sleep(0.5)
    ukaz_cas()
    time.sleep(0.5)