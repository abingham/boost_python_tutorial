boost_python_tutorial
=====================

*An IPython Notebook-based tutorial on Boost.Python*

This notebook introduces the main features of Boost.Python, a C++ library for interfacing CPython and C++ code. It covers topics including:

 * The core Boost.Python API
 * Writing extensions
 * Embedding Python in C++ programs
 * The basics of the Python C-API
 * Debugging across the languages
 * Managing exceptions across the language boundary

This notebook is a bit of an experiment, and is intended to serve two related purposes. First, it is used as the source for a set of "slides" for presentations. Second, it is a takeaway document for people who attend that presentation. The IPython notebook format straddles these two roles - presentation materials and study material - reasonably well, and it has the interesting benefit of supporting embedded executable code.

Using this notebook
-------------------

To do anything with this, you'll need to first install [IPython](http://ipython.org/).

The first way to view this notebook is using the standard `ipython notebook` command. To do this, just run that command from the `tutorial` directory:

```
% cd tutorial
% ipython notebook
```

The second intended way to use this notebook is as a slide deck. This relies on the `ipython nbconvert` command. In general, you just need to run this command from the `tutorial` directory:

```
ipython nbconvert Boost.Python.ipynb --to slides --post serve
```

This will generate the slides (using [reveal.js](http://lab.hakim.se/reveal-js/#/)) and then try to open a new browser tab with the slides.

The `bp_magic.py` extension
---------------------------

This notebook is all about mixing C++ and Python code. To support that, I developed an IPython extension that knows how to compile C++ code blocks into either shared library extension modules or into standalone programs. This extension is called `bp_magic` (for "boost python magic"), and it needs to be loaded prior to executing any of the C++ code blocks. If you execute the notebook linearly, the extension is loaded in time.

As of this writing the `bp_magic` extension is very fiddly and not likely to work on most systems. It *may* work on Mac OS X, there's less chance that it'll work on most Linux system, and there's essentially zero chance that it will work on Windows. There's nothing to prevent development of a more robust, cross-platform implementation, but I haven't had the time or motivation to do that yet.

If you want to make `bp_magic` work on your system, take a look at `tutorial/bp_magic.py`. It's relatively straightforward Python code, and it should be easy to rework it so that it works for you. I'm more than happy to integrate improvements to the script, so let me know if you've make any progress!

With that said, you don't really need a working `bp_magic` to use the notebook. You'll still be able to see all of the code examples; you just won't be able to execute them.
