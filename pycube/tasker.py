from redis import Redis
from rq import Queue
from rq.job import Job

class Task(object):

    def __init__(self, conn=Redis()):
        self.conn = conn
        self.q = Queue(connection=self.conn)

    def add_job(self, func, *args, ttl=500):
        job = self.q.enqueue_call(func=func, args=args, result_ttl=ttl)
        return job
    
    def get_job(self, job_id=id):
        job = Job.fetch(job_id, connection=self.conn)
        return job