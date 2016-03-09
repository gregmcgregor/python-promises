# python-promises
Promises for Python


 Promise package for Python 2.7+.  Node has such a wonderful way to handle server side.  With all of the debates
 on what to do with Python around GIL, I decided to support both GIL via threads and also multicore in the same
 API structure.

 Threads version (default) uses GIL and therefore all your data is thread safe.  It just runs.

 multicore uses multiprocessing.  Effectively, the script is forked to another core and the process is monitored.
   When the function finishes, one can return data but only if it is JSON seralizable. TBD:  Other means to
   share results from a process can be added.

 This is a good useable start!


 greg@brightappsllc.com - Copyright (c) 2016
