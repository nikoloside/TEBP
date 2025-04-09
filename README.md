# DeepFracture & The Eye of Breaking Perception 【WIP】

## Overview

This project serves as the code base for the DeepFracture and The Eye of Breaking Perception paper. It encompasses various components essential for generating, processing, and training models on fracture simulations. The following sections outline the key components of the code base.

### Components

1. **Data Generation**
   - This module is responsible for downloading and preparing the necessary 3D object files (OBJ) for the simulation. It includes scripts for normalizing and converting OBJ files into formats suitable for the fracture simulation.

2. **Running FractureRB**
   - The FractureRB component is designed to simulate the behavior of fractured materials. This module allows users to run simulations using the Bullet Physics engine, providing insights into the dynamics of fractured objects.

3. **Cook Data**
   - This component processes the generated data, preparing it for training. It includes data cleaning, normalization, and formatting to ensure compatibility with the training algorithms.

4. **Training**
   - The training module implements machine learning algorithms to train models on the processed fracture data. It includes scripts for model selection, hyperparameter tuning, and evaluation metrics.

5. **Run-time**
   - This section encompasses various runtime environments for executing the simulations:
   - **Havok Version**: A runtime environment utilizing the Havok Physics engine for high-performance simulations.
   - **PyBullet Version**: A version that leverages the PyBullet physics engine, providing a flexible and easy-to-use interface for running simulations.
   - **Morpho Seg**: This component focuses on segmenting the mesh data based on morphological features, enhancing the simulation's realism.
   - **Mesh Boolean**: This module allows for complex boolean operations on meshes, enabling the creation of intricate fracture patterns.

## Usage Instructions

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd DeepFracture
   ```

2. **Install Dependencies**
   Ensure you have all the required dependencies installed. You can use the following command:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run Data Generation**
   Execute the data generation scripts to prepare your dataset:
   ```bash
   python data_generation.py
   ```

4. **Run Fracture Simulation**
   To run the fracture simulation, use:
   ```bash
   python run_fracture.py
   ```

5. **Train the Model**
   Start the training process with:
   ```bash
   python train_model.py
   ```

6. **Run the Simulation**
   Finally, execute the simulation in your desired runtime environment:
   ```bash
   python run_time.py --engine <Havok|PyBullet>
   ```

By following these instructions, you can effectively utilize the DeepFracture code base to explore and analyze fracture simulations.
