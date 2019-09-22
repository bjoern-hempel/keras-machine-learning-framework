# Nine Points Demo

Imagine the following situation. We have given the following parameters:

Points around the x-values 1 and 0 as well as the y-values also around 1 and 0 should result in 1. Only the point [0.5, 0.5] should give 0:

<img src="/markdown/demos/nine_points.png">

This could simply be implemented algorithmically.

## Deductive learning approach

The deductive learning approach implements functions as they are. A sum, for example. 1 plus 1 should give 2. Or in other words, if I give 10 and 3 to the system, 13 should come out. For example, for the example above:

```python
if x in [0, 1] and y in [0, 1]:
    return 1
else
    return 0
```

This should work. But what happens when there are changes. E.g. that [0, 0] should also result in 0? It needs a programmer who changes the above source code and thinks about the problem! Wouldn't it make more sense if it also worked automatically? This is a simple example! What about more complex ones? E.g. the recognition of images? Implementing an algorithm is difficult, isn't it?

## Inductive learning approach

The indicative learning approach (and thus all artificial intelligence approaches) takes a different path: the learning process takes place through observation of the environment. A system is only given the start variables and the expected results from which the system is to learn. This is what makes machine learning so successful. Give a system the start variables and the expected results and let it learn! Learning by observing the environment!

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

