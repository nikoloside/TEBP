#!/bin/bash

CONFIG="config.yaml"

# 检查是否安装 yq（YAML 解析工具）
if ! command -v yq &> /dev/null; then
  echo "Install yq：brew install yq"
  exit 1
fi

# 读取 VM 名列表并创建
for VM_NAME in $(yq '.vms[]' $CONFIG); do
  echo "🚀 创建 VM: $VM_NAME"
  ./createVM.sh $VM_NAME
done
