# GPU vs CPU

Performance comparison based on the Kaggle floral data set training: https://www.kaggle.com/alxmamaev/flowers-recognition This picture set consists of 5 classes with about 4350 training pictures.

The training time includes 10 training epochs, whereby InceptionV3 was used as a transfer learning model. The times were determined with the following standard command:

```bash
(keras-gpu) C:\Users> ml train --data-path=./Data/raw/flowers --model-file=./Data/inceptionv3-trained.h5

Using TensorFlow backend.

general
-------
verbose:                  False
debug:                    False

transfer_learning
-----------------
data_path:                ./Data/raw/flowers
transfer_learning_model:  InceptionV3
number_trainable_layers:  305
input_dimension:          299
dense_size:               512
dropout:                  0.5
weights:                  imagenet

machine_learning
----------------
model_file:               ./Data/inceptionv3-trained.h5
epochs:                   10
learning_rate:            0.001
activation_function:      tanh
loss_function:            mean_squared_error
optimizer:                adam
metrics:                  accuracy
environment_path:         None


Are these configurations correct? Continue? [Y/n] y
```

## Comparison

The exact output of the mentioned commands can be viewed here: [Train, build and save the model](/markdown/image-classifier/train-build-save.md)

|                                                                   | Preparation | Train       | Train (Factor) | Save model |
|-------------------------------------------------------------------|-------------|-------------|----------------|------------|
| NVIDIA GeForce GTX 1060 6GB (Desktop) - Windows                   | 17.5s    | 303.5s 00:05:03.5   |  1.00x        | 33.8s   |
| NVIDIA GeForce GT 750M 2GB (Notebook) - Windows                   | 18.4s    | 2415.0s 00:40:15.0  |  7.96x        | 29.8s   |
| Intel(R) Core(TM) i7-6700HQ CPU @ 2.60GHz (Single Core) - MacOS   | 17.5s    | 17110.1s 04:45:10.1 | 56.37x        | 131.7s  |
| Intel(R) Core(TM) i7-4712HQ CPU @ 2.30GHz (Single Core) - Windows | 16.9s    | 9016.8s 02:30:16.8  | 29.71x        | 28.7s   |
| Intel(R) Core(TM) i7-3770 CPU @ 3.40GHz (Single Core) - Windows   | 16.3s    | 25183.4s 06:59:43.4 | 82.97x        | 28.3s   |

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

