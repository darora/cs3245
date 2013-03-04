== General Notes ==

###### SkipList structure

The skiplists used for storing the postings lists is defined in the
skiplist.py file. It is a recursive singly-linked list, with
additional skip pointers.

###### Persistence to disk

I use the Pickle module to persist the dictionary & postings lists to
disk.
The dictionary contains, for each token, the index in the postings
file that should be "seek-ed" to, in order to obtain the beginning of
the corresponding postings skiplist. Once we've done this, we can
simple call pickle.load() on the FD, and it'd stop reading in the file
once it has unpickled one object (the skiplist we were after).

This allows us to read in only the necessary posting lists, without
having to deal with a lot of low-level IO.

###### Testing

In tests.py, I have a suite of unit tests that are used for ensuring
correct operation of--

* creation of the skip lists & their skip pointers
* merging of skip lists over OR|AND|NOT
* parsing of queries into trees in a variety of scenarios

Tests can be executed via the makefile--
,----
| $ make test
`----

This requires that the dict & postings file be already present. If
that is not the case, please run
,----
| $ make build_full_index test
`----






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

* skiplist.py: recursive singly-linked list definition

* parser.py: defines a binary tree data structure, and parses queries into such a structure

* tests.py: test suite using the unittests module

* makefile: for convenience





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
* http://www.peterbe.com/plog/uniqifiers-benchmark -- benchmarks
  different methods of making a list unique
