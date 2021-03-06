# Copyright 2021 Variscite LTD
# SPDX-License-Identifier: BSD-3-Clause

from argparse import ArgumentParser

from pyvar.ml.engines.tflite import TFLiteInterpreter
from pyvar.ml.utils.framerate import Framerate
from pyvar.ml.utils.label import Label
from pyvar.ml.utils.overlay import Overlay
from pyvar.ml.utils.resizer import Resizer
from pyvar.ml.utils.retriever import FTP
from pyvar.multimedia.helper import Multimedia

ftp = FTP()
parser = ArgumentParser()
parser.add_argument('--num_threads', type=int)
args = parser.parse_args()

if ftp.retrieve_package(category="classification"):
    model_file_path = ftp.model
    label_file_path = ftp.label

labels = Label(label_file_path)
labels.read_labels("classification")

engine = TFLiteInterpreter(model_file_path=model_file_path,
                           num_threads=args.num_threads)

resizer = Resizer()
resizer.set_sizes(engine_input_details=engine.input_details)

camera = Multimedia("/dev/video1", resolution="vga")
camera.set_v4l2_config()

framerate = Framerate()

draw = Overlay()
draw.framerate_info = True

while camera.loop:
    with framerate.fpsit():
        frame = camera.get_frame()
        resizer.resize_frame(frame)

        engine.set_input(resizer.frame_resized)
        engine.run_inference()
        engine.get_result("classification")

        output_frame = draw.info(category="classification",
                                 image=resizer.frame,
                                 top_result=engine.result,
                                 labels=labels.list,
                                 inference_time=engine.inference_time,
                                 model_name=model_file_path,
                                 source_file=camera.dev.name,
                                 fps=framerate.fps)

        camera.show("TFLite: Real Time Classification", output_frame)

camera.destroy()
