from getmac import get_mac_address

def createEUI():
    macAddr     = get_mac_address(interface="Ethernet")
    macArray    = macAddr.split(':')

    macArray.insert(3, 'ff')
    macArray.insert(4, 'fe')

    flipBit = bin(int(macArray[0], base=16)).split('0b')[1]
    if flipBit[-2] == '0':
        flipBit = flipBit[:-2] + '1' + flipBit[-1]
    else:
        flipBit = flipBit[:-2] + '0' + flipBit[-1]

    flipBit     = hex(int(flipBit, base=2)).split('0x')[1]
    macArray[0] = flipBit
    ipvsix      = macArray[0] + macArray[1] + ':' + macArray[2] + macArray[3] + ':' + macArray[4] + macArray[5] + ':' + macArray[6] + macArray[7]
    return ipvsix

print('The link-local-address for your host based on eui-64 is: ' + createEUI())