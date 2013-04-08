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
  corpus. But this would increase our indexing time _significantly_.
  Fine if it's your job and it's running as a constant background
  process, not so fine if it's being timed & evaluated under testing
  conditions.
  
*  Configurable signals to the algorithm (mostly within the utils.py
   file's Config hash):
   - a default vote for the citations whose values can't be
     ascertained
   - a percentile for the query terms, to act as a threshold below
     which the terms are discarded
   - a percentile that configures the percentile of the result set to
     keep from the first round of matches (ref:query expansion)
   - a percentile for the matching documents, to act as a threshold
     below which the documents are discarded from the final result set.

########## Vocabulary mismatch
     
To deal with the problem of vocabulary mismatch, I've implemented a
very simple round of query expansion. Simply put, I first execute my
search code with the given query file as the input. I retain the 80th
percentile of these results[1], and process these into a query which is
run against the search code once again. The result set thus obtained
is processed as per usual (with the --doc-percentile threshold etc.)
and returned as the final results.

########## make tasks

* dev: builds the index
* output_[12]: executes the sample queries

* gui: a simple qt-based gui to examine the index & the citation
  weights
* test: [computation-heavy] plots the precision by varying the
  doc-percentile & term-percentile over the range [0.05, 0.95] with a
  0.10 step-size.

########## Optimizations

* query expansion: implemented in a separate branch (query_expansion),
  it did not [at the settings I tested it with] provide noticeable
  improvements for the precision. It did increase the execution time,
  and therefore I've disabled it for the moment.

* the search.py script takes in additional arguments
  --verbose: enables verbose output, mostly for debugging
  --term-percentile [X.XX]: defines the percentile of scored terms to
  		    be used for searching the corpus
  --doc-percentile [X.XX]: defines the percentile of matched documents
  		   to be returned as the result set.
  --query-expansion-percentile [X.XX]: the percentile for the first
  			       round of matches, which are used as the
			       input to another round of the search
			       code.

* I've used stemming. I found the PorterStemmer to be at the sweet
  spot of performance vs efficiency, as compared to lemmatization, and
  also other stemming algorithms. However, if we are to emphasize one
  over the other (between perf & efficiency, that is), we might want
  to pick an alternate algorithm.
  
== Files included with this submission ==

* index.py: a wrapper that deals with CLI stuff, and calls the indexer
  class from indexer.py
* indexer.py: the main index creation code
* citation_weight.py: creates an index of weights based on an analysis
  of the citations made by each of the patents

* search.py: search interface, as per assignment guidelines.

* makefile: for convenience

* diff_results.py: compares the sample output from the search.py
  script to the reference output, and prints the precision. Accepts
  the --verbose flag for a more detailed report.

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

Footnotes: 
[1]  This is done with the assumption that the first query itself
     would return a significant number of matches, and if we were to
     consider all of these (rather than just the ones that ranked
     among the highest) as plausible inputs for our next iteration of
     the search, our precision would go down drastically.

