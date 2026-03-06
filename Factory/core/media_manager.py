import os
import shutil


def collect_media(project_data, project_path, output_path):

    media_output = os.path.join(output_path, "media")

    os.makedirs(media_output, exist_ok=True)

    for page in project_data["pages"]:

        for block in page["blocks"]:

            if block["type"] in ["image", "video", "audio"]:

                src = os.path.join(project_path, block["src"])

                if os.path.exists(src):

                    dst = os.path.join(media_output, os.path.basename(src))

                    shutil.copy(src, dst)