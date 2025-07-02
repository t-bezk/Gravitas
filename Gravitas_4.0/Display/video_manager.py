"""""""""""""""""""""""""""""""""
----------------------------------
GRAVITAS v.4.0.1 - video manager module
by Tomas Bezkorowajnyj c. February 2025
----------------------------------
"""""""""""""""""""""""""""""""""

import shutil
import os
import cv2


def delete_contents(folder_path):
    """Delete all files within folder_path"""
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)  # Remove the file or symbolic link
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)  # Remove the directory and all its contents
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')


def images_to_video(image_folder, output_video, frame_rate):
    """Create video file from series of images within buffer folder"""

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


def video_manager(image_folder_p, output_video_p, frame_rate_p):
    """Parent function carries out entire video-processing system"""

    ## Run file conversion funciton
    images_to_video(image_folder_p, output_video_p, frame_rate_p)


    ## Finally, delete all residual files from buffer folder
    delete_contents(image_folder_p)



if __name__ == "__main__":
    print("video_manager.py successfully loaded")