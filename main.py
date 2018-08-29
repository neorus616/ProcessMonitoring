"""This script prompts a user to enter a positive number
 (seconds) that will refresh monitor processes in that time"""
import time
import os
import sys
import psutil
import ctypes
import datetime
from datetime import timedelta


def main():
    while 1:
        option = raw_input(
            "Please state which option you want to use: \n1)Process Monitor \n2)Manual Mode \n3)Exit\n"
            "For example 'Manual Mode'(without apostrophes, Case Sensitive!)\n")
        if option == "Process Monitor":
            clearscreen()
            try:
                inputcheck()
            except ValueError:
                print "Timer must be a positive number!\n"
                print "Exiting to main menu..\n"
            except KeyboardInterrupt:
                print "Exiting to main menu..\n"
        elif option == "Manual Mode":
            try:
                datecheck()
            except KeyboardInterrupt:
                print "Exiting to main menu..\n"
        elif option == "Exit":
            terminate()
            print "Bye bye..\n"
            exit()
        else:
            print "Wrong state entered, please try again.. \n"


def inputcheck():
    timer = input("Please state frequency in seconds of Process Monitor updating\n")
    if timer > 0:
        print "Starting monitoring every " + str(timer) + " seconds..\n"
        time.sleep(1)
        print "timer: " + str(timer) + '\n'
        processmonitor(timer)
    else:
        raise ValueError


def terminate():
    """This function writes if the program closed suddenly by ctrl+c"""
    terminated = 1
    filename = 'secretfile.txt'
    if os.path.exists(filename):
        writesecret(filename, terminated)
    # print "Program exiting now.. good bye"


def writesecret(filename, terminated):
    """This function writes to a secret file about the logs"""
    # For *nix add a '.' prefix.
    prefix = '.' if os.name != 'nt' else ''
    filename = prefix + filename
    # Write file.
    if os.path.exists(filename):
        os.remove(filename)
    f = open(filename, 'w')
    f.write(str(os.stat("processList.txt")[8]) + '\n')
    f.write(str(os.stat("Status_Log.txt")[8]) + '\n')
    f.write(str(terminated))
    f.close()
    # For windows set file attribute.
    if os.name == 'nt':
        ret = ctypes.windll.kernel32.SetFileAttributesW(ur'%s' % filename, 2)
        if not ret:  # There was an error.
            raise ctypes.WinError()


def checkhacker(check):
    """Cross platform hidden check hacker."""
    if os.path.exists("processList.txt") and os.path.exists("Status_Log.txt"):
        filename = 'secretfile.txt'
        prefix = '.' if os.name != 'nt' else ''
        filename = prefix + filename
        if os.path.exists(filename) and check:
            secretfile = open(filename, "r")
            pl = secretfile.readline().rstrip('\n')
            sl = secretfile.readline().rstrip('\n')
            terminated = secretfile.readline().rstrip('\n')
            if terminated == str(2):
                if pl != str(os.stat("processList.txt")[8]) or sl != str(os.stat("Status_Log.txt")[8]):
                    print "Files has been modified! 1"
                    secretfile.close()
                    os.remove(filename)
                    exit()
                else:
                    secretfile.close()
                    os.remove(filename)
            elif terminated == str(1):
                if pl != str(os.stat("processList.txt")[8]) or sl != str(os.stat("Status_Log.txt")[8]):
                    print "Files has been modified!! 2"
                    print check
                    secretfile.close()
                    os.remove(filename)
                    exit()
            elif terminated != str(1):
                if pl != str(os.stat("processList.txt")[8]) or sl != str(os.stat("Status_Log.txt")[8]):
                    print "Program has not been closed properly, please restart.."
                    secretfile.close()
                    os.remove(filename)
                    exit()
            else:
                secretfile.close()
                os.remove(filename)
        else:
            filename = 'secretfile.txt'
            writesecret(filename, 2)


def list_to_dict(proclist):
    """This function convert list to dictionary"""
    procdict = {}
    for process in proclist:
        procdict[process.pid] = (process.name(), process.create_time())
    return procdict


