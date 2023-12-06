import sys
import time
from intelhex import IntelHex

# Check if a file path was provided as an argument
if len(sys.argv) < 2:
    print("Usage: python generate_data.py <hex_file>")
    sys.exit(1)

# Read the hex file using the IntelHex library
ih = IntelHex()
ih.loadhex(sys.argv[1])

# Get the start address and data as a list of bytes
start_address = ih.minaddr()
data = ih.tobinarray(start=start_address)

# If data is an odd number of bytes, make it even
if len(data) % 2 != 0:
    data.append(0xFF)

print(f"Length: {len(data)}")
print(f"Start address: {start_address}")

# Generate the bootloader_data.c file
with open("bootloader_data.c", "w") as file:
    file.write("// This file contains the bootloader data itself and the address to install the bootloader at\n")
    file.write("// Use generate-data.py to generate these values from a hex file\n")
    file.write(f"// Generated from {sys.argv[1]} at {time.ctime()}\n\n")
    file.write(f"const uint16_t bootloader_data[{len(data) // 2}] PROGMEM = {{\n")
    for i in range(0, len(data), 2):
        word = (data[i+1] << 8) + data[i] if i+1 < len(data) else data[i]
        file.write(f"    0x{word:04X},\n")
    file.write("};\n\n")
    file.write(f"const uint16_t bootloader_address = {start_address};\n") 
