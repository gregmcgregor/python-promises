
#
# Promise package for Python 2.7+.  Node has such a wonderful way to handle server side.  With all of the debates
# on what to do with Python around GIL, I decided to support both GIL via threads and also multicore in the same
# API structure.
#
# Threads version (default) uses GIL and therefore all your data is thread safe.  It just runs.
#
# multicore uses multiprocessing.  Effectively, the script is forked to another core and the process is monitored.
#   When the function finishes, one can return data but only if it is JSON seralizable. TBD:  Other means to
#   share results from a process can be added.
#
# This is a good useable start!
#
#
# greg@brightappsllc.com - Copyright (c) 2016
#
# To Be opensourced
#


from threading import Thread
from threading import Event
import time
from multiprocessing import Process, Queue
import json

version = "0.4"

# Our deferred object that can be held by your main code
class Deferred(object):

    def __init__(self):
        self._event = Event()
        self._rejected = False
        self._result = None

    def resolve(self, value):
        self._rejected = False
        self._result = value
        self._event.set()

    def reject(self, reason):
        self._rejected = True
        self._result = reason
        self._event.set()

    def promise(self):
        promise = Intent(self)
        return promise


# A Promise is an Intent to do something.  The Intent utilizes an IntentTask that does the actual calling
# of your function.  The Intent either resolves with a successful promise or rejected if it can't finish what
# it promised
class Intent(object):

    def __init__ (self,deferred ):
        self._deferred = deferred


    def then(self, multicore=False, resolved=None, rejected=None):
        defer = Deferred()
        global pool

        def task():
            try:

                # Important:  ALL data returned from your function must be JSON seralizable for mutlicore
                if multicore:
                    q = Queue ()
                    self._deferred.process = Process (target=self._deferred.runmc, args=(q,))
                    self._deferred.process.start()
                    self._deferred.process.join()
                    res = q.get()

                    if 'Error' in list(res):
                        results = json.loads ( res['Error'] )
                        self._deferred._rejected = True
                        self._deferred._result = results
                    else:
                        results = json.loads ( res['Success'])
                        self._deferred._result = results
                else:

                    Thread (target=self._deferred.run).start()
                    self._deferred._event.wait()

                if self._deferred._rejected:
                    result = self._deferred._result
                    if rejected:
                        result = rejected(self._deferred._result)

                    defer.reject(result)
                else:
                    result = self._deferred._result

                    if resolved:
                        result = resolved(self._deferred._result)

                    defer.resolve(result)


            except Exception as ex:
                defer.reject(ex.message)
                rejected (self._deferred._result)

        Thread(target=task).start()

        return defer.promise()

    def wait(self):
        self._deferred._event.wait()


    @staticmethod
    def wait_all(*args):
        for promise in args:
            if isinstance( promise, list):
                for item in promise:
                    item.wait ()
            else:
                promise.wait()

        ret = False

        # ANY promise we are waiting for MUST end with success or the chain fails
        for promise in args:
            if isinstance ( promise, list ):
                for item in promise:
                    ret = item._deferred._rejected
                    if ret == True:
                        return False
            else:
                ret = promise._deferred._rejected
                if ret == True:
                    return False

        return True

    # todo: Other logic for exiting promises


# The class that wraps your function and is hand's the user code a Promise to execute
class IntentTask (Deferred ):

    func = None
    args = None

    def setfunc ( self, func, *args):
        self.func = func
        if args:
            self.args = args


    def runmc ( self, q):
        if self.func:

            try :
                if self.args:
                    self._result = self.func(self.args)
                else:
                    self._result = self.func ()

                res = {'Success' : json.dumps ( self._result)}
                q.put ( res)
                self._event.set()

            except Exception as e:
                self._rejected = True
                self._result = e.message
                q.put ( {'Error' : json.dumps(self._result)} )
                self._event.set()

        else:
            # I am going to do nothing and be happy
            self._result = "Did nothing"
            self._event.set()


    def run (self ):
        if self.func:

            try :
                if self.args:
                    self._result = self.func(self.args)
                else:
                    self._result = self.func ()

                self._event.set()

            except Exception as e:
                self._rejected = True
                self._result = e.message
                self._event.set()
        else:
            # I am going to do nothing and be happy
            self._result = "Did nothing"
            self._event.set()


class Promise ( Intent ):

    def __init__ ( self, func=None, *args ):
        task = IntentTask()
        self.task = task
        super (Promise, self).__init__(task)
        if func:
            self.setup (func, *args)

    def setup (self, func, *args ):
        self.task.setfunc ( func, *args )
        return self

    # todo: this is going to change so that this is a dependant call .. do after
    # todo:  a do call after a then
    # todo:  Chaining promises






### TEST STUBS
###  TODO: Move to python test
###  TODO: create pip package


def myerror (result):

    print 'error'
    print result


def mysuccess (result):

    print 'mysuccess'
    print result


def sleep (args):
    print 'sleeping ' + str ( args[0])
    time.sleep(args[0])
    x = 1/0
    raise ValueError ('foo')



def mctest (args):
    ret = []

    for arg in args:
        ret.append (arg)

    ret.append ('Rocks')
    return ret

def dosomeloops():
    y = 3.14
    for x in range (0,1000000):
        y = y * 10.0;

def mcfail ():
    raise ValueError ('Test the failure case')


if __name__ == '__main__':

    t = time.clock()

    p = Promise (sleep, 1).then(rejected=myerror)
    p.wait ()

    #Multicore
    p = Promise(mcfail).then (multicore=True, rejected=myerror)
    p.wait()

    for x in range (0, 10):
        dosomeloops()
    e = time.clock ()
    print e-t

    p = []
    p.append (Promise(mctest, 'Erin', 'Greg', 'Mallorie', 'Josie', 'Emma').then (multicore=True, resolved=mysuccess, rejected=myerror))

    t = time.clock()

    for x in range (0, 10):
        p.append ( Promise (dosomeloops).then (multicore=True))

    if Promise.wait_all ( p ):
        print 'Success'

    e = time.clock ()
    print e-t

    #Thread
    t = time.clock()

    p = []
    for x in range ( 0, 10):
         p.append(Promise(dosomeloops).then())

    if Promise.wait_all( p ):
        print 'Success'
    e = time.clock ()
    print e-t


    #m = model ()

    #loadmodel(m)

    #p2 = Promise().do( loadbigrams, m ).then (resolved=mysuccess, rejected=myerror)

    #if Promise.wait_all ( p2 ):
     #   print 'groovy'


    #p = []
    #for x in range ( 0,  10):
     #   p.append (Promise().do( heatword2vec, 3, m).then (resolved=mysuccess, rejected=myerror))


    #p5 = Promise ( loadtrigrams).then()


    #if Promise.wait_all( p, p5):
     #   print 'All promises we were interested in successfully completed'



    print 'All promises done'
