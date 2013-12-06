import logging
from taskthread import TimerTask, TaskThread
import time

logging.basicConfig(level=logging.DEBUG)

count = 0

def execute():
    print "Count: %d" % count

task = TimerTask(execute,
                 delay=2)
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
