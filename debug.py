import canopen
import time
from canopen.profiles.p402 import BaseNode402

network = canopen.Network()
network.connect(channel='can0', interface='socketcan')

motor_node = BaseNode402(3, 'eds_files/Eds1406C.eds')
network.add_node(motor_node)

print(motor_node.nmt.state)
motor_node.nmt.state = 'PRE-OPERATIONAL'
motor_node.setup_pdos()
print(motor_node.nmt.state)
print(motor_node.state)


try:
    while True:
        pass
except KeyboardInterrupt:
    network.disconnect()
