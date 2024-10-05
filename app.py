import math
import numpy as np
from random import randint, uniform
import streamlit as st
import plotly.graph_objects as go
import time

# Set the radius of the galactic disc (scaling factor):
SCALE = 350

# Function to build a single spiral arm
def build_spiral_stars(b, r, rot_fac, fuz_fac):
    """Return list of (x,y,z) points for a logarithmic spiral.

    b = constant for spiral direction and "openness"
    r = scale factor (galactic disc radius)
    rot_fac = factor to rotate each spiral arm
    fuz_fac = randomly shift star position; applied to 'fuzz' variable
    """
    fuzz = int(0.030 * abs(r))  # Scalable initial amount to shift locations.
    num_stars = 1000
    spiral_stars = []
    for i in range(0, num_stars):
        theta = math.radians(i)
        x = r * math.exp(b * theta) * math.cos(theta - math.pi * rot_fac) - randint(-fuzz, fuzz) * fuz_fac
        y = r * math.exp(b * theta) * math.sin(theta - math.pi * rot_fac) - randint(-fuzz, fuzz) * fuz_fac
        z = uniform(-SCALE / (SCALE * 3), SCALE / (SCALE * 3))
        spiral_stars.append((x, y, z))
    return spiral_stars

# Function to generate a central bulge
def spherical_coords(num_pts, radius):
    """Return list of uniformly distributed points in a sphere."""
    position_list = []
    for _ in range(num_pts):
        coords = np.random.normal(0, 1, 3)
        coords *= radius
        coords[2] *= 0.02  # Reduce z range
        position_list.append(list(coords))
    return position_list

# Function to build spiral arms
def build_spiral_arms(b, arms_info):
    """Return lists of point coordinates for galactic spiral arms.

    b = constant for spiral direction and "openness"
    arms_info = list of scale, rotation, and fuzz factors
    """
    leading_arms = []
    trailing_arms = []
    for i, arm_info in enumerate(arms_info):
        arm = build_spiral_stars(b=b,
                                 r=arm_info[0],
                                 rot_fac=arm_info[1],
                                 fuz_fac=arm_info[2])
        if i % 2 != 0:
            leading_arms.extend(arm)
        else:
            trailing_arms.extend(arm)
    return leading_arms, trailing_arms

def main():
    st.set_page_config(page_title='3D Galaxy Simulation', page_icon=':milky_way:', layout='wide')
    st.title('Simulated Spiral Galaxy with Central Bulge')

    # Initialize session state
    if 'animate' not in st.session_state:
        st.session_state['animate'] = False

    # Assign scale factor, rotation factor, and fuzz factor for spiral arms.
    arms_info = [(SCALE, 1, 1.5), (SCALE, 0.91, 1.5),
                 (-SCALE, 1, 1.5), (-SCALE, -1.09, 1.5),
                 (-SCALE, 0.5, 1.5), (-SCALE, 0.4, 1.5),
                 (-SCALE, -0.5, 1.5), (-SCALE, -0.6, 1.5)]

    # Create lists of star positions for galaxy:
    leading_arm, trailing_arm = build_spiral_arms(b=-0.3, arms_info=arms_info)
    core_stars = spherical_coords(2000, SCALE / 15)

    # Prepare data for Plotly
    x_leading, y_leading, z_leading = zip(*leading_arm)
    x_trailing, y_trailing, z_trailing = zip(*trailing_arm)
    x_core, y_core, z_core = zip(*core_stars)

    # Create Plotly traces
    trace_leading = go.Scatter3d(
        x=x_leading,
        y=y_leading,
        z=z_leading,
        mode='markers',
        marker=dict(
            size=1,
            color='white'
        ),
        name='Leading Arm'
    )

    trace_trailing = go.Scatter3d(
        x=x_trailing,
        y=y_trailing,
        z=z_trailing,
        mode='markers',
        marker=dict(
            size=1,
            color='white'
        ),
        name='Trailing Arm'
    )

    trace_core = go.Scatter3d(
        x=x_core,
        y=y_core,
        z=z_core,
        mode='markers',
        marker=dict(
            size=1,
            color='white'
        ),
        name='Core'
    )

    data = [trace_leading, trace_trailing, trace_core]

    layout = go.Layout(
        paper_bgcolor='black',
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
            bgcolor='black',
            camera=dict(
                eye=dict(x=1.25, y=1.25, z=1.25)
            )
        ),
        margin=dict(l=0, r=0, b=0, t=0),
        showlegend=False
    )

    fig = go.Figure(data=data, layout=layout)

    # Create a placeholder for the plot
    plot_placeholder = st.empty()

    # Create the animate button
    if st.button('Animate Galaxy'):
        st.session_state['animate'] = not st.session_state['animate']

    if st.session_state['animate']:
        # Animate the rotation
        for angle in range(0, 360, 5):
            camera = dict(
                eye=dict(
                    x=1.5 * np.cos(np.radians(angle)),
                    y=1.5 * np.sin(np.radians(angle)),
                    z=0.3  # Adjust z to control the elevation angle
                )
            )
            fig.update_layout(scene_camera=camera)
            plot_placeholder.plotly_chart(fig, use_container_width=True)
            time.sleep(0.1)
        st.session_state['animate'] = False
    else:
        # Display the static plot
        plot_placeholder.plotly_chart(fig, use_container_width=True)

if __name__ == '__main__':
    main()