def clearscreen():
    """This function clear the screen from previous scans and show header"""
    os.system('cls' if os.name == 'nt' else 'clear')
    print "$$______________$$_______________$$_______________$$___________" + \
          "____$$_______________$$_______________$$_______________$$" + '\n' + \
          "$$___$$$$$$$$___$$___$$$$$$$$____$$____$$$$$$_____$$___$$$$$$$$$___$$_" + \
          "__$$$$$$$$$___$$___$$$$$$$$$___$$___$$$$$$$$$___$$" + '\n' + \
          "$$___$$____$$___$$___$$_____$$___$$___$$____$$____$$___$$____" + \
          "______$$___$$__________$$___$$__________$$___$$__________$$" + '\n' + \
          "$$___$$$$$$$$___$$___$$$$$$$$____$$___$$____$$____$$___$$________" + \
          "__$$___$$$$$$______$$___$$$$$$$$$___$$___$$$$$$$$$___$$" + '\n' + \
          "$$___$$_________$$___$$___$$_____$$___$$____$$____$$___$$________" + \
          "__$$___$$__________$$__________$$___$$__________$$___$$" + '\n' + \
          "$$___$$_________$$___$$____$$____$$____$$$$$$_____$$___$$$$$$$$$_" + \
          "__$$___$$$$$$$$$___$$___$$$$$$$$$___$$___$$$$$$$$$___$$" + '\n' + \
          "$$______________$$_______________$$_______________$$______________" + \
          "_$$_______________$$_______________$$_______________$$"
    print "$$_$$________$$_$$____$$$$$$_____$$___$$____$$____$$____$$$$$$$____$$_$$$$$$$$$$$$$_$$_" +\
          "___$$$$$$_____$$___$$$$$$$$____$$" + '\n' +\
          "$$_$$$$____$$$$_$$___$$____$$____$$___$$$___$$____$$______$$$______$$_____" +\
          "_$$$______$$___$$____$$____$$___$$_____$$___$$" + '\n' +\
          "$$_$$__$$$$__$$_$$___$$____$$____$$___$$_$$_$$____$$______$$$______$$______$$$__" +\
          "____$$___$$____$$____$$___$$$$$$$$____$$" + '\n' +\
          "$$_$$___$$___$$_$$___$$____$$____$$___$$___$$$____$$______$$$______$$______$$$__" +\
          "____$$___$$____$$____$$___$$___$$_____$$" + '\n' +\
          "$$_$$___$$___$$_$$____$$$$$$_____$$___$$____$$____$$____$$$$$$$____$$______$$$___" +\
          "___$$____$$$$$$_____$$___$$____$$____$$" + '\n' +\
          "$$______________$$_______________$$_______________$$_______________$$_____________" +\
          "__$$_______________$$_______________$$" + '\n'


def epochtotime(epochtime):
    """This function convert from float time to standard date"""
    return datetime.datetime.fromtimestamp(epochtime).strftime('%Y-%m-%d %H:%M:%S')


def processtostring(pid, process):
    """This function creates a string of a received process"""
    return "pid = " + str(pid) + " name = " + str(process[0]) + " Time started: " + \
           datetime.datetime.fromtimestamp(process[1]).strftime("%Y-%m-%d %H:%M:%S")


def writer(line, filename):
    """This function writes to a log file"""
    if os.path.exists(filename):
        os.chmod(filename, 0o0755)
    filelog = open(filename, "a")
    filelog.write("Timestamp: " + epochtotime(time.time()) + ' ')
    filelog.write(line + '\n')
    filelog.close()
    os.chmod(filename, 0o0444)


