# bpf-virtio
A collection of tools to debug virtio devices using bpf

## vhost-trace
A tool to trace vhost ioctls.

### TODO
- Add an option to pretty-print ioctl arguments
- Consider tracing another function?
- Add timestamp / time (%H:%M:%S) option
- Add return value
- Create a VhostCommand class that abstracts the way to print the event from the way to identify it. That way we can use the same for vhost user
- Add vhost-vsock and vhost-scsi
