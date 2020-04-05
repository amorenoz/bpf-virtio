#include <stdio.h>

#include <bpf/libbpf.h>
#include <bpf/bpf.h>
#include <time.h>
#include <unistd.h>

#include "vhost_trace.h"
#include "vhost_trace.skel.h"

#define PERF_BUFFER_PAGES	64
#define PERF_BUFFER_TIME_MS	10
/* Set the poll timeout when no events occur. */
#define PERF_POLL_TIMEOUT_MS	100

static const char* vhost_trace_event_str[VHOST_TRACE_MAX_EVENT] = {
	[VHOST_TRACE_OPEN]  = "VHOST_TRACE_OPEN",
	[VHOST_TRACE_CLOSE] = "VHOST_TRACE_CLOSE",
	[VHOST_TRACE_MSG]   = "VHOST_TRACE_MSG",
};

static void
vhost_trace_print_event(const struct vhost_trace_event* event) {
	const char* etype_str;

	if (event->etype >= VHOST_TRACE_MAX_EVENT)
		etype_str = "Unknown";
	else
		etype_str = vhost_trace_event_str[event->etype];

	printf("Event %p: \n", event);
	printf("  ts:    %llu \n", event->ts);
	printf("  pid:   %i \n", event->pid);
	printf("  uid:   %i \n", event->uid);
	printf("  fname: %s \n", event->fname);
	printf("  etype: %s(%d) \n", etype_str, event->etype);
	printf("  msg:   0x%lx \n", event->msg);
}

void handle_event(void *ctx, int cpu, void *data, __u32 data_sz)
{
	const struct vhost_trace_event *e = data;
	if (e != NULL)
		vhost_trace_print_event(e);

	if (e-> etype == VHOST_TRACE_OPEN) {
		printf("[%d] New Vhost device opened: %-16s \n", e->pid,
		       e->fname);
	}
	if (e-> etype == VHOST_TRACE_CLOSE) {
		printf("[%d] New Vhost msg : %ld \n", e->pid,
		       e->msg);
	}
}

void handle_lost_events(void *ctx, int cpu, __u64 lost_cnt)
{
	fprintf(stderr, "Lost %llu events on CPU #%d!\n", lost_cnt, cpu);
}

int main(int argc, char **argv)
{
	struct vhost_trace_bpf *obj;
	struct perf_buffer_opts pb_opts;
	struct perf_buffer *pb = NULL;
	int err;

	obj = vhost_trace_bpf__open();
	if (!obj) {
		fprintf(stderr, "failed to open and/or load BPF object\n");
		return 1;
	}

	/* initialize global data (filtering options)
	obj->rodata->targ_tgid = env.pid;
	obj->rodata->targ_pid = env.tid;
	obj->rodata->targ_uid = env.uid;
	obj->rodata->targ_failed = env.failed;
	*/

	err = vhost_trace_bpf__load(obj);
	if (err) {
		fprintf(stderr, "failed to load BPF object: %d\n", err);
		goto cleanup;
	}

	err = vhost_trace_bpf__attach(obj);
	if (err) {
		fprintf(stderr, "failed to attach BPF programs\n");
		goto cleanup;
	}
	fprintf(stdout, "Bpf program attached\n");

	/* setup event callbacks */
	pb_opts.sample_cb = handle_event;
	pb_opts.lost_cb = handle_lost_events;
	pb = perf_buffer__new(bpf_map__fd(obj->maps.events), PERF_BUFFER_PAGES,
			      &pb_opts);
	err = libbpf_get_error(pb);
	if (err) {
		pb = NULL;
		fprintf(stderr, "failed to open perf buffer: %d\n", err);
		goto cleanup;
	}

	while (1) {
		usleep(PERF_BUFFER_TIME_MS * 1000);
		if ((err = perf_buffer__poll(pb, PERF_POLL_TIMEOUT_MS)) < 0)
			break;
		//if (env.duration) {
		//	if (gettimens() > time_end) {
		//		goto cleanup;
		//	}
		//}
	}
	printf("Error polling perf buffer: %d\n", err);


cleanup:
	perf_buffer__free(pb);
	vhost_trace_bpf__destroy(obj);

	return err != 0;

}
