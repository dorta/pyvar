#!/usr/bin/env python3
# Copyright 2021 Variscite LTD
# SPDX-License-Identifier: BSD-3-Clause

from pyvarml.dataset.mnist import train_mnist_fashion

trained_model = train_mnist_fashion()

with open('mnist_fashion.tflite', "wb") as model_file:
    model_file.write(trained_model[0])
    model_file.close()

print(f"Test loss: {trained_model[1]}")
print(f"Test accuracy: {trained_model[2]}")