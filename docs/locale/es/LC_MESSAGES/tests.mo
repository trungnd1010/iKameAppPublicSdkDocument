��    
      l               �   �   �      A  `   X  $  �     �  �   �  �   �  �     "   �  �  �  �   �     $  `   ;  $  �     �  �   �  �   r	  �   �	  "   �
   Before contributing to Read the Docs, make sure your patch passes our test suite and your code style passes our code linting suite. Continuous Integration In order to run all test including the search tests, include `"'--including-search'"` argument:: Read the Docs uses `Tox`_ to execute testing and linting procedures. Tox is the only dependency you need to run linting or our test suite, the remainder of our requirements will be installed by Tox into environment specific virtualenv paths. Before testing, make sure you have Tox installed:: Testing The RTD test suite is exercised by Travis CI on every push to our repo at GitHub. You can check out the current build status: https://travis-ci.org/rtfd/readthedocs.org The ``tox`` configuration has the following environments configured. You can target a single environment to limit the test suite:: To run the full test and lint suite against your changes, simply run Tox. Tox should return without any errors. You can run Tox against all of our environments by running:: To target a specific environment:: Project-Id-Version:  readthedocs-docs
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2018-09-17 19:05-0500
PO-Revision-Date: 2018-09-18 00:12+0000
Last-Translator: Anthony <aj@ohess.org>
Language: es
Language-Team: Spanish (http://www.transifex.com/readthedocs/readthedocs-docs/language/es/)
Plural-Forms: nplurals=2; plural=(n != 1)
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.6.0
 Before contributing to Read the Docs, make sure your patch passes our test suite and your code style passes our code linting suite. Continuous Integration In order to run all test including the search tests, include `"'--including-search'"` argument:: Read the Docs uses `Tox`_ to execute testing and linting procedures. Tox is the only dependency you need to run linting or our test suite, the remainder of our requirements will be installed by Tox into environment specific virtualenv paths. Before testing, make sure you have Tox installed:: Testing The RTD test suite is exercised by Travis CI on every push to our repo at GitHub. You can check out the current build status: https://travis-ci.org/rtfd/readthedocs.org The ``tox`` configuration has the following environments configured. You can target a single environment to limit the test suite:: To run the full test and lint suite against your changes, simply run Tox. Tox should return without any errors. You can run Tox against all of our environments by running:: To target a specific environment:: 