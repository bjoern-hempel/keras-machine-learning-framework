# Keras GPU Installation on Mac

* [Install CUDA Driver](#user-content-install-cuda-driver)
* [Install Anaconda](#user-content-install-anaconda) and update Anaconda
* [Install CUDA Toolkit 10.1](#user-content-install-cuda-toolkit-101)
* [Save cuDNN and add the path to environment](#save-cudnn-and-add-the-path-to-environment)
* [Create environment and activate it](#user-content-create-environment-and-activate-it)
* [Test it!](#user-content-test-it)

## Install CUDA Driver

* [Download CUDA Driver](https://www.nvidia.de/object/mac-driver-archive-de.html)
* Install the latest one

## Install Anaconda

* Install the Windows Installer: Python 3.7 version
* [Download and install Anaconda](https://www.anaconda.com/distribution/)
  * Python 3.7 version
  * 64-Bit Graphical Installer

Open a terminal and type the following commands to update Anaconda and all other libraries:

```bash
(base) user$ conda update conda
(base) user$ conda update --all
```

## Install CUDA Toolkit 10.1

* [Download CUDA Toolkit 10.1](https://developer.nvidia.com/cuda-downloads)
* Select Target Platform "Mac OSX"
* Architecture: x86_64
* Version: 10.13
* dmg (local)

## Save cuDNN and add the path to environment

* [Download cuDNN v7.6.3 (August 23, 2019), for CUDA 10.1](https://developer.nvidia.com/rdp/cudnn-download) (cuDNN Library for OSX)
* Extract the data at a location of your choice, eg. `/cuda`
* Add the `bin` path to the environment variable `path` (`~/.bash_profile`):
```
export PATH=/cuda/bin${PATH:+:${PATH}}
export DYLD_LIBRARY_PATH=/cuda/lib${DYLD_LIBRARY_PATH:+:${DYLD_LIBRARY_PATH}}
```
* Open a terminal
  * `(base) user$ echo $PATH`
  * Should return: `...:/cuda/bin:...`
  * `(base) user$ echo $DYLD_LIBRARY_PATH`
  * Should return: `...:/cuda/lib:...`

## Build the required python environment and activate it

Open Anaconda Prompt and create a GPU environment and if necessary an environment without GPU (only needed for comparison):

### With GPU support

```bash
(base) user$ conda create -n keras-gpu python=3.6 numpy scipy keras-gpu
(base) user$ conda activate keras-gpu
(keras-gpu) user$
```

### Without GPU support

```bash
(base) user$ conda create -n keras python=3.6 numpy scipy keras
(base) user$ conda activate keras
(keras) user$
```

## Test it!

### Some preparations

```bash
(base) user$ conda install -c anaconda git
(base) user$ git clone https://github.com/bjoern-hempel/keras-machine-learning-suite.git
(base) user$ cd machine-learning-keras-suite
```

### Test the GPU environment

#### Switch to GPU environment

```bash
(base) user$ conda activate keras-gpu
```

#### Build the command line execution script

```bash
(keras-gpu) user$ cd machine-learning-keras-suite
(keras-gpu) user$ pip install --editable .
...
(keras-gpu) user$ which ml
/anaconda3/envs/keras-gpu/bin/ml
```

#### Check environment

```bash
(keras-gpu) user$ ml info

Available GPUs: 1

Available devices:
------------------
CPU: /device:CPU:0
GPU: /device:GPU:0 [GeForce GT 650M 512MB]
------------------

Default device:
---------------
Device mapping:
/job:localhost/replica:0/task:0/device:GPU:0 -> device: 0, name: GeForce GT 650M 512MB, ...
---------------

Information: You are running this script with GPU support.
```

### Test the CPU environment (just for comparison)

#### Switch to CPU environment

```bash
(base) user$ conda activate keras
```

#### Build the command line execution script

```bash
(keras) user$ cd machine-learning-keras-suite
(keras) user$ pip install --editable .
...
(keras) user$ where ml
/anaconda3/envs/keras/bin/ml
```

#### Check environment

```bash
(keras) user$ ml info

Available GPUs: 0

Available devices:
------------------
CPU: /device:CPU:0
------------------

Default device:
---------------
Device mapping: no known devices.
---------------

Attention: You are running this script without GPU support.
```

## A. Further Tutorials

* [An introduction to artificial intelligence](https://github.com/friends-of-ai/an-introduction-to-artificial-intelligence)

## B. Sources

* [Keras Tensorflow Windows Installation](https://github.com/antoniosehk/keras-tensorflow-windows-installation)

## C. Authors

* Björn Hempel <bjoern@hempel.li> - _Initial work_ - [https://github.com/bjoern-hempel](https://github.com/bjoern-hempel)

## D. License

This tutorial is licensed under the MIT License - see the [LICENSE.md](/LICENSE.md) file for details

## E. Closing words

Have fun! :)
