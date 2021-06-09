#include "sched.h"

static void put_prev_task_myprior(struct rq* rq, struct task_struct* p);
static int select_task_rq_myprior(struct task_struct* p, int cpu, int sd_flag, int flags);
static void set_curr_task_myprior(struct rq* rq);
static void task_tick_myprior(struct rq* rq, struct task_struct* p, int oldprio);
static void switched_to_myprior(struct rq* rq, struct task_struct* p);
void init_myprior_rq(struct myprior_rq* myprior_rq);
static void update_curr_myprior(struct rq* rq);
static void enqueue_task_myprior(struct rq* rq, struct task_struct* p, int flags);
static void dequeue_task_myprior(struct rq* rq, struct task_struct* p, int flags);
static void check_preempt_curr_myprior(struct rq* rq, struct task_struct* p, int flags);
struct task_struct* pick_next_task_myprior(struct rq* rq, struct task_struct* prev);
static void prio_changed_myprior(struct rq* rq, struct task_struct* p, int oldprio);

#define MAX_PRIOR 8
#define MYPRIOR_TIME_SLICE 4

const struct sched_class myprior_sched_class = {
	.next = &fair_sched_class,
	.enqueue_task = &enqueue_task_myprior,
	.dequeue_task = dequeue_task_myprior,
	.check_preempt_curr = check_preempt_curr_myprior,
	.pick_next_task = pick_next_task_myprior,
	.put_prev_task = put_prev_task_myprior,
#ifdef CONFIG_SMP
	.select_task_rq = select_task_rq_myprior,
#endif
	.set_curr_task = set_curr_task_myprior,
	.task_tick = task_tick_myprior,
	.prio_changed = prio_changed_myprior,
	.switched_to = switched_to_myprior,
	.update_curr = update_curr_myprior,
};

void init_myprior_rq(struct myprior_rq* myprior_rq)
{
	unsigned int i;
	printk(KERN_INFO "***[MYPRIOR] Mysched class is online \n");
	myprior_rq->all_nr_running = 0;
	for(i =0 ; i < MAX_PRIOR ; i++){
		INIT_LIST_HEAD(&myprior_rq->queue[i]);
	}

}
static void update_curr_myprior(struct rq* rq) {

	struct task_struct *curr_p = rq->curr;
	struct task_struct *next_p = NULL;
	struct sched_myprior_entity *next_entity = NULL;
	struct sched_myprior_entity *myprior_entity = &curr_p->myprior;
	unsigned int curr_prior = myprior_entity->myprior;
	unsigned int i;
	struct list_head *queue = &rq->myprior.queue[curr_prior];
	unsigned int lowest_prior = 0;
	unsigned int highest_prior = MAX_PRIOR;	
	

	for(i=MAX_PRIOR-1;i>0;i--){
		if(rq->myprior.nr_running[i] >0){
			lowest_prior = i;
			break;
		}
	}

	myprior_entity->update_num +=1;
	myprior_entity->pick_time +=1;
	//printk(KERN_INFO"***[MYPRIOR] update_curr_myprior		 pid = %d,update_num = %d\n",curr_p->pid, myprior_entity->update_num);


	if(myprior_entity->pick_time > 100){
		myprior_entity->pick_time = 0;

		next_entity = list_entry(rq->myprior.queue[lowest_prior],struct sched_myprior_entity,run_list);
		next_p = container_of(next_entity,struct task_struct,myprior);
		printk(KERN_INFO"***[MYPRIOR] lowest priority queue is waiting long time");
		
		list_del(&next_p->myprior.run_list);
		list_add(&next_p->myprior.run_list, queue);
		
		resched_curr(rq);
	}


	if(myprior_entity->update_num > MYPRIOR_TIME_SLICE){
		//printk(KERN_INFO"***{MYPRIORUPDATECUREND] update_curr_end pid = %d, update_num =%d\n", curr_p->pid, myprior_entity->update_num);
		myprior_entity->update_num = 0;
		
		list_del_init(&myprior_entity->run_list);
		list_add_tail(&myprior_entity->run_list,queue);
		
		resched_curr(rq);
	} 

}

