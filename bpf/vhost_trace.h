#ifndef __VHOST_TRACE_H
#define __VHOST_TRACE_H

#ifdef _BCC_
#include <sys/types.h>
#endif

#define TASK_COMM_LEN 16
#define NAME_MAX 255


enum vhost_trace_event_type {
	VHOST_TRACE_OPEN = 0,
	VHOST_TRACE_CLOSE,
	VHOST_TRACE_MSG,
	VHOST_TRACE_MAX_EVENT,
};

struct vhost_trace_event {
	__u64 ts; // TODO: Add timestamp
	pid_t pid;
	uid_t uid;
	char fname[NAME_MAX];
	__u8 etype;
	unsigned long msg;
	// TODO: Add payload
};

/* Removeme?
struct event2 {
	
	__u64 ts;
	pid_t pid;
	uid_t uid;
	//int ret;
	//int flags;
	char comm[TASK_COMM_LEN];
	char fname[NAME_MAX];
};
*/

#endif
