import hashlib
import secrets
from datetime import datetime
from getmac import get_mac_address

def createSecret():
    return secrets.token_hex()

def peMDFive():
    # EUI-64 bases approach from ../eui64/eui64_shot_ver.py
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
    eui         = macArray[0] + macArray[1] + ':' + macArray[2] + macArray[3] + ':' + macArray[4] + macArray[5] + ':' + macArray[6] + macArray[7]

    nextIID     = ''
    fileName    = 'history_value'
    try:
        f = open(f'{fileName}.txt', 'r')
        nextIID = f.read()
        f.close()
    except:
        print(f'File "{fileName}.txt" not found')

    if not nextIID:
        print('Generating secret with random number for md5-digest')
        secret = createSecret() + eui
    else:
        print('Using history-value "' + nextIID + '" for md5-digest')
        secret = nextIID + eui

    iidHash     = hashlib.md5(secret.encode('utf-8'))
    iidHash     = iidHash.hexdigest()
    iid         = []

    iid.append(iidHash[:16])
    iid.append(iidHash[16:])

    stableStorage   = iid[1] # Theoretically this will be the next input instead of the random secret-value for the md5-digest.
    try:
        print(f'Writing history-value to text-file "{fileName}.txt"')
        f = open(f'{fileName}.txt', 'w')
        f.write(stableStorage)
        f.close()
    except:
        print(f'Something went wrong with writing to file {fileName}.txt')
    
    iid             = iid[0]
    flipBit         = bin(int(iid[:2], base=16)).split('0b')[1]
    flipBit         = flipBit[:-3] + '0' + flipBit[-2:]
    flipBit         = hex(int(flipBit, base=2)).split('0x')[1]
    iid             = flipBit + iid[2:]
    iid             = iid[:4] + ':' + iid[4:8] + ':' + iid[8:12] + ':' + iid[12:16]

    print('\nAs of rfc 3041 chapter 3.2.1 your random interface identifier should be: ' + iid)



def peSHA1():
    macAddr = get_mac_address(interface="Ethernet")
    ntp     = datetime.now(tz=None).strftime('%H:%M:%S') #64 Bit NTP
    secret  = ntp + macAddr
    iidHash = hashlib.sha1(secret.encode('utf-8')).hexdigest()
    iid     = iidHash[:16]
    iid     = iid[:4] + ':' + iid[4:8] + ':' + iid[8:12] + ':' + iid[12:16]

    print('With the use of NTP and MAC-address in a sha1-digest your interface identifier should be: '+ iid)

    
peMDFive()
peSHA1()