static void enqueue_task_myprior(struct rq* rq, struct task_struct* p, int flags) {
	struct myprior_rq *myprior_rq = &rq->myprior;
	struct sched_myprior_entity *myprior_entity = &p->myprior;

	list_add_tail(&myprior_entity->run_list, &myprior_rq->queue[myprior_entity->myprior]);
	myprior_rq->all_nr_running++;
	myprior_rq->nr_running[myprior_entity->myprior]++;
	printk(KERN_INFO "***[MYPRIOR] enqueue:success cpu=%d,nr_running=%d,pid=%d\n",cpu_of(rq),myprior_rq->nr_running[myprior_entity->myprior],p->pid);
}

static void dequeue_task_myprior(struct rq* rq, struct task_struct* p, int flags){
	struct myprior_rq* myprior_rq = &rq->myprior;
	struct sched_myprior_entity* myprior_entity = &p->myprior;

	if(myprior_rq->nr_running > 0){
		myprior_rq->all_nr_running--;
		myprior_rq->nr_running[myprior_entity->myprior]--;
		list_del_init(&myprior_entity->run_list);
		printk(KERN_INFO "***[MYPRIOR] dequeue: the dequeued task is curr, set TIF_NEED_RESCHED flag cpu=%d,p->state=%d,p->pid=%d,curr->pid=%d\n",cpu_of(rq), p->state, p->pid, p->pid);
	}
	else{}

}
static void check_preempt_curr_mysched(struct rq *rq, struct task_struct *p, int flags){
}

void check_preempt_curr_myprior(struct rq* rq, struct task_struct* p, int flags) {
	printk("***[MYPRIOR] check_preempt_curr_myprior\n");
}
struct task_struct* pick_next_task_myprior(struct rq* rq, struct task_struct* prev)
{
	struct task_struct *next_p = NULL;
	struct sched_myprior_entity *next_entity = NULL;
	struct myprior_rq* myprior_rq = &rq->myprior;
	unsigned int i;
		
	

	if (rq->myprior.all_nr_running == 0) {
		return NULL;
	}

	else {
		for(i = 0 ; i<MAX_PRIOR; i++) {
			if(rq->myprior.nr_running[i] > 0) {
				next_entity = list_entry(rq->myprior.queue[i].next, struct sched_myprior_entity, run_list);
				next_p = container_of(next_entity, struct task_struct, myprior);
				if(prev->myprior.myprior > next_p->myprior.myprior){
					printk(KERN_INFO "\t***[MYPRIOR][PREEMP] pick_next_task: prev->pid=%d,next_p->pid=%d,prev->prior=%d,next->prior=%d,nr_running=%d\n", prev->pid, next_p->pid,prev->myprior.myprior,next_p->myprior.myprior,myprior_rq->all_nr_running);
				}
				else{
					printk(KERN_INFO "\t***[MYPRIOR] pick_next_task: prev->pid=%d,next_p->pid=%d,nr_running=%d\n",prev->pid,next_p->pid,myprior_rq->all_nr_running);
				}
				return next_p;
			}
		}
		return NULL;
	}
}

void put_prev_task_myprior(struct rq* rq, struct task_struct* p) {
	printk(KERN_INFO "\t***[MYPRIOR] put_prev_task: do_nothing, p->pid=%d\n", p->pid);
}
int select_task_rq_myprior(struct task_struct* p, int cpu, int sd_flag, int flags) { return task_cpu(p); }
void set_curr_task_myprior(struct rq* rq) {
	printk(KERN_INFO"***[MYPRIOR] set_curr_task_myprior\n");
}
void task_tick_myprior(struct rq* rq, struct task_struct* p, int queued) {
	update_curr_myprior(rq);
}
void prio_changed_myprior(struct rq* rq, struct task_struct* p, int oldprio) { }
/*This routine is called when a task migrates between classes*/
void switched_to_myprior(struct rq* rq, struct task_struct* p)
{
	resched_curr(rq);
}
