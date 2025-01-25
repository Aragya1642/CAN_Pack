import canopen

network = canopen.Network()

encoder = network.add_node(2, 'eds_files/HTB_FHB_PM_CA_2021-02-24.eds')
motor = network.add_node(3, 'eds_files/Eds1406C.eds')

