import argparse
import os
import shutil
import subprocess
from urllib import parse
from typing import List, Optional
import csv

from huggingface_hub import login

from env import REPO_ROOT_DIR, CUSTOM_NODES_DIR, CUSTOM_NODES_LIST


parser = argparse.ArgumentParser(description="Script for preparing ComfyUI environment")
parser.add_argument('-m', '--src_models_dir', type=str, default="/share/stable-diffusion/models")
args = parser.parse_args()
args.src_models_dir = os.path.abspath(args.src_models_dir)
assert os.path.exists(args.src_models_dir), f"{args.src_models_dir} does not exist"


def run(cmd: List[str], cwd: str = "."):
    result = subprocess.run(cmd, shell=False,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            text=True,
                            cwd=cwd)
    print(result.stdout)
    print(result.stderr)


def get_custom_node(
    repo_url: str,
    commit_id: Optional[str] = None,
):
    url = parse.urlparse(repo_url)
    basename = os.path.basename(url.path).replace(".git", "")
    dst = os.path.join(CUSTOM_NODES_DIR, basename)

    if not os.path.exists(dst):
        run(["git", "clone", "--recursive", repo_url, dst])
        if commit_id is not None:
            run(["git", "fetch", "origin", commit_id], cwd=dst)
            run(["git", "reset", "--hard", commit_id], cwd=dst)
            run(["git", "submodule", "update", "--init", "--recursive"], cwd=dst)
    else:
        print(f"{dst} already exists, so skip...")


with open(CUSTOM_NODES_LIST, "r") as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        repo_url = row[0]
        commit_id = row[1]
        get_custom_node(repo_url, commit_id=commit_id)


def link_model(name: str, custom_dst: Optional[str] = None):
    src = f"{args.src_models_dir}/{name}"
    os.makedirs(src, exist_ok=True)
    DST_MODELS_DIR = os.path.join(REPO_ROOT_DIR, "models")

    if custom_dst is not None:
        dst = custom_dst
    else:
        dst = f"{DST_MODELS_DIR}/{name}"

    if os.path.exists(dst):
        if os.path.islink(dst):
            print(f"{dst} is a symbolic link, so relink")
            os.unlink(dst)
            os.symlink(src, dst)
        elif os.path.isdir(dst):
            print(f"{dst} is a directory, so remove and link ({src} -> {dst})")
            shutil.rmtree(dst)
            os.symlink(src, dst)
        else:
            print(f"{src} is not a directory nor symbolic link or directory, so skip...")
    else:
        if os.path.islink(dst):
            print(f"{dst} is an invalid symbolic link, so relink")
            os.unlink(dst)
        os.symlink(src, dst)


link_model("checkpoints")
link_model("clip")
link_model("clip_vision")
link_model("configs")
link_model("controlnet")
link_model("diffusers")
link_model("embeddings")
link_model("gligen")
link_model("hypernetworks")
link_model("loras")
link_model("style_models")
link_model("unet")
link_model("upscale_models")
link_model("vae")
link_model("vae_approx")
link_model("ultralytics")
link_model("onnx")
link_model("sams")
link_model("mmdets")
link_model("facedetection")
link_model("facerestore_models")
link_model("reactor")
link_model("insightface")
link_model("animatediff/models", "custom_nodes/ComfyUI-AnimateDiff-Evolved/models")
link_model("moondream", "custom_nodes/comfyui-moondream/checkpoints")


# login to Huggingface to download models
run(["git", "config", "--global", "credential.helper", "store"])
login()

# for comfyui-moondream
# comfyui_moondream_dir = os.path.join(CUSTOM_NODES_DIR, "comfyui-moondream")
# comfyui_moondream_ckpt_dir = os.path.join(comfyui_moondream_dir, "checkpoints")
# if not os.path.exists(comfyui_moondream_ckpt_dir):
    # run(["python", "download_models.py"], cwd=comfyui_moondream_dir)