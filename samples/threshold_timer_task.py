import logging
from taskthread import TimerTask, TaskThread
import time

count = 0
def get_count():
    return count
def execute():
    print "Count: %d" % count

task = TimerTask(execute,
                 delay=1,
                 count_fcn=get_count,
                 threshold=3)
task.start()

for i in xrange(10):
    count += 1
    time.sleep(1)

task.stop()

count = 0
task.start()
for i in xrange(10):
    count += 1
    time.sleep(1)

task.shutdown()
