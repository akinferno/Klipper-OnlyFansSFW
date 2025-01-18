from klippy import server
from klippy.extras import profile_extras
from klippy.log import logger

# Define a global variable to store the previous fan factor value
previous_fan_factor = 1.0

@server.on_event("klippy_started")
def on_klippy_started():
    """
    Initialize the previous fan factor value when Klippy starts.
    """
    global previous_fan_factor
    previous_fan_factor = printer['output_pin fan_factor'].value

@server.on_event("printer_objects_ready")
def on_printer_objects_ready():
    """
    Register the fan factor change observer.
    """
    printer.register_event_handler("output_pin_changed", on_output_pin_changed)

def on_output_pin_changed(event_type, event_data):
    """
    This function is called whenever an output pin value changes.
    It checks if the fan factor has changed and updates the fan speed accordingly.
    """
    global previous_fan_factor
    current_fan_factor = printer['output_pin fan_factor'].value

    if current_fan_factor != previous_fan_factor:
        # Update the fan speed
        logger.info("Fan factor changed, updating fan speed...")
        # Get the current fan speed (if any)
        current_fan_speed = printer.lookup_object('extruder').cool_fan.speed
        # Calculate the new fan speed based on the multiplier
        new_fan_speed = current_fan_speed * current_fan_factor
        # Set the new fan speed
        printer.lookup_object('extruder').cool_fan.speed = new_fan_speed
        # Update the previous fan factor
        previous_fan_factor = current_fan_factor

# Register the hooks
server.register_event_handler("klippy_started", on_klippy_started)
server.register_event_handler("printer_objects_ready", on_printer_objects_ready)
