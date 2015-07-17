Before you start
---------------

1. Install `requests`, see http://requests.readthedocs.org/en/latest/user/install/


How to use it
-------------

Use `\cite{MR...}` in your LaTeX file to cite articles on MathSciNet, where `MR...` is the MSC identifier. Then:

1. Run `pdflatex` (or similar) on your file to get an updated `.aux` file
2. Run `python mscget.py` (update the hardcoded filename: I'll have to implement parameters I realise now)
3. Appropriately import `mr.bib`


Questions to myself
-------------------

* Which assumptions did I make are actually wrong?
* Is there a documented API for msnmain? I guess fn=130 is "make a request", but are there other interesting functions?
* What are the possible commands that can appear in the `.aux` that indicate a citation?
* Can I improve on handing certain HTTP status codes?

