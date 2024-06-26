import os

REPO_ROOT_DIR = os.path.abspath(os.path.join(__file__, "..", ".."))
SETUP_DIR = os.path.join(REPO_ROOT_DIR, "setup")
CUSTOM_NODES_DIR = os.path.join(REPO_ROOT_DIR, "custom_nodes")
CUSTOM_NODES_LIST = os.path.join(SETUP_DIR, "custom_nodes_list.csv")
