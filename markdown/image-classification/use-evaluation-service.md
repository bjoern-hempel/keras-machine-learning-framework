# Use the evaluation service

The problem with validating models is the time it takes to load the model, especially if it needs to be loaded into the graphics card memory first. 30 seconds is not uncommon. The validation itself takes only a few milliseconds. To solve the problem, the model must be loaded and kept in memory. The program then waits for the data to be validated. This process is also called service. This framework offers this functionality out of the box. The procedure for using this functionality is explained and shown below.

## First train the model

See the following link to do so: [Train, build and save the model](/markdown/image-classification/train-build-save.md)

## Then validate the data using the service mode

```bash
(keras-gpu) C:\Users> ml evaluate --verbose --service --yes --environment-path=C:/data \
    --config-file=food.inceptionv3.json --evaluation-path=_evaluation
```

The above command starts the service, loads the model and waits for new images in the folder `C:/data/_evaluation` to be validated. **Attention**: The images will be deleted immediately after the validation in the folder! Search for a picture for validation and wait for the result. Example based on this image: [pancake from Flickr by itslynzee](https://www.flickr.com/photos/81106231@N00/192310519)

<img src="/markdown/image-classification/pancake.jpg">

Save the image in the folder `C:/data/_evaluation`. The result could look like this:

<img src="/markdown/image-classification/pancake_predicted.png">

```bash
classes
-------
01) pancakes:                      99.96%
02) quesadilla:                     0.03%
03) guacamole:                      0.00%
...
-------
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

