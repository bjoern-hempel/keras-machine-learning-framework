# Train, build and save the model

...

## Train, build and save the model

The data set `./data/raw/flowers` is based on Kaggle's floral data set: https://www.kaggle.com/alxmamaev/flowers-recognition. The following command trains the specified data folder `./data/raw/flowers` and writes the calculated model to `./data/inceptionv3-trained.h5`.

```bash
(keras-gpu) C:\Users> ml train --data-path=./data/raw/flowers --model-file=./data/inceptionv3-trained.h5
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

A time overview and graphic can be found on the CPU/GPU comparison page: [GPU vs CPU](/markdown/hardware/gpu-vs-cpu.md)

### @NVIDIA GeForce GTX 1060 6GB (Desktop)

```bash
...
Epoch 1/10
135/135 [==============================] - 55s 405ms/step - loss: 0.8413 - acc: 0.6882
Epoch 2/10
135/135 [==============================] - 26s 195ms/step - loss: 0.5610 - acc: 0.7954
Epoch 3/10
135/135 [==============================] - 26s 190ms/step - loss: 0.4741 - acc: 0.8235
Epoch 4/10
135/135 [==============================] - 26s 190ms/step - loss: 0.4466 - acc: 0.8337
Epoch 5/10
135/135 [==============================] - 27s 196ms/step - loss: 0.3825 - acc: 0.8639
Epoch 6/10
135/135 [==============================] - 27s 202ms/step - loss: 0.4184 - acc: 0.8466
Epoch 7/10
135/135 [==============================] - 34s 252ms/step - loss: 0.3591 - acc: 0.8711
Epoch 8/10
135/135 [==============================] - 26s 192ms/step - loss: 0.3598 - acc: 0.8771
Epoch 9/10
135/135 [==============================] - 29s 213ms/step - loss: 0.3258 - acc: 0.8762
Epoch 10/10
135/135 [==============================] - 28s 207ms/step - loss: 0.3448 - acc: 0.8758

--- time measurement for "preparations": 17.5051s ---

--- time measurement for "fit": 303.5375s ---

--- time measurement for "save model": 33.7900s ---
```

### @NVIDIA GeForce GT 750M 2GB (Notebook)

```bash
...
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
...
Epoch 1/10
135/135 [==============================] - 948s 7s/step - loss: 0.8142 - acc: 0.6942
Epoch 2/10
135/135 [==============================] - 902s 7s/step - loss: 0.5621 - acc: 0.7942
Epoch 3/10
135/135 [==============================] - 870s 6s/step - loss: 0.4704 - acc: 0.8281
Epoch 4/10
135/135 [==============================] - 873s 6s/step - loss: 0.4600 - acc: 0.8223
Epoch 5/10
135/135 [==============================] - 908s 7s/step - loss: 0.3833 - acc: 0.8616
Epoch 6/10
135/135 [==============================] - 885s 7s/step - loss: 0.4216 - acc: 0.8456
Epoch 7/10
135/135 [==============================] - 933s 7s/step - loss: 0.3589 - acc: 0.8748
Epoch 8/10
135/135 [==============================] - 915s 7s/step - loss: 0.3564 - acc: 0.8741
Epoch 9/10
135/135 [==============================] - 898s 7s/step - loss: 0.3401 - acc: 0.8731
Epoch 10/10
135/135 [==============================] - 884s 7s/step - loss: 0.3475 - acc: 0.8760

--- time measurement for "preparations": 16.8698s ---

--- time measurement for "fit": 9016.7745s ---

--- time measurement for "save model": 28.6788s ---
```

### Intel(R) Core(TM) i7-3770 CPU @ 3.40GHz

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

