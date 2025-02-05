import canopen
import time
from canopen.profiles.p402 import BaseNode402

def print_system_states(network, motor_node):
    op_mode_disp = motor_node.sdo['Modes Of Operation Display']

    print("------------------------------")
    print(f"Network State: {network.nmt.state}")
    print(f"State Machine State: {motor_node.state}")
    print(f"Operation Mode: {op_mode_disp.read()}")

def setup_network():
    network = canopen.Network()
    network.connect(channel='can0', interface='socketcan')
    return network

def add_motor(network, node_num):
    motor_node = BaseNode402(node_num, 'eds_files/Eds1406C.eds')
    network.add_node(motor_node)
    return motor_node

network = setup_network()
motor1 = add_motor(network, node_num=3)

# Network Initialization Stage
print_system_states(network, motor1)

# Network Pre Op Stage
network.nmt.state = 'PRE-OPERATIONAL'
motor1.op_mode = 'PROFILED VELOCITY'
print_system_states(network, motor1)


# Network Operational Stage
network.nmt.state = 'OPERATIONAL'
print_system_states(network, motor1)

try:
    while True:
        pass
except KeyboardInterrupt:
    motor1.op_mode = 'NO MODE'
    print_system_states(network, motor1)
    network.nmt.state = 'INITIALISING'
    print("------------------------------")
    print(f"Network State: {network.nmt.state}")
    network.disconnect()