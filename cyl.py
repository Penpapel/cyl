import streamlit as st
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
import random

# Function to draw a cylinder
def draw_cylinder(ax, radius, height, color):
    z = np.linspace(0, height, 50)
    theta = np.linspace(0, 2 * np.pi, 50)
    theta_grid, z_grid = np.meshgrid(theta, z)
    x_grid = radius * np.cos(theta_grid)
    y_grid = radius * np.sin(theta_grid)

    # Create surface plot for the cylinder
    ax.plot_surface(x_grid, y_grid, z_grid, color=color, alpha=0.7)

    # Plot base circle at z=0
    ax.add_collection3d(Poly3DCollection([list(zip(radius * np.cos(theta), radius * np.sin(theta), np.zeros_like(theta)))], color=color, alpha=0.7))

    # Plot top circle at z=height
    ax.add_collection3d(Poly3DCollection([list(zip(radius * np.cos(theta), radius * np.sin(theta), np.full_like(theta, height)))], color=color, alpha=0.7))

# Initialize the number of cylinders and randomized values
num_cylinders = 5
cylinders = []

# Randomize initial cylinders
for _ in range(num_cylinders):
    cylinders.append({
        'radius': random.uniform(1, 5),
        'height': random.uniform(1, 10),
        'color': [random.random(), random.random(), random.random()]
    })

st.title("Cylindrical Volume Generator")

# Streamlit sidebar for sliders and controls
st.sidebar.header("Control Cylinders")

# Streamlit slider controls for each cylinder
for i, cylinder in enumerate(cylinders):
    st.sidebar.subheader(f"Cylinder {i + 1}")
    cylinder['radius'] = st.sidebar.slider(f"Radius (Cylinder {i + 1})", min_value=0.5, max_value=10.0, value=cylinder['radius'], step=0.1)
    cylinder['height'] = st.sidebar.slider(f"Height (Cylinder {i + 1})", min_value=1.0, max_value=20.0, value=cylinder['height'], step=0.1)
    
    color = st.sidebar.color_picker(f"Choose Color (Cylinder {i + 1})", "#%02x%02x%02x" % tuple(int(c*255) for c in cylinder['color']))
    cylinder['color'] = [int(color.lstrip("#")[i:i+2], 16)/255 for i in (0, 2, 4)]  # Convert hex to RGB

# Plot the cylinders at the top after interaction
fig = plt.figure(figsize=(6, 6), facecolor=(1, 1, 1, 0))  # Set the whole figure's background to transparent
ax = fig.add_subplot(111, projection='3d')

# Set the background of the axis to transparent
ax.set_facecolor((1, 1, 1, 0))  # Set to transparent background for the axis

for cylinder in cylinders:
    draw_cylinder(ax, cylinder['radius'], cylinder['height'], cylinder['color'])

# Remove the grid, axis ticks, and labels
ax.grid(False)  # Disable grid
ax.set_xticks([])  # Remove x-axis ticks
ax.set_yticks([])  # Remove y-axis ticks
ax.set_zticks([])  # Remove z-axis ticks
ax.set_axis_off()  # Optionally, hide the entire axis frame

# Display the plot once with a transparent background
st.pyplot(fig)
