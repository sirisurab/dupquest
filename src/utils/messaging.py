import redis
from typing import List
from functools import partial

def get_client():
    r = redis.Redis(
        host='redis',
        port='6379'
    )
    #print('connected to redis %s' % r.info())
    return r

# push task to queue
def push_to_q(msg: str, queue: str) -> None:
    print('connecting to redis')
    r = get_client()
    r.lpush(queue, msg)
    print('pushed message '+msg+' to '+queue)
    return

# push multiple tasks to queue
def push_tasks_to_q(tasks: List[str], queue: str) -> None:
    print('connecting to redis')
    r = get_client()
    #r.lpush(queue, msg)
    for task in tasks:
        r.lpush(queue, task)
    #push_to_queue = partial(r.lpush, name=queue)
    #push = map(push_to_queue, tasks)
    print('pushed message '+str(tasks)+' to '+queue)
    return


# remove/delete message from queue
def del_from_q(msg: bytes, queue: str) -> None:
    r = get_client()
    r.lrem(queue, msg, 1)
    print('deleted message '+str(msg)+' from '+queue)
    return


# pops message from queue1 and simultaneously pushes the message to queue2
# returns message
def pop_q1_push_q2(pop_queue: str, push_queue: str) -> bytes:
    r = get_client()
    msg: bytes = r.rpoplpush(pop_queue, push_queue)
    print('popped msg '+str(msg)+' from '+pop_queue+' and pushed to '+push_queue)
    #if msg is None:
        #msg = ''
    return msg
    #return '2016-1'