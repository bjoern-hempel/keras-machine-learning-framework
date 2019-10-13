# Keras GPU Installation on Windows 10

* [Install NVIDIA Driver](#user-content-install-nvidia-driver)
* [Install Anaconda](#user-content-install-anaconda) and update Anaconda
* [Install CUDA Toolkit 10.0](#user-content-install-cuda-toolkit-100)
* [Save cuDNN and add the path to environment](#save-cudnn-and-add-the-path-to-environment)
* [Create environment and activate it](#user-content-create-environment-and-activate-it)
* [Test it!](#user-content-test-it)

## Install NVIDIA Driver

* [Download NVIDIA Driver](https://www.nvidia.com/Download/index.aspx?lang=en-us)
* For example, if you have a GTX 1060 6MB:
  * **Product Type:** GeForce
  * **Product Series:** GeForce 10 Series
  * **Product:** GeForce GTX 1060
  * **Operating System:** Windows 10 64-bit
  * **Windows Driver Type:** Standard
  * **Download Type:** Game Ready Driver (GRD)
  * **Language:**	English

## Install Anaconda

* Install the Windows Installer: Python 3.7 version
* [Download and install Anaconda](https://www.anaconda.com/distribution/)
  * Python 3.7 version
  * 64-Bit Graphical Installer

Open Anaconda Prompt:

* [Win] + s
* Enter: `anaconda`
* Open: Anaconda Prompt (Anaconda3)

And type the following commands to update Anaconda and all other libraries:

```bash
(base) C:\Users> conda update conda
(base) C:\Users> conda update --all
```

## Install CUDA Toolkit 10.0

* [Download CUDA Toolkit 10.0](https://developer.nvidia.com/cuda-downloads)
* Select Target Platform "Windows"
* Architecture: x86_64
* Version: 10
* exe (local)

## Save cuDNN and add the path to environment

* [Download cuDNN](https://developer.nvidia.com/rdp/cudnn-download)
* Extract the data at a location of your choice, eg. `C:\cuda`
* Add the `bin` path to the environment variable `path`:
  * [Win] + s
  * `env`
  * Edit system environment variables
  * Variable: Path
  * Add `C:\cuda\bin`
* Open Anaconda Prompt
  * `user$ echo %PATH%`
  * Should return: `...;C:\cuda\bin;...`

## Build the required python environment and activate it

Open Anaconda Prompt and create a GPU environment and if necessary an environment without GPU (only needed for comparison):

### With GPU support

```bash
(base) C:\Users> conda create -n keras-gpu python=3.6 numpy scipy keras-gpu matplotlib pillow
(base) C:\Users> conda activate keras-gpu
(keras-gpu) C:\Users>
```

### Without GPU support

```bash
(base) C:\Users> conda create -n keras python=3.6 numpy scipy keras matplotlib pillow
(base) C:\Users> conda activate keras
(keras) C:\Users>
```

## Test it!

### Some preparations

```bash
(base) C:\Users> conda install -c anaconda git
(base) C:\Users> git clone https://github.com/bjoern-hempel/keras-machine-learning-framework.git
(base) C:\Users> cd machine-learning-keras-framework
```

### Test the GPU environment

#### Switch to GPU environment

```bash
(base) C:\Users> conda activate keras-gpu
```

#### Build the command line execution script

```bash
(keras-gpu) C:\Users> cd machine-learning-keras-framework
(keras-gpu) C:\Users> pip install --editable .
...
(keras-gpu) C:\Users> where ml
C:\Users\[user]\Anaconda3\envs\keras-gpu\Scripts\ml.exe
```

#### Check environment

```bash
(keras-gpu) C:\Users> ml info

Available GPUs: 1

Available devices:
------------------
CPU: /device:CPU:0
GPU: /device:GPU:0 [GeForce GTX 1060 6GB]
------------------

Default device:
---------------
Device mapping:
/job:localhost/replica:0/task:0/device:GPU:0 -> device: 0, name: GeForce GTX 1060 6GB, ...
---------------

Information: You are running this script with GPU support.
```

### Test the CPU environment (just for comparison)

#### Switch to CPU environment

```bash
(base) C:\Users> conda activate keras
```

#### Build the command line execution script

```bash
(keras) C:\Users> cd machine-learning-keras-framework
(keras) C:\Users> pip install --editable .
...
(keras) C:\Users> where ml
C:\Users\[user]\Anaconda3\envs\keras-gpu\Scripts\ml.exe
```

#### Check environment

```bash
(keras) C:\Users> ml info

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

