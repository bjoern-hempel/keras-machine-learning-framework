# Keras Machine Learning Suite

This suite prepares, trains and validates an image classifier.

## Install Keras with GPU Support (Preparation)

* [Keras GPU Installation on Windows](markdown/installation/keras-gpu-windows.md)
* [Keras GPU Installation on Mac](markdown/installation/keras-gpu-mac.md)
* [Keras GPU Installation on Linux](markdown/installation/keras-gpu-linux.md) _(In progress)_

## Why is it important to choose a GPU over a CPU?

If you intend to implement and optimize Deep Neuronal Networks (DNN), the calculations must take place on the GPU. It is also possible to run calculations on the CPU. Also the installation of Keras for CPU driven computations is much easier, because the installation of the GPU drivers is not necessary. The disadvantage of this, however, is that it takes much longer to train larger models. Good models for the classification of e.g. pictures are only achieved after several training units. Training units require a lot of computing power in the form of many matrix operations. A GPU is predestined for matrix operations.

* [GPU vs CPU](markdown/hardware/gpu-vs-cpu.md)

## Python is not really intended for production environments

..but perfect for machine learning experiments. ;)

* [Cross-language model exchange (Python → JAVA)](markdown/cross-language/python-java.md)

## Some background knowledge

* Neuronal network vs Millions of parameters
* Transfer Learning
* ...

## First attempts to train an image classifier

* Train, build and save the model
* Preparations to make training more efficient
* ...

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
