ux
==

*A Python package for Measuring and Analyzing User Experience.*

* Most software for analyzing UX is designed for in-person trials using small-population samples. While useful, this 
  approach suffers from the problem of sample bias.
* Site analytics platforms like Google Analytics are more geared to measuring conversion, click-through-rates and other 
  e-commerce type metrics. They focus more on what than why and are hard to customize.
* ux is a Python 3 package for conducting meaningful analysis of UX at scale. To install, type:

      pip install ux

* The first version deals specifically with usability metrics. Future versions will better support A/B testing, 
  hypothesis testing, behavioral inference and predictive UX interventions.


ux Data Classes
---------------

* Users take Sequences of Actions in Sessions. 
* Each Action takes place at a given time, at a given Location in the Application. 
* The Actions taken may or may not correspond to a Task.
* Each Task consists of a Sequence of Action Templates.

Analysis can be conducted offline e.g. in Jupyter notebooks, or integrated into a REST API and piped to a dashboard as 
JSON objects.

Database Manager
----------------

* Uses the [Facade Pattern](https://en.wikipedia.org/wiki/Facade_pattern) to a data store of underlying User Session 
  logs, providing a common querying interface to the UX Data Classes.
* Allows for switching out backend to different technologies e.g.  Firebase, BigQuery etc.

Calculations
------------

User Experience calculations are very simple, typically consisting of sums, averages and confidence intervals. The 
complexity comes from their application to large datasets, where we have to deal with questions such as:
* What is the definition of a Task for measuring success / completion etc?
* To what extent does the Sequence of Actions the User took match this predefined Task?

The calculation API deals mirrors these two levels of complexity, consisting of:
* Basic Calculations which deal with the nuts and bolts metrics calculations.
* Object Calculations, which provide convenient wrappers to the basic calculations in object methods.

Plots
-----

Visualization methods are provided in the plots sub-package. These methods reproduce the examples in Chapter 4 of the 
book [Measuring the User Experience](https://www.measuringux.com/book.htm), and some of the other methods described in 
the chapter.
