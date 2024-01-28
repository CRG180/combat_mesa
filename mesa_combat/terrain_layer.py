from mesa import Agent
import numpy as np
#import rasterio
#from rasterio.plot import show
#from rasterio.merge import merge
#import os
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist

def extract_elevation_data(image_path, elevation_lookup):
    # Open the PNG image
    image = Image.open(image_path)

    # Convert the image to a NumPy array
    image_array = np.array(image)

    # Extract RGB values for each pixel
    pixel_rgb_values = image_array[:, :, :3].reshape(-1, 3)

    # Create an array to store the elevation data
    elevation_data = np.zeros(pixel_rgb_values.shape[0])

    # Find the closest RGB combination using cdist
    closest_rgb_indices = np.argmin(cdist(pixel_rgb_values, list(elevation_lookup.keys())), axis=1)
    
    # Assign elevation values based on the closest RGB combination
    elevation_data = np.array([elevation_lookup[list(elevation_lookup.keys())[idx]] for idx in closest_rgb_indices])

    # Reshape the elevation data to match the original image shape
    elevation_data = elevation_data.reshape(image_array.shape[0], image_array.shape[1])

    return elevation_data


def plot_elevation_data(elevation_data):
    plt.imshow(elevation_data, cmap='viridis', origin='lower', interpolation='nearest')
    plt.colorbar(label='Elevation (meters)')
    plt.title('Elevation Map')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.show()

def plot_3d_elevation_data(elevation_data):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    x_size, y_size = elevation_data.shape
    x = np.arange(x_size)
    y = np.arange(y_size)
    x, y = np.meshgrid(x, y)

    ax.plot_surface(x, y, elevation_data, cmap='viridis')
    
    # Set the same scale for all axes
    ax.set_box_aspect([np.ptp(coord) for coord in [x, y, elevation_data]])

    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_zlabel('Elevation (meters)')
    ax.set_title('3D Elevation Map')

    plt.show()

class TerrainMap:
    
    def __init__(self) -> None:
        pass
    
    def line_of_sight(self,source:Agent,other:Agent) -> bool:
        return True
    

if __name__ == '__main__':
        
        
    # Example usage
    image_path = './mesa_combat/data/terrain/gray_scale_terrain.PNG'

    # Define your elevation lookup table
    # Format: {(R, G, B): Elevation, ...}
    elevation_lookup = {
        (0, 0, 0): 140,   # Example: black corresponds to elevation 600 meters
        (50, 50, 50): 125,   
        (80, 80, 80): 75,
        (110, 110, 110): 50,
        (169, 169, 169): 25,
        (235, 235, 235): 10,
        (255, 255, 255): 0 
    }

    elevation_data = extract_elevation_data(image_path, elevation_lookup)

    # Print the elevation data for a sample pixel
    sample_pixel = elevation_data[216, 738] #y,x
    print(f'Elevation for sample pixel: {sample_pixel} meters')
    
    #plot_elevation_data(elevation_data)
    plot_3d_elevation_data(elevation_data)
    
    # directory_path = './data/terrain/'
    # all_files = os.listdir(directory_path)
    # # Filter the list to include only TIFF files
    # tiff_files = [file for file in all_files if file.lower().endswith('.tif') or file.lower().endswith('.tiff')]
    # # Initialize an empty list to store the data arrays
    # data_list = []
    # # Open each TIFF file and append the data array to the list
    # for tiff_file in tiff_files:
    #     tiff_path = os.path.join(directory_path, tiff_file)
    #     src = rasterio.open(tiff_path)
    #     data_list.append(src)
        
    # mosaic, out_transform = merge(data_list)
    # # Make sure to close the datasets after merging,
    # # context manager did not provide the flexbility
    
    
    # for src in data_list:
    #     src.close()
            
    # # Stack the data arrays along a new dimension (axis 0)
    # #stacked_data = np.stack(data_list, axis=0)

    # print(mosaic)