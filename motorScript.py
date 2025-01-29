import canopen
import time
from canopen.profiles.p402 import BaseNode402

network = canopen.Network()
network.connect(channel='can0', interface='socketcan')

motor_node = BaseNode402(3, 'eds_files/Eds1406C.eds')
network.add_node(motor_node)

motor_node.nmt.state = 'PRE-OPERATIONAL'
motor_node.setup_402_state_machine()
motor_node.setup_pdos()
motor_node.op_mode = 'PROFILED VELOCITY'
motor_node.nmt.state = 'OPERATIONAL'

motor_node.state = 'NOT READY TO SWITCH ON'
print(motor_node.state)

motor_node.state = 'SWITCHED ON'
print(motor_node.state)

motor_node.state = 'OPERATION ENABLED'
print(motor_node.state)

print(motor_node.op_mode)

try:
    while True:
        print(f"Current velocity: {motor_node.sdo[0x606C].raw} rpm")
        time.sleep(1)

except KeyboardInterrupt:
    print("\nStopping motor...")

    motor_node.state = 'READY TO SWITCH ON'
    print(motor_node.state)
    
network.disconnect()