# Copyright 2021 Variscite LTD
# SPDX-License-Identifier: BSD-3-Clause

"""
:platform: Unix/Yocto
:synopsis: Class to retrieve packages from Variscite HTTPS server.

.. moduleauthor:: Bruno Bonaldi Teixeira <bruno.t@variscite.com>
"""

import glob
import logging
import os
import shutil
import socket
import requests

from pyvar.config import CACHEDIR
from pyvar.ml.config import CLASSIFICATION
from pyvar.ml.config import CLASSIFICATION_93
from pyvar.ml.config import DETECTION
from pyvar.ml.config import SEGMENTATION
from pyvar.ml.utils.config import DEFAULT_PACKAGES
from pyvar.ml.utils.config import HTTPS_HOST
from pyvar.ml.utils.config import JPG, MP4, PNG, TFLITE, TXT, ZIP


class HTTPS:
    """
    **This class can be used as reference only. It is not for production-ready.**
    """
    def __init__(self, host=None, user=None, passwd=None):
        """
        Constructor method for the HTTPS class.
        """
        self.host = HTTPS_HOST if host is None else host
        self.cachedir = CACHEDIR
        self.retrieved_package = None
        self.model = None
        self.label = None
        self.image = None
        self.video = None
        os.makedirs(self.cachedir, exist_ok=True)
        self.logger = logging.getLogger(__name__)

    def retrieve_package(self, package_dir=None,
                         package_filename=None,
                         category=None):
        """
        Retrieve package from the HTTPS server.
        
        Args:
            package_dir (str): package directory;
            package_filename (str): model package file name;
            category (str): model category (classification or detection).
        
        Returns:
            True if the package file was downloaded successfully. False if not.
        """
        host_name = socket.gethostname()
        host_93 = False
        if host_name.startswith("imx93"):
            host_93 = True

        if category is not None:
            if category == CLASSIFICATION:
                package_dir = DEFAULT_PACKAGES[CLASSIFICATION][0]
                package_filename = DEFAULT_PACKAGES[CLASSIFICATION][1]
                if host_93 is True:
                    package_filename = DEFAULT_PACKAGES[CLASSIFICATION_93][1]
            elif category == DETECTION:
                package_dir = DEFAULT_PACKAGES[DETECTION][0]
                package_filename = DEFAULT_PACKAGES[DETECTION][1]
            elif category == SEGMENTATION:
                package_dir = DEFAULT_PACKAGES[SEGMENTATION][0]
                package_filename = DEFAULT_PACKAGES[SEGMENTATION][1]
            else:
                raise ValueError("Unsupported model category: {}".format(category))
        
        if not package_dir or not package_filename:
            raise ValueError("package_dir and package_filename are required")

        package_url = f"{self.host}/{package_dir}/{package_filename}"
        package_file = os.path.join(self.cachedir, package_filename)
        partial_file = package_file + ".part"

        try:
            response = requests.get(package_url, timeout=30, stream=True)
            response.raise_for_status()
            with open(partial_file, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            os.replace(partial_file, package_file)
            self.retrieved_package = package_file
        except (requests.RequestException, OSError) as ex:
            self.logger.error("Could not retrieve %s: %s", package_url, ex)
            if os.path.exists(partial_file):
                os.remove(partial_file)
            return False

        if self.retrieved_package.endswith(ZIP):
            package_name_path = self.retrieved_package[:-4]
            try:
                shutil.unpack_archive(self.retrieved_package, self.cachedir)
                self._get_package_names(package_name_path, category)
                os.remove(self.retrieved_package)
            except Exception as ex:
                print(f"Exc: {ex}")
                return False

        return True

    def _get_package_names(self, package_name_path, category):
        """
        Get the model and label names from the downloaded package.        
        """
        model_list = glob.glob(os.path.join(package_name_path, TFLITE))
        self.model = model_list[0]
        label_list = glob.glob(os.path.join(package_name_path, TXT))
        self.label = label_list[0]
        if category == CLASSIFICATION:
            image_list = glob.glob(os.path.join(package_name_path, JPG))
            self.image = image_list[0]
        if category == DETECTION:
            image_list = glob.glob(os.path.join(package_name_path, PNG))
            self.image = image_list[0]
        video_list = glob.glob(os.path.join(package_name_path, MP4))
        self.video = video_list[0]
