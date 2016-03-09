# python-promises
Promises for Python

This project was made to merge Multic-core processing and threading in python via a node Javascript style promises package.

## Examples

```python

# Simple case

p = Promise(somefunction).then (rejected=myerror)
# Executed with no waiting.  myerror is called if there was a problem

# Wait Case
p = Promise (somefunction).then (resolved=mysuccess)
if p.wait(): 
    print 'all completed successfully'

# Mixing threads and Multiprocessing ones
for x in range (0,20):
     p.append ( Promise (crunchnumber, somemodel, somestart).then ( multicore=True)

for x in range (0,10:
     p.append ( Promise (someiofunction).then ()
     
# Wait for all threads and multi-core promises to finish
Promise.wait_all ( p )
 ```

## Why ?

 Promise package for Python 2.7+.  Node has such a wonderful way to handle server side.  With all of the debates
 on what to do with Python around GIL, I decided to support both GIL via threads and also multicore in the same
 API structure.

 Threads version (default) uses GIL and therefore all your data is thread safe.  It just runs.

 Multicore uses multiprocessing.  Effectively, the script is forked to another core and the process is monitored.
   When the function finishes, one can return data but only if it is JSON seralizable. TBD:  Other means to
   share results from a process can be added.

 For I/O blocking requests, threads keeps it simple as it uses GIL and you don't have to worry about thread locking or safety.  However, for true multicore processing, you can set multicore=true and bypass GIL.  This is fantastic for hard computing tasks and when you need the computing power of the machine.  Same syntax, just a flag.
 
 This is a good useable start!


 greg@brightappsllc.com - Copyright (c) 2016
