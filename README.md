# python-promises
Promises for Python

This project was made to merge Multicore processing and threading in python via a node Javascript style promises package.  Having simple power over GIL and multi-core with the beauty of Promises is nice

## Install
pip install gofast

## Examples

```python

import gofast.promise as Q

def somefunction (args):
    print 'hi'
    
def crunchnumber ( args ):
    pi = 3.14
    for x in range ( 0, 1000000):
        pi = pi * pi
    # Could use args and compute neural nets or cpu intensive work - this was called multicore
    
    return pi

# Simple case

p = Q.Promise(somefunction).then (rejected=myerror)
# Executed with no waiting.  myerror is called if there was a problem

# Wait Case
p = Q.Promise (somefunction).then (resolved=mysuccess)
if p.wait(): 
    print 'all completed successfully'

# Mixing threads and Multiprocessing ones
for x in range (0,20):
     p.append ( Promise (crunchnumber, somemodel, somestart).then ( multicore=True, resovled=get_computation_result)

for x in range (0,10:
     p.append ( Promise (someiofunction).then ()
     
# Wait for all threads and multi-core promises to finish
Q.Promise.wait_all ( p )
 ```

## Why ?

 For Python 2.7+.  Node has such a wonderful way to handle server side.  With all of the debates
 on what to do with Python around GIL, I decided to support both GIL via threads and also multicore in the same
 API structure.  We are doing data science work and need multi-core there and threads for I/O

 Threads version (default) uses GIL and therefore all your data is thread safe.  It just runs.

 Multicore uses multiprocessing.  Effectively, the script is forked to another core and the process is monitored.
   When the function finishes, one can return data but only if it is JSON seralizable. 

 Notes: For I/O blocking requests, threads keeps it simple as it uses GIL and you don't have to worry about thread locking or safety.  However, for true multicore processing, you can set multicore=true and bypass GIL.  This is fantastic for hard computing tasks and when you need the computing power of the machine.  Same syntax, just a flag.
 
 
