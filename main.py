# TV B Gone for Raspberry Pi Pico
# Adapted from https://github.com/bikeNomad/micropython-tv-b-gone (Ned Konz, Public Domain)
#
# Hardware pin mapping (from original badge main.py):
#   IR output  : GPIO 18 (mod)     - IR LED/transistor via PWM at 38 kHz
#   Trigger    : GPIO 14 (sw1push) - press to start sending all codes
#   Cancel     : GPIO 22 (sw2push) - press mid-run to abort
#   Status LED : GPIO 25 (LED0)    - onboard Pico LED

import machine
import utime
import gc
from codes import CODES

# --- Hardware init ---

ir_pwm = machine.PWM(machine.Pin(18, machine.Pin.OUT, value=0))
ir_pwm.freq(38000)
ir_pwm.duty_u16(0)

# Buttons use internal pull-ups; active LOW (press = 0).
# If your badge has external pull-downs and active-HIGH buttons,
# flip the .value() checks below to `== 1`.
trigger = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP)  # sw1push
cancel  = machine.Pin(22, machine.Pin.IN, machine.Pin.PULL_UP)  # sw2push

led = machine.Pin(25, machine.Pin.OUT, value=0)  # onboard LED

# --- IR transmission ---

def ir_mark(us):
    """Transmit 38 kHz carrier burst for `us` microseconds."""
    ir_pwm.duty_u16(32768)  # ~50% duty cycle
    utime.sleep_us(us)

def ir_space(us):
    """Silence (no carrier) for `us` microseconds."""
    ir_pwm.duty_u16(0)
    utime.sleep_us(us)

def send_code(code):
    """Send one IR code sequence.
    code format: (name_str, on_us, off_us, on_us, off_us, ...)
    """
    pulses = code[1:]
    for i, duration in enumerate(pulses):
        if i % 2 == 0:
            ir_mark(duration)
        else:
            ir_space(duration)
    ir_pwm.duty_u16(0)  # ensure carrier is off after code

def send_all_codes():
    """Cycle through every code in CODES.
    Toggle LED on each code. Press cancel (sw2push) to abort early.
    """
    total = len(CODES)
    print("Sending", total, "codes...")
    for i, code in enumerate(CODES):
        if cancel.value() == 0:  # active LOW
            print("Cancelled at", code[0])
            break
        print(code[0], str(i + 1) + "/" + str(total))
        led.toggle()
        send_code(code)
        gc.collect()
    ir_pwm.duty_u16(0)
    led.value(0)

# --- Startup blink ---

def blink(n, on_ms=100, off_ms=100):
    for _ in range(n):
        led.value(1)
        utime.sleep_ms(on_ms)
        led.value(0)
        utime.sleep_ms(off_ms)

blink(3)
print("TV B Gone ready.")
print("  sw1push (GPIO 14) = start")
print("  sw2push (GPIO 22) = cancel")

# --- Main loop ---

while True:
    if trigger.value() == 0:  # active LOW: button pressed
        utime.sleep_ms(20)    # debounce
        if trigger.value() == 0:
            blink(1, on_ms=200)
            send_all_codes()
            blink(5, on_ms=50, off_ms=50)  # done pattern
    utime.sleep_ms(20)
