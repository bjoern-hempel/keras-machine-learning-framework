# Keras GPU Installation on Windows

* [Install NVIDIA Driver](#user-content-install-nvidia-driver)
* [Install Anaconda](#user-content-install-anaconda) and update Anaconda
* [Install CUDA Toolkit 10.0](#user-content-install-cuda-toolkit-100)
* Save cuDNN and add the path to environment
* Create environment and activate it
* Test it!

## Install NVIDIA Driver

* [Download NVIDIA Driver](https://www.nvidia.com/Download/index.aspx?lang=en-us)

## Install Anaconda

* Install for Windows Installer: Python 3.7 version
* [Download Anaconda](https://www.anaconda.com/distribution/)

Open Anaconda Prompt:

* [Win] + s
* Enter: Anaconda

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

https://developer.nvidia.com/rdp/cudnn-download
