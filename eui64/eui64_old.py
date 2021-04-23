from getmac import get_mac_address

win_mac     = get_mac_address(ip="192.168.0.6")
macArray    = win_mac.split(':')
ipvsix      = []
counter     = 0

for block in macArray:
    if counter == 3:
        ipvsix.append('ff')
        ipvsix.append('fe')

    ipvsix.append(block)
    counter += 1

hexIntBin       = int(ipvsix[0], base=16)
hexIntBin       = bin(hexIntBin)
hexIntBin       = hexIntBin.split('0b')
hexIntBin       = hexIntBin[1]

if hexIntBin[-2] == '1':
    hexIntBin = hexIntBin[:-2] + '0' + hexIntBin[-1]
else:
    hexIntBin = hexIntBin[:-2] + '1' + hexIntBin[-1]

hexIntBin       = hex(int(hexIntBin, base=2)).split('0x')[1]
ipvsixArray     = ipvsix
ipvsixArray[0]  = hexIntBin
counter         = 0
linkLocal       = ''
ipvsixBlock     = ''


for block in ipvsixArray:
    if counter % 2 == 0:
        if counter == 0:
            ipvsixBlock = block
        else:
            ipvsixBlock = ':' + block
    else:
        ipvsixBlock     += block
        linkLocal       += ipvsixBlock
        ipvsixBlock     = ''
    counter += 1

print(linkLocal)