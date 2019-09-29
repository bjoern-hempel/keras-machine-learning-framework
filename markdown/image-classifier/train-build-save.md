# Train, build and save the model

...

## Train, build and save the model

Data set based on Kaggle's floral data set: https://www.kaggle.com/alxmamaev/flowers-recognition

### @NVIDIA GeForce GT 750M - 2GB

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

Epoch 1/10
135/135 [==============================] - 233s 2s/step - loss: 0.8411 - acc: 0.6910
Epoch 2/10
135/135 [==============================] - 236s 2s/step - loss: 0.5703 - acc: 0.7919
Epoch 3/10
135/135 [==============================] - 238s 2s/step - loss: 0.4762 - acc: 0.8242
Epoch 4/10
135/135 [==============================] - 238s 2s/step - loss: 0.4377 - acc: 0.8385
Epoch 5/10
135/135 [==============================] - 244s 2s/step - loss: 0.3846 - acc: 0.8646
Epoch 6/10
135/135 [==============================] - 245s 2s/step - loss: 0.4335 - acc: 0.8407
Epoch 7/10
135/135 [==============================] - 244s 2s/step - loss: 0.3623 - acc: 0.8741
Epoch 8/10
135/135 [==============================] - 245s 2s/step - loss: 0.3620 - acc: 0.8743
Epoch 9/10
135/135 [==============================] - 256s 2s/step - loss: 0.3369 - acc: 0.8773
Epoch 10/10
135/135 [==============================] - 236s 2s/step - loss: 0.3477 - acc: 0.8793

--- time measurement for "preparations": 18.3966s ---

--- time measurement for "fit": 2415.0062s ---

--- time measurement for "save model": 29.7956s ---     
```

### @Intel(R) Core(TM) i7-4712HQ CPU @ 2.30GHz

```bash

```

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

