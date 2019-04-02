# coding: utf-8
# Create by LC
import sys, threading, thread

reload(sys)
sys.setdefaultencoding('utf8')

import threading
import time

condition = threading.Condition()
products = 1000
products = [100, 203, 203, 40, 34]
result = 0

class Tasker(threading.Thread):
    task_index = 0
    task_done = False

    def __init__(self, task_index):
        threading.Thread.__init__(self)
        self.task_index = task_index

    def run(self):
        global result
        global products
        while True:
            if not self.task_done:
                if products[self.task_index] > 0:
                    products[self.task_index] -= 1
                    print "tasker(%s):finish one, now task is:%s" % (self.name, products[self.task_index])
                    time.sleep(2)
                else:
                    if condition.acquire():
                        result += 1;
                        print "tasker->(%s):finish task, products:%s, sequence->%s" % (self.name, products[self.task_index], result)
                        if result > 4:
                            print "task all done!"
                        condition.release()
                        self.task_done = True
                        time.sleep(2)
                    break
            else:
                break


if __name__ == "__main__":
    for count in range(0, len(products)):
        tasker = Tasker(count)
        tasker.start()
