import sys
import arcticfox.device

MyDevice = arcticfox.device.Arcticfox()

try:
    MyDevice.connect()
except RuntimeError:
    print("Vape not connected.")
    sys.exit(0)

data = MyDevice.readMonitoringData()

if data['IsFiring']:
    print("{}W/{}W {}v/{}v {}/{}Ω".format(data['OutputPower'], "{00:.2f}".format(data['PowerSet']), str(data['OutputVoltage']), str(data['Battery1Voltage']), str(data['RealResistance']/10), str(data['Resistance']/10)))
else:
    print("{}W {}v {}/{}Ω".format("{00:.2f}".format(data['PowerSet']),str(data['Battery1Voltage']), str(data['RealResistance']/10), str(data['Resistance']/10)))
