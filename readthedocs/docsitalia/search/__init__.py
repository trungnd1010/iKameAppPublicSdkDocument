"""
Docs Italia search module.

A separate index has been defined (with related documents registered) to have
a single dedicated search and greater speed possible in indexing, searching
and reporting data (since the documents do not contain all the attributes,
even complex of the other indexes).

Tests were carried out using the existing RTD indexes and the speed was not
satisfactory as well as not working due to the following:
- the ES full-text analyzer is designed for the needs of a search engine,
  so to assess the relevance between entire searched phrases and long texts,
  while in this specific search the requirement is to find with accuracy short
  mounts of characters inside not very long individual titles, for this reason
  the currently implemented analyzer (ie "italian") is not good (to the best of
  our knowledge and tests), for this reason the Trigram mechanism (similar to
  that of PostgreSQL) was used, which allows to have results even with a few
  characters searched (eg returns correctly the titles containing "document/s"
  if you type "doc", which in the other case does not happen) and robustness
  with respect to simple typing errors.

The search can be further optimized by adjusting the parameters of the Trigram
or by choosing a different analyzer, in this regard a good number of
investigations and attempts have been made without finding better solutions.
"""
