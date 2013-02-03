This is the README file for U000000X's submission

== General Notes about this assignment ==

# General methodology

I conducted tests for all the metrics suggested in the essay
questions, and a couple of others.

The complete list would be--

* [q1] token-based ngrams vs [1-5] length character based ngrams,
* [q3] stripping out punctuation and digits
* [q3] converting everything to lowercase vs leaving as it is
* [other] stripping out tokens that nltk detected as proper nouns
  ["NNP"]

TODO::Explain stripping away proper nouns

Therefore, the number of tests I conducted grew as O(2**n), but I
conducted less than that as I optimized away tests which trends could
show to be degrading the accuracy of the guesses.

# Results

Across all the tests I conducted on the given data sets, several
combination attained an accuracy of 0.8. For instance, this included
the most simple combination of no conversion to lowercase characters,
and no stripping of proper nouns.

However, the very best result (0.85) was restricted to the single
combination of using--

* conversion to lowercase
* no stripping of proper nouns
* using token-based ngrams

TODO::limit match to < 10, thereby detecting at least one "other"


== Files included with this submission ==

List the files in your submission here and provide a short 1 line
description of each file.  Make sure your submission's files are named
and formatted correctly.

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

* nltk documentation
* python language reference
* a few questions on the stackexchange family of sites referring to
  python usage
