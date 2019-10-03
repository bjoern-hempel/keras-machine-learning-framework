# Evaluate the model

...

## Evaluate the model

Example based on this image: [Sunflower from Flickr by erikslife](https://www.flickr.com/photos/erikslife/36073451125)

<img src="/markdown/image-classification/sunflower.jpg">

```bash
(keras-gpu) C:\Users> ml evaluate --config-file=./data/inceptionv3-trained.json \
--evaluation-file=./data/eval/sunflower/1.jpg
Using TensorFlow backend.

general
-------
verbose:                  True
debug:                    False

data
----
environment_path:         F:/data
config_file:              F:/data/inceptionv3-trained.json
evaluation_file:          F:/data/eval/sunflower/1.jpg


Are these configurations correct? Continue? [Y/n] y


classes
-------
daisy:                8.53%
dandelion:            0.00%
rose:                 0.00%
sunflower:           91.47%
tulip:                0.00%
-------


predicted class:
----------------
predicted: sunflower
----------------

--- time measurement for "load json config file": 0.0010s ---

--- time measurement for "load model file": 19.4119s ---

--- time measurement for "load image file": 0.0353s ---

--- time measurement for "predict image file": 4.0958s ---
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

