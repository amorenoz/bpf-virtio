from enum import Enum
import ioctls as io

VHOST_VIRTIO = 0xAF

class VhostCmnd(Enum):
    #define VHOST_GET_FEATURES	_IOR(VHOST_VIRTIO, 0x00, __u64)
    #define VHOST_SET_FEATURES	_IOW(VHOST_VIRTIO, 0x00, __u64)
    VHOST_GET_FEATURES=0
    VHOST_SET_FEATURES=0

    #define VHOST_SET_OWNER _IO(VHOST_VIRTIO, 0x01)
    VHOST_SET_OWNER = 0x1

    #define VHOST_RESET_OWNER _IO(VHOST_VIRTIO, 0x02)
    VHOST_RESET_OWNER = 0x2

    #define VHOST_SET_MEM_TABLE	_IOW(VHOST_VIRTIO, 0x03, struct vhost_memory)
    VHOST_SET_MEM_TABLE = 0x3

    #define VHOST_SET_LOG_BASE _IOW(VHOST_VIRTIO, 0x04, __u64)
    VHOST_SET_LOG_BASE = 0x4

    #define VHOST_SET_LOG_FD _IOW(VHOST_VIRTIO, 0x07, int)
    VHOST_SET_LOG_FD = 0x7

    #define VHOST_SET_VRING_NUM _IOW(VHOST_VIRTIO, 0x10, struct vhost_vring_state)
    VHOST_SET_VRING_NUM = 0x10

    #define VHOST_SET_VRING_ADDR _IOW(VHOST_VIRTIO, 0x11, struct vhost_vring_addr)
    VHOST_SET_VRING_ADDR = 0x11

    #define VHOST_SET_VRING_BASE _IOW(VHOST_VIRTIO, 0x12, struct vhost_vring_state)
    VHOST_SET_VRING_BASE = 0x12

    #define VHOST_GET_VRING_BASE _IOWR(VHOST_VIRTIO, 0x12, struct vhost_vring_state)
    VHOST_GET_VRING_BASE = 0x12

    #define VHOST_VRING_LITTLE_ENDIAN 0
    #define VHOST_VRING_BIG_ENDIAN 1
    #define VHOST_SET_VRING_ENDIAN _IOW(VHOST_VIRTIO, 0x13, struct vhost_vring_state)
    #define VHOST_GET_VRING_ENDIAN _IOW(VHOST_VIRTIO, 0x14, struct vhost_vring_state)
    VHOST_SET_VRING_ENDIAN = 0x13
    VHOST_GET_VRING_ENDIAN = 0x14

    #define VHOST_SET_VRING_KICK _IOW(VHOST_VIRTIO, 0x20, struct vhost_vring_file)
    VHOST_SET_VRING_KICK = 0x20

    #define VHOST_SET_VRING_CALL _IOW(VHOST_VIRTIO, 0x21, struct vhost_vring_file)
    VHOST_SET_VRING_CALL = 0x21

    #define VHOST_SET_VRING_ERR _IOW(VHOST_VIRTIO, 0x22, struct vhost_vring_file)
    VHOST_SET_VRING_ERR = 0x22

    #define VHOST_SET_VRING_BUSYLOOP_TIMEOUT _IOW(VHOST_VIRTIO, 0x23,
    #                                             struct vhost_vring_state)
    VHOST_SET_VRING_BUSYLOOP_TIMEOUT = 0x23

    #define VHOST_GET_VRING_BUSYLOOP_TIMEOUT _IOW(VHOST_VIRTIO, 0x24,
    #                                             struct vhost_vring_state)
    VHOST_GET_VRING_BUSYLOOP_TIMEOUT = 0x24

    #define VHOST_BACKEND_F_IOTLB_MSG_V2 0x1
    VHOST_BACKEND_F_IOTLB_MSG_V2 = 0x1

    #define VHOST_SET_BACKEND_FEATURES _IOW(VHOST_VIRTIO, 0x25, __u64)
    VHOST_SET_BACKEND_FEATURES = 0x25
    #define VHOST_GET_BACKEND_FEATURES _IOR(VHOST_VIRTIO, 0x26, __u64)
    VHOST_GET_BACKEND_FEATURES = 0x26

    """VHOST_NET specific defines """
    #define VHOST_NET_SET_BACKEND _IOW(VHOST_VIRTIO, 0x30, struct vhost_vring_file)
    VHOST_NET_SET_BACKEND = 0x30

    """ VHOST_SCSI specific defines """

    #define VHOST_SCSI_SET_ENDPOINT _IOW(VHOST_VIRTIO, 0x40, struct vhost_scsi_target)
    VHOST_SCSI_SET_ENDPOINT = 0x40
    #define VHOST_SCSI_CLEAR_ENDPOINT _IOW(VHOST_VIRTIO, 0x41, struct vhost_scsi_target)
    VHOST_SCSI_CLEAR_ENDPOINT  = 0x41

    #define VHOST_SCSI_GET_ABI_VERSION _IOW(VHOST_VIRTIO, 0x42, int)
    VHOST_SCSI_GET_ABI_VERSION = 0x42

    #define VHOST_SCSI_SET_EVENTS_MISSED _IOW(VHOST_VIRTIO, 0x43, __u32)
    VHOST_SCSI_SET_EVENTS_MISSED = 0x43
    #define VHOST_SCSI_GET_EVENTS_MISSED _IOW(VHOST_VIRTIO, 0x44, __u32)
    VHOST_SCSI_GET_EVENTS_MISSED = 0x44

    """VHOST_VSOCK specific defines"""

    #define VHOST_VSOCK_SET_GUEST_CID	_IOW(VHOST_VIRTIO, 0x60, __u64)
    VHOST_VSOCK_SET_GUEST_CID = 0x60

    #define VHOST_VSOCK_SET_RUNNING		_IOW(VHOST_VIRTIO, 0x61, int)
    VHOST_VSOCK_SET_RUNNING = 0x61

def print_vhost_cmd(ioctl_num):
    dirstr = ""
    numstr = ""
    direction = io.DIR(ioctl_num)
    if direction == io.NONE:
        dirstr = "NONE"
    else:
        if direction & io.READ:
            dirstr += "R"
        if direction & io.WRITE:
            dirstr += "W"

    num = io.NR(ioctl_num)
    try:
        cmd = VhostCmnd(num)
        numstr = cmd.name
    except Exception :
        numstr = "Unknown"

    print("({}) {}".format(dirstr, numstr))


