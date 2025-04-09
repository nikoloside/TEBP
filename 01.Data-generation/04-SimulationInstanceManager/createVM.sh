#!/bin/bash

# 参数：VM 名称（例如 spc01）
VM_NAME=$1
RESOURCE_GROUP="fracture-group"
LOCATION="eastus"
IMAGE="Ubuntu2404"
SIZE="Standard_D4s_v3"
ADMIN_USER="azureuser"
SSH_KEY_PATH="$HOME/.ssh/id_ed25519.pub"

if ! command -v yq &> /dev/null; then
  echo "Please install yq：brew install yq"
  exit 1
fi
RESOURCE_GROUP=$(yq '.resourceGroup' config.yaml)
LOCATION=$(yq '.location' config.yaml)

# Google Drive 上的 download.sh 的 file ID
DOWNLOAD_ID="1mqwgEX_ZgOifRBLFllqw6cGFRXwUhwk8"

# 生成 cloud-init 临时配置（自动下载并执行 download.sh）
cat > cloud-init-${VM_NAME}.yaml <<EOF
#cloud-config
runcmd:
  - cd /home/azureuser/
  - wget --no-check-certificate "https://docs.google.com/uc?export=download&id=${DOWNLOAD_ID}" -O /home/azureuser/download.tar.gz
  - tar -xzvf /home/azureuser/download.tar.gz -C /home/azureuser/
  - sudo chmod +x /home/azureuser/download.sh
  - sudo /home/azureuser/download.sh
EOF

# 创建资源组（如果尚未存在）
RG_EXISTS=$(az group exists --name $RESOURCE_GROUP)

if [ "$RG_EXISTS" != "true" ]; then
  echo "🔧 Create resource group：$RESOURCE_GROUP"
  az group create --name $RESOURCE_GROUP --location $LOCATION
else
  echo "✅ Resource group exist：$RESOURCE_GROUP"
fi

# 创建 VM
az vm create \
  --resource-group $RESOURCE_GROUP \
  --name $VM_NAME \
  --image $IMAGE \
  --size $SIZE \
  --admin-username $ADMIN_USER \
  --ssh-key-value "$SSH_KEY_PATH" \
  --custom-data cloud-init-${VM_NAME}.yaml \
  --public-ip-sku Standard \
  --output table
