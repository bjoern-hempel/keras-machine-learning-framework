# Keras GPU Installation on Windows

* [Install NVIDIA Driver](#user-content-install-nvidia-driver)
* [Install Anaconda](#user-content-install-anaconda) and update Anaconda
* [Install CUDA Toolkit 10.0](#user-content-install-cuda-toolkit-100)
* [Save cuDNN and add the path to environment](#save-cudnn-and-add-the-path-to-environment)
* [Create environment and activate it](user-content-create-environment-and-activate-it)
* [Test it!](user-content-test-it)

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

* Install for Windows Installer: Python 3.7 version
* [Download Anaconda](https://www.anaconda.com/distribution/)

Open Anaconda Prompt:

* [Win] + s
* Enter: anaconda
* Open: Anaconda Prompt (Anaconda3)

And type the following commands to update Anaconda and all other libraries:

```bash
user$ conda update conda
user$ conda update --all
```

## Install CUDA Toolkit 10.0

* [Download CUDA Toolkit 10.0](https://developer.nvidia.com/)
* Select Target Platform "Windows"
* Architecture: x86_64
* Version: 10
* exe (local)

## Save cuDNN and add the path to environment

* [Download cuDNN](https://developer.nvidia.com/rdp/cudnn-download)
* Extract the data at a location of your choice, eg. C:\cuda
* Add the path to environment path

## Create environment and activate it

...

## Test it!

...
