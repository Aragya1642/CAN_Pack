import canopen
import time
from canopen.profiles.p402 import BaseNode402

def setup_motor_pdo_mappings(motor_node):
    motor_node.tpdo.read()
    motor_node.rpdo.read()
    
    # TPDO 1 - Default
    motor_node.tpdo[1].clear()
    motor_node.tpdo[1].trans_type = 255
    motor_node.tpdo[1].inhibit_time = 0
    motor_node.tpdo[1].add_variable('Statusword')
    motor_node.tpdo[1].enabled = True

    # TPDO 2 - Default (not gonna touch because binary interpreter)

    # TPDO 3 - Custom
    motor_node.tpdo[3].clear()
    motor_node.tpdo[3].trans_type = 1
    motor_node.tpdo[3].add_variable('Velocity Sensor Actual Value')
    motor_node.tpdo[3].enabled = True

    # TPDO 4 - Custom
    # motor_node.tpdo[4].clear()

    # RPDO 1 - Default
    motor_node.rpdo[1].clear()
    motor_node.rpdo[1].trans_type = 255
    motor_node.rpdo[1].add_variable('Controlword')
    motor_node.rpdo[1].enabled = True

    # RPDO 2 - Default (not gonna touch because binary interpreter)

    # RPDO 3 - Default
    motor_node.rpdo[3].clear()
    motor_node.rpdo[3].trans_type = 255
    motor_node.rpdo[3].add_variable('Target Velocity')
    motor_node.rpdo[3].enabled = True

    # RPDO 4
    # motor_node.rpdo[4].clear()


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
network.sync.start(1)

# Network Initialization Stage
print_system_states(network, motor1)

# Network Pre Op Stage
network.nmt.state = 'PRE-OPERATIONAL'
motor1.op_mode = 'PROFILED VELOCITY'
setup_motor_pdo_mappings(motor1)
motor1.tpdo.save()
motor1.rpdo.save()
print_system_states(network, motor1)

# Network Operational Stage
network.nmt.state = 'OPERATIONAL'
motor1.state = 'READY TO SWITCH ON'
motor1.state = 'SWITCHED ON'
motor1.state = 'OPERATION ENABLED'
print_system_states(network, motor1)

# Command the motor to spin by sending a target velocity.
target_velocity = 80000  # change this value as needed
print(f"Setting target velocity to {target_velocity}")
motor1.rpdo[3]['Target Velocity'].raw = target_velocity
motor1.rpdo[3].transmit()
# motor1.sdo[0x60FF].raw = target_velocity

try:
    while True:
        print(motor1.sdo[0x60FF].raw)
        time.sleep(2)

except KeyboardInterrupt:
    motor1.sdo[0x60FF].raw = 0
    # motor1.op_mode = 'NO MODE'
    motor1.state = 'SWITCH ON DISABLED'
    print_system_states(network, motor1)
    network.sync.stop()
    network.nmt.state = 'INITIALISING'
    print("------------------------------")
    print(f"Network State: {network.nmt.state}")
    network.disconnect()