def processmonitor(timer):
    """main monitor"""
    oldprocess = {}
    checkhacker(True)
    while 1:
        clearscreen()
        pidtoremove = []
        newprocess = list_to_dict(list(psutil.process_iter()))
        for process in sorted(newprocess.iterkeys()):
            processstring = processtostring(process, newprocess[process])
            writer(processstring, "processList.txt")
            if process in oldprocess:
                continue
            else:
                print "new process: " + processstring
                oldprocess[process] = (newprocess[process][0], newprocess[process][1])
                writer("Created: " + processstring, "Status_Log.txt")
        for process in sorted(oldprocess.iterkeys()):
            if process not in newprocess:
                processstring = processtostring(process, oldprocess[process])
                print "process terminated: " + processstring
                pidtoremove.append(process)
                writer("Terminated: " + processstring + " Time Terminated: "
                       + epochtotime(time.time()), "Status_Log.txt")
        for pid in pidtoremove:
            del oldprocess[pid]
        checkhacker(False)
        time.sleep(timer)
        checkhacker(True)


def lister(line):
    return line[line.find("pid = "):]


def parser(line):
    return line[line.find("name = ")+7:line.find("Time started")]


def datecheck():
    while 1:
        checkhacker(True)
        timeformat = "%Y-%m-%d %H:%M:%S"
        firstdate = raw_input("Type First Date :\n")
        try:
            firstdate = datetime.datetime.strptime(firstdate, timeformat)
        except ValueError:
            print "Wrong format! please enter date in the following format: \n %Y-%m-%d %H:%M:%S," +\
                  " for example 2018-04-30 14:08:48 \n try again..\n"
            continue
        seconddate = raw_input("Type Second Date :\n")
        try:
            seconddate = datetime.datetime.strptime(seconddate, timeformat)
        except ValueError:
            print "Wrong format! please enter date in the following format: \n %Y-%m-%d %H:%M:%S," +\
                  " for example 2018-04-30 14:08:48 \n try again..\n"
            continue
        if firstdate > seconddate:
            tmp = seconddate
            seconddate = firstdate
            firstdate = tmp
        if firstdate == seconddate:
            print "Dates needs to be different!\n"
            continue
        checkhacker(True)
        manual(firstdate, seconddate)


def manual(firstdate, seconddate):
    counter = 5
    while 1:
        search = open("processList.txt")
        oldprocess = []
        for line in search:
            if ("Timestamp: " + str(firstdate)) in line:
                oldprocess.append(lister(line))
        newprocess = []
        search = open("processList.txt")
        for line in search:
            if ("Timestamp: " + str(seconddate)) in line:
                newprocess.append(lister(line))
        if len(oldprocess) == 0 and counter >= 0:
            firstdate = firstdate - timedelta(seconds=1)
            counter -= 1
            continue
        if len(newprocess) == 0 and counter >= 0:
            seconddate = seconddate + timedelta(seconds=1)
            counter -= 1
            continue
        if len(newprocess) != 0 and len(oldprocess) != 0:
            break
        if counter == -1:
            break
    if len(newprocess) == 0:
        print "Second date not found, try again with different date \n"
        return
    if len(oldprocess) == 0:
        print "First date not found, try again with different date \n"
        return
    searcher(newprocess, oldprocess)
    while 1:
        again = raw_input("Do you want to check another dates? y for yes, n for no \n")
        if again == "y":
            break
        if again == "n":
            raise KeyboardInterrupt
        else:
            print "wrong input, try again, y for yes, n for no\n"


def searcher(newprocess, oldprocess):
    for process in oldprocess:
        flag = False
        for process2 in newprocess:
            if process in process2:
                print parser(process) + " still running.."
                flag = True
                break
        if not flag:
            print parser(process) + " has been closed.."
    for process in newprocess:
        flag = False
        for process2 in oldprocess:
            if process in process2:
                flag = True
                break
        if not flag:
            print parser(process) + " has been started.."


def show_usage():
    """usage of this program"""
    print """
      USAGE:
        ProcessMonitor.py
    """
    exit()


if __name__ == '__main__':
    if len(sys.argv) == 1:
        try:
            main()
        except KeyboardInterrupt:
            print "Bye bye.."
            exit()
    else:
        show_usage()
