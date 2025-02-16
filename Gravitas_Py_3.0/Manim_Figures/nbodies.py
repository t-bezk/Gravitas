import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os

import pathlib

# Constants
G = 1  # Gravitational constant (arbitrary units)
N = 20  # Number of bodies
DT = 0.05  # Time step
STEPS = 1000  # Number of time steps

# Create output directory

dir = pathlib.Path(__file__).parent.resolve()

output_dir = "n_body_frames"
os.makedirs(output_dir, exist_ok=True)

# Initialize positions and velocities randomly
np.random.seed(42)  # For reproducibility
positions = np.random.rand(N, 3) * 10 - 5  # Random positions in a 10x10x10 cube
velocities = np.random.rand(N, 3) - 0.5  # Random initial velocity vectors
masses = np.ones(N)*0.5  # Equal masses

#masses[0] = 3

#positions[0] = [0, 0, 0]
#velocities[0] = [0, 0, 0]


def compute_accelerations(positions, masses):
    """Compute gravitational accelerations for all particles."""
    accelerations = np.zeros_like(positions)
    for i in range(N):
        for j in range(N):
            if i != j:
                r_vec = positions[j] - positions[i]
                r_mag = np.linalg.norm(r_vec) + 1e-5  # Avoid singularity
                accelerations[i] += G * masses[j] * r_vec / r_mag**3
    return accelerations

# Initialize accelerations
accelerations = compute_accelerations(positions, masses)

# Simulation loop
for step in range(STEPS):
    # Velocity Verlet integration
    positions += velocities * DT + 0.5 * accelerations * DT**2
    new_accelerations = compute_accelerations(positions, masses)
    velocities += 0.5 * (accelerations + new_accelerations) * DT
    accelerations = new_accelerations

    # Plot current positions
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(positions[:, 0], positions[:, 1], positions[:, 2], c='b', marker='o')
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.set_zlim(-10, 10)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(f'Step {step}')
    ax.set_facecolor("black")
    plt.savefig(f"{dir}/fig/im_d10{100000+step}.png", dpi=200)
    plt.close(fig)

print(f"Simulation complete. Frames saved in {output_dir}/")

#video_manager.py


import shutil
import os
import cv2

"""Delete all files within folder_path"""
def delete_contents(folder_path):

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)  # Remove the file or symbolic link
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)  # Remove the directory and all its contents
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')


"""Create video file from series of images within buffer folder"""
def images_to_video(image_folder, output_video, frame_rate):

    images = ([img for img in os.listdir(image_folder) if img.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff'))])
    
    if not images:
        print("No images found in the folder.")
        return
    
    first_image_path = os.path.join(image_folder, images[0])
    frame = cv2.imread(first_image_path)
    height, width, layers = frame.shape
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(output_video, fourcc, frame_rate, (width, height))
    
    for image in images:
        img_path = os.path.join(image_folder, image)
        frame = cv2.imread(img_path)
        video.write(frame)
    
    video.release()
    print(f"Video saved at {output_video}")


"""Parent function carries out entire video-processing system"""
def video_manager(image_folder_p, output_video_p, frame_rate_p):


    ## Run file conversion funciton
    images_to_video(image_folder_p, output_video_p, frame_rate_p)


    ## Finally, delete all residual files from buffer folder
    delete_contents(image_folder_p)



if __name__ == "__main__":
    
    print("video_manager.py successfully loaded")

video_manager(f'{dir}/fig/', f'{dir}/out/vid.mp4', 60)