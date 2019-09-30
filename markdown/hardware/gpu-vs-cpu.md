# GPU vs CPU

Performance comparison based on the Kaggle floral data set training: https://www.kaggle.com/alxmamaev/flowers-recognition

InceptionV3 is used as the transfer learning model. The times were determined with the following standard command:

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

|                                                         | Preparation | Train       | Train (Factor) | Save model |
|---------------------------------------------------------|-------------|-------------|----------------|------------|
| NVIDIA GeForce GTX 1060 6GB (Desktop) - Windows                   | 17.5051s    | 303.5375s 00:05:03.5375   |  1.00x         | 33.7900s   |
| NVIDIA GeForce GT 750M 2GB (Notebook) - Windows                   | 18.3966s    | 2415.0062s  |  7.96x         | 29.7956s   |
| Intel(R) Core(TM) i7-6700HQ CPU @ 2.60GHz (Single Core) - MacOS   | still running :'D    |             |                |            |
| Intel(R) Core(TM) i7-4712HQ CPU @ 2.30GHz (Single Core) - Windows | 16.8698s    | 9016.7745s  | 29.71x         | 28.6788s   |
| Intel(R) Core(TM) i7-3770 CPU @ 3.40GHz (Single Core) - Windows   | 16.2699s    | 25183.4061s 06:59:43.4061 | 82.97x         | 28.3226s   |

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

