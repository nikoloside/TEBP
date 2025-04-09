#!/bin/bash

INSTANCE_NAME=$(hostname)  # e.g. spc01

echo "[*] Detected instance: $INSTANCE_NAME"

# Download rclone.conf
mkdir -p ~/.config/rclone
curl -L https://drive.google.com/uc?export=download&id=1v5KaftqH6wlJb8gomMoYra_-L222Fcqw \
  -o ~/.config/rclone/rclone.conf

# git clone github
if [ ! -d fracture-project ]; then
  git clone https://github.com/nikoloside/fracturerb-docker.git
fi

cd fracture-project

# 生成并覆盖 config.json
cat <<EOF > config.json
{
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
