from common.utils import Utils

import psutil
import time
import os
from datetime import datetime
from subprocess import *


class LogTrackScriptCntl():
    def __init__(self):
        self.pid = -1
        self.filename = None
        self.successlogfile = Utils.get_tmp_path() + 'success.log'

    def get_pid(self):
        # print("current pid : " + str(self.pid))
        return self.pid

    def set_pid(self, pid):
        print("PID change from " + str(self.pid) + " to " + str(pid))
        self.pid = pid

    def launch_log_track_script(self):
        if os.path.isfile(self.successlogfile):
            os.remove(self.successlogfile)
        path = Utils.get_automation_path() + 'script/catch_log'
        self.subProcess = Popen([path])
        self.set_pid(self.subProcess.pid)
        return self.pid

    def terminate_log_track_script(self, terminated=True):
        # time.sleep(2)
        self.terminate_process_tree()
        if (terminated):
            print('Log taken')

    def checksuccessfile(self):
        if self.pid != -1 and os.path.isfile(self.successlogfile):
            return True
        return False

    def terminate_process_tree(self):
        if self.pid == -1:
            print(
                "Don't need to terminate process tree because current pid is invalid (-1)")
            return

        print("terminateProcessTree : starting pid : " + str(self.pid))
        parent = psutil.Process(self.pid)
        for child in parent.children(True):
            print("get child pid ", child.pid)
            try:
                if child.is_running():
                    print("try to terminate ", child.pid)
                    child.terminate()
            except Exception as e:
                print("exception : ", e)
        self.subProcess.terminate()
        time.sleep(1)
        self.subProcess.poll()
        self.set_pid(-1)

    def findRxdAck(self, data, msg_counter):
        index = -1
        try:
            index = [idx for idx, s in enumerate(
                data) if 'Rxd Ack; Removing MessageCounter:'+msg_counter in s][0]
        except:
            print('Rxd Ack is not found for', msg_counter)
        return index

    def successcount(self, filename):
        if not os.path.isfile(self.successlogfile):
            print(self.successlogfile, 'does not exisit!')
            return 0

        with open(self.successlogfile) as f:
            lines = f.read().splitlines()
        if len(lines) == 0:
            print("No commands Logs")
            return 0
        self.filename = Utils.get_tmp_path() + 'results-' + \
            filename.split(
                '/')[-1]+'-%s' % datetime.now().strftime('%Y-%m-%d-%H%M%S')+'.txt'
        print(self.filename)
        index = -1
        success_count = 0
        fail_count = 0
        while (len(lines)):
            try:
                index = [idx for idx, s in enumerate(
                    lines) if 'Received payload' in s][0]
                if ('Sending encrypted msg' in lines[index+1]):
                    msg_counter1 = str(
                        lines[index+1]).split(' ')[8].split(':')[1]
                    rindex = self.findRxdAck(lines, msg_counter1)
                    if rindex != -1:
                        print("Success: MessageCounter:", msg_counter1, ' Received payload:', str(
                            lines[index]).split(' ')[5], file=open(self.filename, 'a'))
                        success_count += 1
                        del lines[rindex]
                        del lines[index+1]
                        del lines[index]
                    else:
                        fail_count += 1
                        print("Failed: MessageCounter:", msg_counter1, '.Received payload:', str(
                            lines[index]).split(' ')[5], file=open(self.filename, 'a'))
                        del lines[index]
                        del lines[index+1]
                else:
                    fail_count += 1
                    print("Failed: ", '.Received payload:', str(
                        lines[index]).split(' ')[5], file=open(self.filename, 'a'))
                    del lines[index]
            except:
                break

        print('\nTotal Success:', success_count, file=open(self.filename, 'a'))
        print('Total Failed:', fail_count, file=open(self.filename, 'a'))
        # print("Sucess/Failue Ratio:%f" % (success_count*100)/(success_count+fail_count),file=open(self.filename,'a'))
        if (success_count > 0) or (fail_count > 0):
            print("Success Ratio:%.2f%%" % ((success_count*100) /
                  (success_count+fail_count)), file=open(self.filename, 'a'))
        else:
            print("Success Ratio:%.2f%%" % 0, file=open(self.filename, 'a'))

        return success_count
