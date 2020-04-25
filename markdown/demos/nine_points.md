# Nine Points Demo

Imagine the following situation and parameters:

Points around the x<sub>1</sub>-values 1 and 0 as well as the x<sub>2</sub>-values also around 1 and 0 should return 1. Only the point [0.5, 0.5] should give 0:

<img src="/markdown/demos/nine_points.png">

This could simply be implemented algorithmically with the deductive learning approach:

## Deductive learning approach

The deductive learning approach implements functions as they are as an algorithm. A sum, for example. 1 plus 1 should give 2. Or in other words, if I give 10 and 3 to the system, 13 should come out. A deductive learning approach for the case above would be for example:

```python
if x1 in [0, 1] or x2 in [0, 1]:
    return 1
else
    return 0
```

This should work. But what happens when there are changes. E.g. that [0, 0] should also result in 0? It needs a programmer who changes the above source code and thinks about the problem! Wouldn't it make more sense if it also worked automatically? This is a simple example! What about more complex ones? For example the recognition of images? Implementing an algorithm is difficult, isn't it?

## Inductive learning approach

The indicative learning approach (and thus all artificial intelligence approaches) takes a different path: the learning process takes place through observation of the environment. A system is only given the start variables and the expected results from which the system is to learn. This is what makes machine learning so successful: Give a system the start variables and the expected results and let it learn! Learning by observing the environment!

## Inductive vs deductive in graphical form

In other words, in the deductive approach, the model is written by hand (algorithm) to obtain the output:

<img src="/markdown/demos/deductive.png">

In the indicative procedure, we also have given the output set for an input set. An algorithm tries to create a model from these two sets that comes closest to it. The automatically created model can be used to predict the output from a given input, as with the deductive method:

<img src="/markdown/demos/inductive.png">

## A. Further Tutorials

* [An introduction to artificial intelligence](https://github.com/friends-of-ai/an-introduction-to-artificial-intelligence)

## B. Sources

* ...

## C. Authors

* Björn Hempel <bjoern@hempel.li> - _Initial work_ - [https://github.com/bjoern-hempel](https://github.com/bjoern-hempel)

## D. License

This tutorial is licensed under the MIT License - see the [LICENSE.md](/LICENSE.md) file for details

## E. Closing words

Have fun! :)

