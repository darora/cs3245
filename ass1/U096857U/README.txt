This is the README file for U000000X's submission

== General Notes about this assignment ==

# General methodology

I conducted tests for some of the metrics suggested in the essay
questions, and a couple of others.

The complete list would be--

* [q1] token-based ngrams vs [1-5] length character based ngrams,
* [q3] converting everything to lowercase vs leaving as it is
* [other] stripping out tokens that nltk detected as proper nouns
  ["NNP"]

I tried out the idea of stripping out proper nouns as I suspected that
that might help with the accuracy of the LM. This was because I'd be
stripping out English proper nouns, and I hoped that these wouldn't
have much specificity to the language being considered.

I didn't test for the following metric:

* [q3] stripping out punctuation and digits

I did so because when I performed casual tests on a few of the
  configurations, stripping out typically didn't affect the accuracy,
  but did decrease the confidence of the matches.

# Testing

These three criteria resulted in 2 * 2 * 6 test cases.

I modified the code used for parsing the arguments passed to the
script, and added in arguments of my own for the four criteria that I
tested. In addition, I wrote the gen_makefile.py file (included) that
generates a makefile for the 40 cases.

Therefore, to test, one would--

,----
| $ make first
| $ make second
`----

(split across two tasks to use my processor's two cores; should be
executed in parallel in individual shells)

The makefile uses a sequence of unix utilities, rather than the python
eval script that was supplied, for performance reasons. Also, the
makefile contains a lot of redundant cases (when Tokenization = True,
it still varies the char length). (lazy; wontfix)

# Results

I found 3 combinations that resulted in a detection accuracy of 0.9:

  ** Lowercase: no,  Strip NNP: no, Character length: 4
  ** Lowercase: yes, Strip NNP: no, Character length: 3
  ** Lowercase: no,  Strip NNP: no, Character length: 3

== Files included with this submission ==

* build_test_LM.py

source code

* gen_makefile.py

generates the makefile

* makefile

includes the "first" and "second" tasks to execute all the test cases.

*

A list of *all* the test cases & the number of lines detected
incorrectly is included as output_counts with the format:

            """
            configuration_details (e.g. lower_(True|False)_strip_...)
            number of lines that were incorrectly guessed
            """

*

The detailed results for each configuration is also included as
files--
    ** {configuration_details}.output : in the same format as
       input.correct.txt (can be used with diff)
    ** {configuration_details}.output_prob: tuples of (language, probability)


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
