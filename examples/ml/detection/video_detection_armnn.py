# Copyright 2021 Variscite LTD
# SPDX-License-Identifier: BSD-3-Clause

from pyvar.ml.engines.armnn import ArmNNInterpreter
from pyvar.ml.utils.framerate import Framerate
from pyvar.ml.utils.label import Label
from pyvar.ml.utils.overlay import Overlay
from pyvar.ml.utils.retriever import FTP
from pyvar.ml.utils.resizer import Resizer
from pyvar.multimedia.helper import Multimedia

ftp = FTP()

if ftp.retrieve_package(category="detection"):
    model_file_path = ftp.model
    label_file_path = ftp.label
    video_file_path = ftp.video

labels = Label(label_file_path)
labels.read_labels("detection")

engine = ArmNNInterpreter(model_file_path, accelerated=True, category="detection")

resizer = Resizer()

video = Multimedia(video_file_path)
video.set_v4l2_config()

draw = Overlay()

while video.loop:
    frame = video.get_frame()
    resizer.resize_frame(frame, engine.input_width, engine.input_height)

    engine.set_input(resizer.frame_resized)
    engine.run_inference()
    engine.get_result("detection")

    output_frame = draw.info(category="detection",
                             image=resizer.frame,
                             top_result=engine.result,
                             labels=labels.list,
                             inference_time=engine.inference_time,
                             model_name=model_file_path,
                             source_file=video.video_src)

    video.show("ArmNN: Video Detection", output_frame)

video.destroy()
