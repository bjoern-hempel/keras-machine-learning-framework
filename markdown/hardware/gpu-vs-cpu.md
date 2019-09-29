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

|                                           | Preparation | Train       | Save model |
|-------------------------------------------|-------------|-------------|------------|
| NVIDIA GeForce GTX 1060 6GB (Desktop)     | 17.5051 s   | 303.5375 s  | 33.7900 s  |
| NVIDIA GeForce GT 750M 2GB (Notebook)     | 18.3966 s   | 2415.0062 s | 29.7956 s  |
| Intel(R) Core(TM) i7-4712HQ CPU @ 2.30GHz |             |             |            |
| Intel(R) Core(TM) i7-3770 CPU @ 3.40GHz   |             |             |            |

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

