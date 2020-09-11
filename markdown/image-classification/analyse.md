# Analyse the trained model (`ml analyse`)

## Validation part

```bash
(keras-gpu) C:\Users> ml analyse --environment-path=F:/data --config-file=processed/flower-12-MobileNetV2/model.json --yes
```

Analyzes the specified model (configuration file) and creates a confusion matrix:

* confusion_matrix_validation.pdf
* confusion_matrix_validation.png
* confusion_matrix_validation.svg

It also creates a temp file:

* evaluation-file-validation.json

The temporary file is used to speed up the creation of analysis files.

## Train part

```bash
(keras-gpu) C:\Users> ml analyse --analyse-type=train --config-file=F:/data/processed/flower-12-MobileNetV2/model.json --yes
```

Analyzes the specified model (configuration file) and creates a confusion matrix:

* confusion_matrix_train.pdf
* confusion_matrix_train.png
* confusion_matrix_train.svg

It also creates a temp file:

* evaluation-file-train.json

The temporary file is used to speed up the creation of analysis files.

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

