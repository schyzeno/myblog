import os
import binascii
s=binascii.hexlify(os.urandom(24))
print(s)

