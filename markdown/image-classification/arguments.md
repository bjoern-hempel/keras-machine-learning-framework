# Arguments

## Arguments of the training process

```bash
(keras-gpu) C:\Users> ml train --help
Using TensorFlow backend.
Usage: ml train [OPTIONS]

  This subcommand trains a classifier.

Options:
  -m, --transfer-learning-model [DenseNet121|DenseNet169|DenseNet201|InceptionResNetV2|InceptionV3|NASNet|NASNetLarge|NASNetMobile|MobileNet|MobileNetV2|ResNet50|VGG19|Xception
]
                                  Sets the transfer learning model.
  --number-trainable-layers INTEGER
                                  Sets the number trainable layers.
  --input-dimension INTEGER       Sets the size of input dimension.
  --dense-size INTEGER            Sets the dense size.
  --dropout FLOAT RANGE           Sets the dropout value.
  --weights [imagenet]            Sets the database with which the weights are
                                  to be set (pre-trained transfer learning
                                  model).
  --neuronal-network-type [type-1|type-2|type-3]
                                  Sets the neuronal network type (type-1,
                                  type-2, type-3).
  --continue                      Continue learning with given model file.
  -e, --epochs INTEGER            Sets the number of epochs.
  --batch-size INTEGER            Sets the batch size.
  -a, --activation-function [elu|softmax|softplus|softsign|selu|relu|tanh|sigmoid|hard_sigmoid|exponential|linear]
                                  Sets the activation function (elu, softmax,
                                  softplus, softsign, selu, relu, tanh,
                                  sigmoid, hard_sigmoid, exponential, linear).
  --loss-function [mean_squared_error|categorical_crossentropy]
                                  Sets the loss function.
  -o, --optimizer [sgd|rmsprop|adagrad|adadelta|adam|adamax|nadam]
                                  Sets the optimizer (sgd, rmsprop, adagrad,
                                  adadelta, adam, adamax, nadam).
  -l, --learning-rate FLOAT       Sets the learning rate value.
  --learning-rate-drop FLOAT RANGE
                                  Sets the learning rate drop value.
  --learning-rate-epochs-drop INTEGER
                                  Sets the number of epochs after which the
                                  learning rate should decrease.
  --momentum FLOAT RANGE          Sets the momentum value.
  --decay FLOAT RANGE             Sets the decay value.
  --nesterov                      Switches on the nesterov mode.
  --metrics [accuracy]            Sets the metrics.
  --validation-split FLOAT RANGE  Sets the validation split.
  --environment-path PATH         Sets the environment path (used for example
                                  by --model-file, --config-file,
                                  --evaluation-path or --data-path).
  --model-file TEXT               Sets the model file where it should be saved
                                  or loaded.  [required]
  --data-path TEXT                The data path the model should learn from.
                                  [required]
  --model-source TEXT             Sets the source model if you want to
                                  continue learning from.
  --use-train-val                 Continue learning with given model file.
  -v, --verbose                   Switches the script to verbose mode.
  -d, --debug                     Switches the script to debug mode.
  -y, --yes                       Skip demands.
  --service                       Execute the given command as service.
  --http                          Execute the given command as http service.
  -r, --render-device [AUTO|CPU|CPU1|CPU2|CPU3|GPU|GPU1|GPU2|GPU3|PARALLEL]
                                  Specifies the device on which the
                                  calculation is to be performed.  [default:
                                  AUTO]
  --help                          Show this message and exit.
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

