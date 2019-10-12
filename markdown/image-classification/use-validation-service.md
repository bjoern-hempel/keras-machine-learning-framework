# Use the validation service

The problem with validating models is the time it takes to load the model, especially if it needs to be loaded into the graphics card memory first. 30 seconds is not uncommon. The validation itself takes only a few milliseconds. To solve the problem, the model must be loaded and kept in memory. The program then waits for the data to be validated. This process is also called service. This framework offers this functionality out of the box. The procedure for using this functionality is explained and shown below.

## First train the model

```bash
(keras-gpu) C:\Users> ml train --verbose --batch-size=8 -e 20 --learning-rate-epochs-drop=10 -m InceptionV3 \
    --number-trainable-layers=-1 --environment-path=C:/data --model-file=food.h5 --data-path=raw/food
Using TensorFlow backend.

general
-------
verbose:                   True
debug:                     False

machine_learning
----------------
batch_size:                8
epochs:                    20
learning_rate_epochs_drop: 10
activation_function:       tanh
loss_function:             categorical_crossentropy
optimizer:                 sgd
learning_rate:             0.001
learning_rate_drop:        0.5
momentum:                  0.9
decay:                     0.0
nesterov:                  True
metrics:                   accuracy
validation_split:          0.2

transfer_learning
-----------------
transfer_learning_model:   InceptionV3
number_trainable_layers:   -1
input_dimension:           299
dense_size:                512
dropout:                   0.5
weights:                   imagenet
continue:                  False

data
----
environment_path:          C:/data
model_file:                C:/data/food.inceptionv3.h5
data_path:                 C:/data/raw/food
config_file:               C:/data/food.inceptionv3.json
best_model_file:           C:/data/food.inceptionv3.best.{epoch:02d}-{val_acc:.2f}.h5
accuracy_file:             C:/data/food.inceptionv3.png
log_file:                  C:/data/food.inceptionv3.log
csv_file:                  C:/data/food.inceptionv3.csv


Are these configurations correct? Continue? [Y/n] y



-> Start "overall".


-> Start "preparations".
Found 11913 images belonging to 50 classes.
Found 2953 images belonging to 50 classes.
<- Finished "preparations" (16.6308s).

LAYERS
------
0 :  input_1 (not trainable)
1 :  conv2d_1 (trainable)
2 :  batch_normalization_1 (trainable)
...
313 :  dropout_1 (trainable)
314 :  dense_2 (trainable)
315 :  activation_95 (trainable)
------

CLASSES
-------
{'baked_beans': 0, 'baked_salmon': 1, 'beef_stew': 2, 'beef_stroganoff': 3, 'brownies': 4, 'bundt_cake': 5, 'burger': 6, 'burrito': 7, 'buttermilk_biscuits': 8, 'caesar_salad': 9, 'calzone': 10, 'cheesecake': 11, 'chicken_piccata': 12, 'chicken_wings': 13, 'cinnamon_roll': 14, 'cobb_salad': 15, 'coleslaw': 16, 'corn_dog': 17, 'creamed_spinach': 18, 'donut': 19, 'empanada': 20, 'french_fries': 21, 'frittata': 22, 'granola_bar': 23, 'grilled_cheese_sandwich': 24, 'guacamole': 25, 'ice_cream': 26, 'kebabs': 27, 'key_lime_pie': 28, 'lasagne': 29, 'macaroni_and_cheese': 30, 'margarita': 31, 'martini': 32, 'mashed_potatoes': 33, 'meatballs': 34, 'meatloaf': 35, 'muffin': 36, 'nachos': 37, 'omelet': 38, 'pancakes': 39, 'pizza': 40, 'popcorn': 41, 'quesadilla': 42, 'salad': 43, 'sloppy_joe': 44, 'smoothie': 45, 'soup': 46, 'spaghetti': 47, 'stuffed_pepper': 48, 'waffles': 49}
-------

-> Start "fit".
Epoch 1/20

Epoch 00001: LearningRateScheduler setting learning rate to 0.001.
1489/1489 [==============================] - 403s 271ms/step - loss: 2.1907 - acc: 0.4269 - val_loss: 1.2153 - val_acc: 0.6728

Epoch 00001: val_acc improved from -inf to 0.67276, saving model to C:/data/food_3.inceptionv3.best.01-0.67.h5
Epoch 2/20

Epoch 00002: LearningRateScheduler setting learning rate to 0.001.
1489/1489 [==============================] - 380s 255ms/step - loss: 1.2329 - acc: 0.6587 - val_loss: 1.1075 - val_acc: 0.6978

...

Epoch 00019: LearningRateScheduler setting learning rate to 0.0005.
1489/1489 [==============================] - 406s 273ms/step - loss: 0.0448 - acc: 0.9868 - val_loss: 0.9251 - val_acc: 0.8092

Epoch 00019: val_acc did not improve from 0.80951
Epoch 20/20

Epoch 00020: LearningRateScheduler setting learning rate to 0.0005.
1489/1489 [==============================] - 404s 272ms/step - loss: 0.0364 - acc: 0.9895 - val_loss: 0.9661 - val_acc: 0.8024

Epoch 00020: val_acc did not improve from 0.80951
<- Finished "fit" (130017.1215s).


-> Start "save model".
<- Finished "save model" (5.8552s).


-> Start "save config".
Write config file to C:/data/food.inceptionv3.json
<- Finished "save config" (0.0070s).
<- Finished "overall" (132304.3207s).

--- time measurement for "overall": 132304.3207s ---

--- time measurement for "preparations": 16.6308s ---

--- time measurement for "fit": 130017.1215s ---

--- time measurement for "save model": 5.8552s ---

--- time measurement for "save config": 0.0070s ---
```

## Use the model for evaluation as a service

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
