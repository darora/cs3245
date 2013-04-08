== General Notes ==

* I've chosen to use cElementTree, rather than lxml. This choice is
  based on--
  - benchmarks on http://lxml.de/performance.html (we're only
  concerned with parsing performance, and memory usage)

The overall strategy I've used for the assignment is largely similar
to my third assignment (tf-idf weighting), with a number of
modifications to take advantage of the additional information offered
by the structured data. Some of these are--

* The score for a term match is informed by which section of the
  patent application it occurred in. For instance, a title match would
  result in a higher score than a match within the abstract.

* Additional weighting based on citation analysis, based off ideas
  from "Enhancing Patent Retrieval by Citation Analysis" by Atsushi
  Fujii (SIGIR 2007). The default score for each document (i.e.
  patent) is 1.0
  The strategy then for each document is:
  - for each patent under the "Cited By" field:
    + if the patent is within our corpus, do nothing (will be handled
      later)
    + if the patent is _NOT_ within our corpus, add a default vote to
      the document's score
  - for each patent under the "Cites" field we add to _that_ patent's
    score a value of (1/|Cites|) where |Cites| is the count of patents
    listed within the "Cites" field of the current document

  The assumption of the default value could of course be side-stepped
  by querying an online patent database for documents not in our
  corpus. However, this would essentially becomes a depth-first
  search, so we'd likely have to "assume" a score at some tree depth
  of our choosing anyway.

*  Configurable signals to the algorithm (mostly within the utils.py
   file's Config hash):
   - a default vote for the citations whose values can't be
     ascertained
   - a percentile for the query terms, to act as a threshold below
     which the terms are discarded
   - a percentile for the matching documents, to act as a threshold
     below which the documents are discarded from the result set.

 

########## make tasks

* build_full_index: build index
* full_query: test the engine by using queries in the "queries_full" file


########## Optimizations

  
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
* Enhancing Patent Retrieval by Citation Analysis (Atsushi Fujii 2007)
* cElementTree documentation
