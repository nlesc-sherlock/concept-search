# Concept Search for Exploratory Data Analysis

Some pointers to get started:

* [Get the data](https://github.com/nlesc-sherlock/concept-search/blob/develop/GettingTheData.ipynb)
(IPython notebook)
* [Text feature extraction using scikit-learn](http://scikit-learn.org/stable/modules/feature_extraction.html#text-feature-extraction)
* Given a term-document matrix _A_ (where cell _t_, _d_ contains the weight of term _t_ in document _d_),
the term-term correlation matrix is _A_*_A_.T (see
[Automatic Query Expansion in Information Retrieval](http://www-labs.iro.umontreal.ca/~nie/IFT6255/carpineto-Survey-QE.pdf),
page 13, above equation 5).

# Installation

pandas Flask Flask-cors nltk vincent elasticsearch sklearn