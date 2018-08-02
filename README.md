# CircuitPython Watch

This is sort of CircuitPlayground Express clone with Neopixel ring and RTC DS3231.

Goal of this board is make real working watch for Maker Faire Prague (MFP) which can children age of 10+ years make at workshop and which can after that use to learn Circuitpython.   

Sadly we encountered some issues at MFP with assembly of the board, so just 2 watches were made. 

Until now, there were 2 revisions of the board: 

version A: 
- I2C was routed to wrong pins
- VCC was split in 2 signals in schematic so I have to connect them at board with wire
- VBAT was connected to 5V so if I tryed to charge battery there was to much voltage and battery did not charge
- it has not SWDIO & SWCLK pins so I had to solder wires to the pins of the CPU to burn the bootloader
	
version B:
- board is working & ready for MFP
	
Description of the board:
- uses ATSAMD21G18 like CPX
- uses AP131 voltage regulator (5V -> 3.3V)
- uses MCP73831 for battery charging
- uses DS3231 for RTC
- uses UF2 bootloader
- uses micro USB connector for charging & data transfer
- uses 12 WS2812B RGB diodes to schow time
	
Description of usage:

There are 2 touch buttons on the board. 

Button A is "Time button", when is pressed, it will show hours by blue color on RGB LEDs and minutes by green color. Every minute is schowed by 1 blink of green color. 

Button B is  "Mode button", when is pressed, it will increase counter by 1 and it will schow predefined animation from main.py .

Function is showed in gif bellow, in loop with all default animations. 
<p>
<a href="https://imgflip.com/gif/2f5eqi"><img src="https://i.imgflip.com/2f5eqi.gif" title="made at imgflip.com"/></a>
</p>
