# Setup

## How to update the custom node list
```sh
git config --global --add safe.directory '*'
python update_custom_node_list.sh
git config --global --unset-all safe.directory
```