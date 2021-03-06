Machine Learning API: Getting Started
=====================================

Introduction
------------

Before getting started with pyvar package and learning more about its core and
examples, it is important to mention that one of the main focus of this package
is to allow the users to explore multiple ML applications use cases by using
displays, cameras devices, and user interfaces capabilities. We also must
briefly talk about a couple of things such as the AI hardware accelerator,
model training, and model quantization even though those are long subjects.

The comprehension of the above topics might help you to understand how does ML work on
embedded systems, and it will probably allow you to get the best possible
inference performance on your ML applications.

Hardware
--------

Recommended System on Modules (SoMs)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To achieve the best possible performance on the ML applications, it is
recommended to use the System on Modules powered by the i.MX8M Plus processor
from NXP. Check the SoMs below:

+-----------------------+-----------------------+
| `VAR-SOM-MX8M-PLUS`_  | `DART-MX8M-PLUS`_     |
+=======================+=======================+
| |var-mplus|           | |dart-mplus|          |
+-----------------------+-----------------------+

.. _VAR-SOM-MX8M-PLUS: https://www.variscite.com/product/system-on-module-som/cortex-a53-krait/var-som-mx8m-plus-nxp-i-mx-8m-plus/

.. |var-mplus| image:: images/var-som-mx8m-plus.png
   :width: 65%

.. _DART-MX8M-PLUS: https://www.variscite.com/product/system-on-module-som/cortex-a53-krait/dart-mx8m-plus-nxp-i-mx-8m-plus/

.. |dart-mplus| image:: images/dart-mx8m-plus.png
   :width: 60%

Neural Processing Unit (NPU) Overview
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The above SoMs have a dedicated unit to deal with ML inference process called
Neural Processing Unit provided by Verisilicon. This compute engine delivers up
to **2.3** Tera Operations Per Second (*TOPS*) and handles 8-bit fixed-point
operations models, allowing the user to achieve the highest performance during
the inference process.

The pyvar package is not tied to the NPU only, you can use any other SoM from
the i.MX8 family with the ML API, what changes is that the inference process
runs on the GPU/CPU instead of the NPU, and this may probably result on a higher
inference time due more complex calculations.

The NPU itself handles 8-bit fixed-point operations, which results in the ability
to have a ML model with a much simpler and smaller arithmetic units avoiding
larger floating points calculations. To utilize the computation capabilities by
achieving the best possible inference performance of this unit, the model must
be converted from a 32-bit floating-point network into an 8-bit fixed point network.

This conversion is known as quantization, and there are two possible ways to
quantize a model to properly work on the NPU. The first one is to train your own
model by applying the quantization-aware training (QAT) method during training,
and the simpler one is to use a post-training method that only converts a
trained model to the format NPU requires. Check out our `var-demos`_ repository
for more source code samples, and simple post-training example.

.. _var-demos: https://github.com/varigit/var-demos/tree/master/machine-learning-demos

* For more information about the NPU, please check this `page`_.

.. _page: https://www.nxp.com/products/processors-and-microcontrollers/arm-processors/i-mx-applications-processors/i-mx-8-processors/i-mx-8m-plus-arm-cortex-a53-machine-learning-vision-multimedia-and-industrial-iot:IMX8MPLUS


Software
--------

Setting Up the BSP
~~~~~~~~~~~~~~~~~~

#. Build the latest `Yocto Release`_ with **Wayland** + **X11** features using **fsl-image-qt5** image;

    **NOTE**: To use the **fsl-image-gui** image, make sure to add the following lines at your **local.conf** file:

    .. code-block:: bash

        OPENCV_PKGS_imxgpu = " \
           opencv-apps \
           opencv-samples \
           python3-opencv \
        "

        IMAGE_INSTALL_append_mx8mp = " \
            packagegroup-imx-ml \
            ${OPENCV_PKGS} \
        "

.. _Yocto Release: https://variwiki.com/

2. Flash the built image into the SD Card, boot the board, then go to next section.


Python API Package Installation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. To install the pyvar API Python package use the pip3 tool to retrieve via Pypi:

    .. code-block:: console

        root@imx8mp-var-dart:~# pip3 install pyvar

2. To make sure that pyvar is installed, run the following command to check:

    .. code-block:: console

        root@imx8mp-var-dart:~# python3
        Python 3.9.5 (default, May  3 2021, 15:11:33)
        [GCC 10.2.0] on linux
        Type "help", "copyright", "credits" or "license" for more information.
        >>> from pyvar import ml
        >>>
