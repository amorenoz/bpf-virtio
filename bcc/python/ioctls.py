
NRBITS = 8
TYPEBITS = 8

# TODO: may be arch dependent
SIZEBITS = 14
DIRBITS = 2

NRMASK = (1 << NRBITS) - 1
TYPEMASK = (1 << TYPEBITS) - 1
SIZEMASK = (1 << SIZEBITS) - 1
DIRMASK = (1 << DIRBITS) - 1

NRSHIFT = 0
TYPESHIFT = NRSHIFT + NRBITS
SIZESHIFT = TYPESHIFT + TYPEBITS
DIRSHIFT = SIZESHIFT + SIZEBITS

# TODO: may be arch dependent
NONE = 0x0
WRITE = 0x1
READ = 0x2

IN = WRITE << DIRSHIFT
OUT = READ << DIRSHIFT
INOUT = (WRITE | READ) << DIRSHIFT
IOCSIZE_MASK = SIZEMASK << SIZESHIFT
IOCSIZE_SHIFT = SIZESHIFT

def IO( _type, nr):
    return IOC(NONE, _type, nr, 0)

def IOC(direction, _type, nr, size):
    return (direction << DIRSHIFT) | (_type << TYPESHIFT) | (nr << NRSHIFT) | (size << SIZESHIFT)

def IOR( _type, nr, size):
    return IOC(READ, _type, nr, size)

def IOW(_type, nr, size):
    return IOC(WRITE, _type, nr, size)

def IOWR(_type, nr, size):
    return IOC(READ|WRITE, _type, nr, size)

def IOR_BAD(_type, nr, size):
    return IOC(READ, _type, nr, size)

def IOW_BAD(_type, nr, size):
    return IOC(WRITE, _type, nr, size)

def IOWR_BAD(_type, nr, size):
    return IOC(READ|WRITE, _type, nr, size)

# Decoders: 
def DIR(nr):
    return (nr >> DIRSHIFT) & DIRMASK

def TYPE(nr):
    return (nr >> TYPESHIFT) & TYPEMASK

def NR(nr):
    return (nr >> NRSHIFT) & NRMASK

def SIZE(nr):
    return (nr >> SIZESHIFT) & SIZEMASK


