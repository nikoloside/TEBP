#!/bin/bash

INSTANCE_NAME=$(hostname)  # e.g. spc01
FILE_ID="1v5KaftqH6wlJb8gomMoYra_-L222Fcqw"
FILE_NAME=/home/azureuser/.config/rclone/rclone.conf

echo "[*] Detected instance: $INSTANCE_NAME"

# Download rclone.conf
mkdir -p /home/azureuser/.config/rclone
wget --no-check-certificate "https://docs.google.com/uc?export=download&id=${FILE_ID}" -O ${FILE_NAME}

# git clone github
if [ ! -d fracture-docker ]; then
  git clone https://github.com/nikoloside/fracturerb-docker.git
fi

cd fracturerb-docker

# 生成并覆盖 config.json
cat <<EOF > config.json
{
  "gdrive_name": "fracture-gdrive",
  "gdrive_bullet_path": "BulletData",
  "gdrive_result_path": "SharedResults/${INSTANCE_NAME}",
  "local_bullet_path": "/mnt/bullet",
  "local_result_path": "/mnt/results"
}
EOF

echo "[*] Generated config.json with result path: SharedResults/${INSTANCE_NAME}"

# start auto setup & exec fracture program
chmod +x start.sh
./start.sh
