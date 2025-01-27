import canopen
import time
from canopen.profiles.p402 import BaseNode402

network = canopen.Network()
network.connect(channel='vcan0', interface='socketcan')
network.sync.start(0.01) # Transmit sync message every 10 ms

encoder_node = canopen.LocalNode(2, 'eds_files/HTB_FHB_PM_CA_2021-02-24.eds')
motor_node = BaseNode402(3, 'eds_files/Eds1406C.eds')

network.add_node(encoder_node)
network.add_node(motor_node)

for node_id in network:
    print(network[node_id])

# Get the Object Dictionary of a node
# for obj in encoder_node.object_dictionary.values():
#     print(f'0x{obj.index:X}: {obj.name}')
#     if isinstance(obj, canopen.objectdictionary.ODRecord):
#         for subobj in obj.values():
#             print(f'  {subobj.subindex}: {subobj.name}')

# device_type = motor_node.sdo[0x1000]
# print(f"The device type is 0x{device_type.raw:X}")


time.sleep(10)


network.sync.stop()
network.disconnect()
