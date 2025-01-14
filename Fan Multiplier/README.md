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

If you do not want to install virtual pins, or do not have access to SSH, you can use the following instead:
'''
[gcode_macro PART_FAN_VARS]
variable_fan_rate: 1.0
gcode:


[gcode_macro SET_FAN_MULTIPLIER]
gcode:
    {% set MULTIPLIER = params.MULTIPLIER|default(1.0)|float %}
    SET_GCODE_VARIABLE MACRO=PART_FAN_VARS VARIABLE=fan_rate VALUE={MULTIPLIER}


[gcode_macro M106]
rename_existing: M106.1
gcode:
    {% set S = params.S|default(0)|int %}
    {% set P = params.P|default(0)|int %}
    {% set MULTIPLIER = printer["gcode_macro PART_FAN_VARS"].fan_rate %}
    {% set ADJUSTED_S = (S * MULTIPLIER)|round(0)|int %}
    M106.1 P{P} S{ADJUSTED_S}
'''

If you would like a variable to add to your 12864 style display, include these commands also:
'''
[display_status]

[menu __main __control __fan_multiplier]
type: input
name: Fan Rate: {'%.2f' % printer['gcode_macro PART_FAN_VARS'].fan_rate}
input: {printer['gcode_macro PART_FAN_VARS'].fan_rate}
input_min: 0
input_max: 2
input_step: 0.05
gcode:
    SET_FAN_MULTIPLIER MULTIPLIER={'%.2f' % menu.input}
'''
