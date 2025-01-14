# Klipper-OnlyFansSFW
Repository to create a fan/temperature management system for 3d printers. 

* Not currently working with toolchanger. Testing all of this on my V0, which has bed fans only. I want to get that working before adding exhaust fans and chamber heating to the mix.

Goals for the project:
- Create a global fan_rate variable, so you can adjust fans during a print, similar to flow adjustment. (This was easy and is working, but want to add a slider for it).
- Evaluate chamber temp on Print_start. If chamber temp is set above 40C, heatsoak, then start print, but soak should be overridable. (Think I have this working too, but want to improve it. Before print starts, hotend and part fan should be managed to set chamber temp, but not during the print.)
- During the print, adjust bed fans, exhaust fans and/or chamber heater, to try to keep chamber at + or - 5C. (This is monitoring and making changes, but not in a useful manner without PID tuning, which would change based on hotend temp, bed temp and part fan. So want incorporate PID tuning directly into it.)
- Be easily configurable. Each of my printers is totally different and I want it to work on them all.

-----------------------

***Dynamic Fan speed Adjustment***

Worked with @speedkills from the Voron and FLSUN servers. Came up with a way to dynamically adjust fan speed with a multiplier, in Fluidd or Mainsail. The commands override the M106 variable so when Gcode sends a fan speed, it is first multiplied by the multiplier before executing the change. This would make the fans dynamically adjustable, inbthe same way the "Speed" slider adjusts the individual Gcode moves from the calculated values in gcode via slider. 

You will need ssh access to add the virtual pin which provides a slider in Fluidd and Mainsail. But the macro can be used on it's own without the slider. 

Example: If you drastically change the print speed and want to change the fan to compensate, set fan multiplier to %50, and the 60% fan command in gcode becomes 30%.  

```
#Install klipper-virtual-pins
cd ~
git clone https://github.com/pedrolamas/klipper-virtual-pins.git
./klipper-virtual-pins/install.sh

#add virtual pin to printer.cfg
[virtual_pins]

[output_pin fan_multiplier]
pin: virtual_pin:fan_multiplier
pwm: True
value: 1.0


#Configure M106 to use fan_multiplier
[gcode_macro M106]
rename_existing: M106.1
gcode:
  {% set S = params.S|default(0)|int %}
  {% set P = params.P|default(0)|int %}
  {% set MULTIPLIER = printer['output_pin fan_multiplier'].value %}
  {% set ADJUSTED_S = (S * MULTIPLIER)|round(0)|int %}
  M106.1 P{P} S{ADJUSTED_S}

```