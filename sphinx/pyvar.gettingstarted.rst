Getting Started
===============

Introduction
------------

Before getting started with pyvar package and learning more about its core and
examples, it is important to mention that one of the main focus of this package
is to allow the users to explore multiple ML applications use cases by using
displays, cameras devices, and user interfaces capabilities. We also must
briefly talk about a couple of things such as the AI hardware accelerator,
model training, and model quantization even though those are long subjects.

Software
--------

Setting Up the BSP
~~~~~~~~~~~~~~~~~~

#. Build the latest `Yocto Release`_, make sure to add the following lines at your **local.conf** file:

    .. code-block:: bash

        IMAGE_INSTALL_append = " \
            python3-pip \
        "

.. _Yocto Release: https://variwiki.com/

1. Flash the built image into the SD Card, boot the board, then go to next section.

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
        >>> import pyvar
        >>>
