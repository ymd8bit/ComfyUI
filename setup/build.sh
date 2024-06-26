USER=ymd8bit
VERSION=$(date "+%Y%m%d")
CONTEXT=$(dirname $0)

docker build $CONTEXT -f Dockerfile -t "${USER}/comfyui:${VERSION}"
