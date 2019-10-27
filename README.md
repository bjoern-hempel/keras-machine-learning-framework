# Keras Machine Learning Framework

This machine learning framework prepares, trains and validates an image classifier.

## Install Keras with GPU Support (Preparation)

* [Keras GPU Installation on Windows](/markdown/installation/keras-gpu-windows.md)
* [Keras GPU Installation on Mac](/markdown/installation/keras-gpu-mac.md)
* [Keras GPU Installation on Linux](/markdown/installation/keras-gpu-linux.md) _(In progress)_

## Why is it important to choose a GPU over a CPU?

If you intend to implement and optimize Deep Neuronal Networks (DNN), the calculations must take place on the GPU. It is also possible to run calculations on the CPU. Also the installation of Keras for CPU driven computations is much easier, because the installation of the GPU drivers is not necessary. The disadvantage of this, however, is that it takes much longer to train larger models. Good models for the classification of e.g. pictures are only achieved after several training units. Training units require a lot of computing power in the form of many matrix operations. A GPU is predestined for matrix operations<sup>[[1]](#gpumatrixmult)</sup>.

* [GPU vs CPU](markdown/hardware/gpu-vs-cpu.md)

## Python is not really intended for production environments

..but perfect for machine learning experiments. ;)

* [Cross-language model exchange (Python → JAVA)](/markdown/cross-language/python-java.md)

## Some background knowledge

* [The deductive learning approach versus the inductive learning approach: see nine points demo](/markdown/demos/nine_points.md)
* Neuronal network vs Millions of parameters
* Transfer Learning
* ...

## Demos

To test this framework immediately without any data, there is a selection of demos which can be executed immediately. Good to e.g. test the installation or make a GPU vs CPU comparison on the fly.

Here is an overview of the demos:

* [Demo Overview](/markdown/demos/overview.md)

## First attempts to train an image classifier

* [Train, build and save the model](/markdown/image-classification/train-build-save.md)
* Preparations to make training more efficient
* [Evaluate a given image](/markdown/image-classification/evaluate.md)
* [Transfer learning](/markdown/image-classification/transfer-learning.md)
* ...

## Further attempts

* [Use the evaluation service](/markdown/image-classification/use-evaluation-service.md)
* [Use the http webservice for evaluation](/markdown/image-classification/use-http-webservice.md)

## A. Further Tutorials

* [An introduction to artificial intelligence](https://github.com/friends-of-ai/an-introduction-to-artificial-intelligence)

## B. Sources

* <sup><a name="gpumatrixmult">[1]</a></sup>[Understanding the Efficiency of GPU Algorithms for Matrix-Matrix Multiplication](https://graphics.stanford.edu/papers/gpumatrixmult/gpumatrixmult.pdf)
* <sup><a name="stillinprogress">[2]</a></sup>[What Does Classifying More Than 10,000 Image Categories Tell Us?](http://vision.stanford.edu/pdf/DengBergLiFei-Fei_ECCV2010.pdf)

## C. Authors

* Björn Hempel <bjoern@hempel.li> - _Initial work_ - [https://github.com/bjoern-hempel](https://github.com/bjoern-hempel)

## D. License

This tutorial is licensed under the MIT License - see the [LICENSE.md](/LICENSE.md) file for details

## E. Closing words

Have fun! :)
