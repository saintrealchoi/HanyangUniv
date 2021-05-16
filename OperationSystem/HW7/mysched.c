#include "sched.h"

void init_mysched_rq(struct mysched_rq *mysched_rq)
{
	printk(KERN_INFO "***[MYSCHED] Myschedclass is online \n");
	mysched_rq->nr_running= 0;
	INIT_LIST_HEAD(&mysched_rq->queue);
}

static void update_curr_mysched(struct rq *rq)
{
}

//TODO
static void enqueue_task_mysched(struct rq *rq, struct task_struct *p, int flags) 
{
	list_add_tail(&p->mysched.run_list,&rq->mysched.queue);
	rq->mysched.nr_running++;
	printk(KERN_INFO"***[MYSCHED] enqueue: success cpu=%d,nr_running=%d,p->state=%ld,p->pid=%d\n",p->on_cpu,rq->mysched.nr_running,p->state,p->pid);

}

//TODO
static void dequeue_task_mysched(struct rq *rq, struct task_struct *p, int flags)
{

	printk(KERN_INFO"***[MYSCHED] dequeue: start\n");
	if((int)rq->mysched.nr_running >0){
		printk(KERN_INFO "***[MYSCHED] dequeue: the dequeued task is curr, set TIF_NEED_RESCHED flag cpu=%d,p->state=%ld,p->pid=%d,curr->pid=%d\n",p->on_cpu,p->state,p->pid,p->pid);
		list_del_init(&p->mysched.run_list);
		rq->mysched.nr_running--;
	}

	else{}
	printk(KERN_INFO"***[MYSCHED] dequeue: end\n");

}
static void check_preempt_curr_mysched(struct rq *rq, struct task_struct *p, int flags) 
{ 
}
//TODO
struct task_struct *pick_next_task_mysched(struct rq *rq, struct task_struct *prev)
{
	struct task_struct *p;
	struct sched_mysched_entity *mysched_entity = NULL;

	if(list_empty(rq->mysched.queue.next)){
		return NULL;
	}
	else{
		put_prev_task(rq,prev);
		mysched_entity = list_entry(rq->mysched.queue.next, struct sched_mysched_entity, run_list);
		p = container_of(mysched_entity, struct task_struct, mysched);
		printk(KERN_INFO"***[MYSCHED] pick_next_task: cpu=%d,prev->pid=%d,next_p->pid=%d,nr_running=%d\n",p->on_cpu,prev->pid,p->pid,rq->mysched.nr_running);
	}
	printk(KERN_INFO "***[MYSCHED] pick_next_task: end\n");
}
//TODO
static void put_prev_task_mysched(struct rq *rq, struct task_struct *p) 
{
	printk(KERN_INFO "***[MYSCHED] put_prev_task: do nothing,p->pid=%d\n",p->pid);
}
static int select_task_rq_mysched(struct task_struct *p, int cpu, int sd_flag, int flags)
{
	return task_cpu(p);
}
static void set_curr_task_mysched(struct rq *rq) 
{ 
}
static void task_tick_mysched(struct rq *rq, struct task_struct *p, int queued) 
{ 
}
static void prio_changed_mysched(struct rq *rq, struct task_struct *p, int oldprio) 
{ 
}
/* This routine is called when a task migrates between classes */
static void switched_to_mysched(struct rq *rq, struct task_struct *p)
{
	resched_curr(rq);
}
const struct sched_class mysched_sched_class = {
	.next			= &idle_sched_class,
	.enqueue_task		= enqueue_task_mysched,
	.dequeue_task		= dequeue_task_mysched,
	.check_preempt_curr	= check_preempt_curr_mysched,
	.pick_next_task		= pick_next_task_mysched,
	.put_prev_task		= put_prev_task_mysched,

#ifdef CONFIG_SMP
	.select_task_rq		= select_task_rq_mysched,
#endif
	.set_curr_task		= set_curr_task_mysched,
	.task_tick		= task_tick_mysched,
	.prio_changed		= prio_changed_mysched,
	.switched_to		= switched_to_mysched,
	.update_curr		= update_curr_mysched,
};
