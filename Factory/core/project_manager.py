import json
import os
from core.generator import generate_app


def build_project():

    project_path = "projects/demo"

    with open(os.path.join(project_path, "project.json")) as f:
        data = json.load(f)

    generate_app(data)