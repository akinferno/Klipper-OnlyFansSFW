# Klipper-OnlyFansSFW
Repository to create a fan/temperature management system for 3d printers. 

Goals for the project:
- Create a global fan_rate variable, so you can adjust fans during a print, similar to flow adjustment. (This was easy and is working, but want to add a slider for it).
- Evaluate chamber temp on Print_start. If chamber temp is set above 40C, heatsoak, then start print, but soak should be overridable. (Think I have this working too, but want to improve it. Before print starts, hotend and part fan should be managed to set chamber temp, but not during the print.)
- During the print, adjust bed fans, exhaust fans and/or chamber heater, to try to keep chamber at + or - 5C. (This is monitoring and making changes, but not in a useful manner without PID tuning, which would change based on hotend temp, bed temp and part fan. So want incorporate PID tuning directly into it.)
- Be easily configurable. Each of my printers is totally different and I want it to work on them all.
