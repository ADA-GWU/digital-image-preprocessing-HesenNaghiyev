import pydicom
import os
import imageio.v2
import matplotlib.pyplot as plt
import io

# Define the path to the sample MRI images
mri_dir = '00163'

# Define the output directory if it doesn't exist
output_dir = 'task3'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Loop over the subdirectories in the MRI directory
for subdir in sorted(os.listdir(mri_dir)):
    # Create a new output subdirectory
    subdir_path = os.path.join(output_dir, subdir)
    if not os.path.exists(subdir_path):
        os.makedirs(subdir_path)

    # Loop over the files in the subdirectory
    filenames = sorted(os.listdir(os.path.join(mri_dir, subdir)))
    images = []
    for filename in filenames:
        # Load the MRI image
        mri_path = os.path.join(mri_dir, subdir, filename)
        mri = pydicom.dcmread(mri_path)

        # Print the metadata
        with open(os.path.join(subdir_path, 'metadata.txt'), 'w') as f:
            for elem in mri:
                f.write(str(elem) + '\n')

        # Visualize the different layers of the MRI image
        mri_arr = mri.pixel_array

        # Visualize the raw pixel values
        plt.imshow(mri_arr, cmap='gray')
        plt.axis('off')
        plt.title(filename)
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight')
        buffer.seek(0)
        image = imageio.v2.imread(buffer)
        images.append(image)
        plt.close()

    # Save the animated GIF
    gif_path = os.path.join(subdir_path, 'animation.gif')
    imageio.mimsave(gif_path, images, fps=10)
