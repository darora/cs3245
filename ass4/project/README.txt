== General Notes ==

* I've chosen to use cElementTree, rather than lxml. This choice is
  based on--
  - benchmarks on http://lxml.de/performance.html (we're only
  concerned with parsing performance, and memory usage)
 














Most of my code is pretty blatantly copied over from my second
assignment, except it now uses much speedier native python data
structures rather than my slow implementation of skiplists.

########## make tasks

* build_full_index: build index
* full_query: test the engine by using queries in the "queries_full" file


########## Optimizations

* Dis-regarding low-idf terms from the query.
  If I stop taking these terms into account, I only get slight
  degradation--if it can be called that--in the search results lists.
  In some simple tests, I attained differing results (or results in
  differing order) nearly 25% of the time.

  However, doing so gave me a 10% decrease in time taken for the
  searches. Depending on the goals of the system, if might be worth
  the degradation. [Disabled by default]

* Not using a heap for selecting top-k results.
  Python's heap implementation is a min-heap (heapq), and more
  importantly, doesn't accept a custom comparator function. Therefore,
  using a heap in this case would either call for my own
  implementation based off of the python library's one, or have a very
  complicated two-pass sort to ensure that I received the docs with
  the lower docIds.

  I opted to use a more simple, elegant sort for the entire results,
  although slightly more inefficient.
  
== Files included with this submission ==

* index.py: main indexer, as per assignment guidelines.
  - Use "make build_full_index" as a shortcut.

* search.py: search interface, as per assignment guidelines.
  - Use "make full_query" for use with the included sample queries
    from queries_full (sourced from IVLE forum)
  - Also includes a CLI mode for iterative testing of queries. In
    order to access this--
    1. open file in editor
    2. scroll to bottom, comment out call to main()
    3. uncomment call to manual_mode()
    4. don't forget to undo these changes once you're done testing!

* makefile: for convenience

* compare_lengths.py: test the average length of the results being
  returned by the search engine, compared to baseline to lnn.ltc


== Statement of individual work ==

Please initial one of the following statements.

[x] I, U096857U, certify that I have followed the CS 3245 Information
Retrieval class guidelines for homework assignments.  In particular, I
expressly vow that I have followed the Facebook rule in discussing
with others in doing the assignment and did not take notes (digital or
printed) from the discussions.  

[ ] I, U000000X, did not follow the class rules regarding homework
assignment, because of the following reason:

<Please fill in>

I suggest that I should be graded as follows:

<Please fill in>

== References ==

<Please list any websites and/or people you consulted with for this
assignment and state their role>

* python language reference
