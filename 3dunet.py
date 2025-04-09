import torch
import torch.nn as nn
import torch.nn.functional as F
import nibabel as nib
import pandas as pd
import numpy as np
from torch.utils.data import Dataset, DataLoader
import os

class ResBlock(nn.Module):
    def __init__(self, in_channels, out_channels):
        super(ResBlock, self).__init__()
        self.conv1 = nn.Conv3d(in_channels, out_channels, kernel_size=3, padding=1)
        self.bn1 = nn.BatchNorm3d(out_channels)
        self.conv2 = nn.Conv3d(out_channels, out_channels, kernel_size=3, padding=1)
        self.bn2 = nn.BatchNorm3d(out_channels)
        
        self.shortcut = nn.Sequential()
        if in_channels != out_channels:
            self.shortcut = nn.Sequential(
                nn.Conv3d(in_channels, out_channels, kernel_size=1),
                nn.BatchNorm3d(out_channels)
            )
    
    def forward(self, x):
        residual = x
        x = F.relu(self.bn1(self.conv1(x)))
        x = self.bn2(self.conv2(x))
        x += self.shortcut(residual)
        x = F.relu(x)
        return x

class UNet3D(nn.Module):
    def __init__(self, in_channels=1, out_channels=1, init_features=32):
        super(UNet3D, self).__init__()
        
        # Encoder
        self.encoder1 = ResBlock(in_channels, init_features)
        self.pool1 = nn.MaxPool3d(kernel_size=2, stride=2)
        
        self.encoder2 = ResBlock(init_features, init_features*2)
        self.pool2 = nn.MaxPool3d(kernel_size=2, stride=2)
        
        self.encoder3 = ResBlock(init_features*2, init_features*4)
        self.pool3 = nn.MaxPool3d(kernel_size=2, stride=2)
        
        self.encoder4 = ResBlock(init_features*4, init_features*8)
        self.pool4 = nn.MaxPool3d(kernel_size=2, stride=2)
        
        # Bottleneck
        self.bottleneck = ResBlock(init_features*8, init_features*16)
        
        # Decoder
        self.upconv4 = nn.ConvTranspose3d(init_features*16, init_features*8, kernel_size=2, stride=2)
        self.decoder4 = ResBlock(init_features*16, init_features*8)
        
        self.upconv3 = nn.ConvTranspose3d(init_features*8, init_features*4, kernel_size=2, stride=2)
        self.decoder3 = ResBlock(init_features*8, init_features*4)
        
        self.upconv2 = nn.ConvTranspose3d(init_features*4, init_features*2, kernel_size=2, stride=2)
        self.decoder2 = ResBlock(init_features*4, init_features*2)
        
        self.upconv1 = nn.ConvTranspose3d(init_features*2, init_features, kernel_size=2, stride=2)
        self.decoder1 = ResBlock(init_features*2, init_features)
        
        self.conv = nn.Conv3d(init_features, out_channels, kernel_size=1)
        
    def forward(self, x):
        # Encoding
        enc1 = self.encoder1(x)
        enc2 = self.encoder2(self.pool1(enc1))
        enc3 = self.encoder3(self.pool2(enc2))
        enc4 = self.encoder4(self.pool3(enc3))
        
        # Bottleneck
        bottleneck = self.bottleneck(self.pool4(enc4))
        
        # Decoding
        dec4 = self.upconv4(bottleneck)
        dec4 = torch.cat((dec4, enc4), dim=1)
        dec4 = self.decoder4(dec4)
        
        dec3 = self.upconv3(dec4)
        dec3 = torch.cat((dec3, enc3), dim=1)
        dec3 = self.decoder3(dec3)
        
        dec2 = self.upconv2(dec3)
        dec2 = torch.cat((dec2, enc2), dim=1)
        dec2 = self.decoder2(dec2)
        
        dec1 = self.upconv1(dec2)
        dec1 = torch.cat((dec1, enc1), dim=1)
        dec1 = self.decoder1(dec1)
        
        return self.conv(dec1)

class VoxelDataset(Dataset):
    def __init__(self, csv_dir, nii_dir):
        self.csv_files = sorted([os.path.join(csv_dir, f) for f in os.listdir(csv_dir) if f.endswith('.csv')])
        self.nii_files = sorted([os.path.join(nii_dir, f) for f in os.listdir(nii_dir) if f.endswith('.nii')])
        
    def __len__(self):
        return len(self.csv_files)
    
    def __getitem__(self, idx):
        # Load CSV data
        csv_data = pd.read_csv(self.csv_files[idx]).values
        # Reshape to 128x128x128
        input_data = csv_data.reshape(128, 128, 128)
        
        # Load NII data
        nii_img = nib.load(self.nii_files[idx])
        target_data = nii_img.get_fdata()
        
        # Convert to tensors
        input_tensor = torch.FloatTensor(input_data).unsqueeze(0)  # Add channel dimension
        target_tensor = torch.FloatTensor(target_data).unsqueeze(0)  # Add channel dimension
        
        return input_tensor, target_tensor

def get_data_loaders(csv_dir='dataset/impact', nii_dir='dataset/nii', batch_size=4):
    dataset = VoxelDataset(csv_dir, nii_dir)
    train_size = int(0.8 * len(dataset))
    val_size = len(dataset) - train_size
    train_dataset, val_dataset = torch.utils.data.random_split(dataset, [train_size, val_size])
    
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)
    
    return train_loader, val_loader


