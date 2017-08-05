import usb.core
import usb.util
import struct
import sys
dev = usb.core.find(idVendor=0x0416, idProduct=0x5020)

if dev is None:
    print('Vape not connected')
    sys.exit(0)

reattach = False
if dev.is_kernel_driver_active(0):
    reattach = True
    dev.detach_kernel_driver(0)

endpoint_in = dev[0][(0,0)][0]
endpoint_out = dev[0][(0,0)][1]


hid_signature = bytearray(b'HIDC')

def hidcmd(cmdcode, arg1, arg2):
    """Generates a Nuvoton HID command.
    Args:
        cmdcode: A byte long HID command.
        arg1: First HID command argument.
        arg2: Second HID command argument.
    Returns:
        A bytearray containing the full HID command.
    """

    # Do not count the last 4 bytes (checksum)
    length = bytearray([14])

    # Construct the command
    cmdcode = bytearray(struct.pack('=B', cmdcode))
    arg1 = bytearray(struct.pack('=I', arg1))
    arg2 = bytearray(struct.pack('=I', arg2))
    cmd = cmdcode + length + arg1 + arg2 + hid_signature

    # Return the command with checksum tacked at the end
    return cmd + bytearray(struct.pack('=I', sum(cmd)))

def send_command(cmd, arg1, arg2):
    """Sends a HID command to the device.
    Args:
        cmd: Byte long HID command
        arg1: First argument to the command (integer)
        arg2: Second argument to the command (integer)
    """

    command = hidcmd(cmd, arg1, arg2)
    return endpoint_out.write(command)

send_command(0x66,0,64)
data = dev.read(endpoint_in.bEndpointAddress, 64, 1000)

Timestamp = struct.unpack("I", data[0:4])[0]
IsFiring = struct.unpack("?", data[4:5])[0]
IsCharging = struct.unpack("?", data[5:6])[0]
IsCelcius = struct.unpack("?", data[6:7])[0]
Battery1Voltage = struct.unpack("b", data[7:8])[0]
Battery2Voltage = struct.unpack("b", data[8:9])[0]
Battery3Voltage = struct.unpack("b", data[9:10])[0]
Battery4Voltage = struct.unpack("b", data[10:11])[0]
PowerSet = struct.unpack("h", data[11:13])[0]
TemperatureSet = struct.unpack("h", data[13:15])[0]
Temperature = struct.unpack("h", data[15:17])[0]
OutputVoltage =struct.unpack("h", data[17:19])[0]
OutputCurrent = struct.unpack("h", data[19:21])[0]
Resistance = struct.unpack("h", data[21:23])[0]
RealResistance = struct.unpack("h", data[23:25])[0]
BoardTemperature = struct.unpack("b", data[11:12])[0]

if Battery1Voltage != 0:
   Battery1Voltage = (Battery1Voltage + 275) / 100
if Battery2Voltage != 0:
   Battery2Voltage = (Battery2Voltage + 275) / 100
if Battery3Voltage != 0:
    Battery2Voltage= (Battery3Voltage + 275) / 100
if Battery4Voltage != 0:
    Battery4Voltage = (Battery4Voltage + 275) / 100

PowerSet = PowerSet / 10
OutputVoltage = OutputVoltage / 100
OutputCurrent = OutputCurrent / 100
OutputPower = "{00:.2f}".format(OutputVoltage * OutputCurrent)
print("{}W/{}W {}v/{}v {}/{} Ω".format(OutputPower, "{00:.2f}".format(PowerSet), str(OutputVoltage), str(Battery1Voltage), str(RealResistance/10), str(Resistance/10)))
