#!/usr/bin/env python3
"""
Simple Modbus RTU client for an RS485 device.
Requires: pymodbus, pyserial
"""

import sys
from pymodbus.client import ModbusSerialClient as ModbusClient

# ------------------------------------------------------------------
# Configuration – change these to match your device
PORT        = "/dev/ttyUSB0"   # USB‑to‑RS485 adapter
BAUDRATE    = 9600             # often 9600, but check the manual
PARITY      = "E"              # 'N', 'E', or 'O'
STOPBITS    = 1
BYTESIZE    = 8
SLAVE_ID    = 1                # Modbus slave address (often 1)
REGISTER   = 40001             # Holding register number to read
COUNT      = 1                 # Number of registers

# ------------------------------------------------------------------
def main():
    client = ModbusClient(
        # method="rtu",
        port=PORT,
        baudrate=BAUDRATE,
        parity=PARITY,
        stopbits=STOPBITS,
        bytesize=BYTESIZE,
        timeout=2
    )

    if not client.connect():
        print(f"❌  Could not open {PORT}")
        sys.exit(1)

    # Read holding register(s)
    rr = client.read_holding_registers(address=REGISTER-40001, count=COUNT, unit=SLAVE_ID)

    if rr.isError():
        print(f"⚠️  Modbus error: {rr}")
    else:
        value = rr.registers[0]
        print(f"✅  Register {REGISTER} raw value : {value}")

        # Example: interpret as IEEE‑754 float (big endian)
        import struct
        packed = struct.pack(">H", value) + b'\x00\x00'  # pad to 4 bytes
        decoded_float = struct.unpack(">f", packed)[0]
        print(f"      As float          : {decoded_float:.3f}")

    client.close()


if __name__ == "__main__":
    main()
