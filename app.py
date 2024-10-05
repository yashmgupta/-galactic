import math
import numpy as np
import streamlit as st
import plotly.graph_objects as go

# Initialize global variables
SCALE = 350  # 🌱 This is how big the galaxy gets! Bigger the number, bigger the sparkle!

# Function to build spiral arms using NumPy
def build_spiral_stars_np(b, r, rot_fac, fuz_fac, num_stars, height_scale):
    """Return NumPy array of (x,y,z) points for a logarithmic spiral."""
    # It's spiraling time! 🛰️
    i = np.arange(0, num_stars)  # Star index - gotta keep count of all these babies 💫
    theta = np.radians(i)  # Going full circle, in radians! ✨
    fuzz = int(0.030 * abs(r)) * fuz_fac  # Adding some fuzziness, because who needs precision in a galaxy? 💡
    x = r * np.exp(b * theta) * np.cos(theta - np.pi * rot_fac)  # X-coordinates to make it spin, baby!
    y = r * np.exp(b * theta) * np.sin(theta - np.pi * rot_fac)  # Y-coordinates, also spinning 🚀
    x += np.random.randint(-fuzz, fuzz, size=num_stars)  # Adding some randomness - galaxies love chaos 🌑
    y += np.random.randint(-fuzz, fuzz, size=num_stars)  # More chaos! Let's fuzz up that Y axis too 🌀
    # Adjust z-values based on height_scale
    z = np.random.uniform(-height_scale / 2, height_scale / 2, size=num_stars)  # Stars going up and down 🌆
    return np.column_stack((x, y, z))  # Packaging the stars into a nice array like a gift box 🎁

# Function to generate a central bulge
def spherical_coords(num_pts, radius, height_scale):
    """Return NumPy array of uniformly distributed points in a sphere."""
    # It's bulge time! Central core with all the "vintage" stars 🌟
    phi = np.random.uniform(0, np.pi * 2, num_pts)  # Random direction for our core stars
    costheta = np.random.uniform(-1, 1, num_pts)  # Core stars be like "I'm going my own way"
    u = np.random.uniform(0, 1, num_pts)  # Radii from 0 to 1, everyone's welcome 🤸‍♀️

    theta = np.arccos(costheta)  # Converting to actual angles, because math 🤓
    r = radius * u ** (1/3)  # Making sure we use the radius for our spherical goodness 🌐

    x = r * np.sin(theta) * np.cos(phi)  # X-coordinates, in 3D now!
    y = r * np.sin(theta) * np.sin(phi)  # Y-coordinates, 3D vibes 🕷
    z = r * np.cos(theta) * (height_scale / radius)  # Z-coordinates, giving the galaxy that fluffy look 🎉
    return np.column_stack((x, y, z))  # Returning our glorious bulging stars 🌟

def main():
    st.set_page_config(page_title='3D Galaxy Simulation', page_icon=':milky_way:', layout='wide')
    st.title('Simulated Spiral Galaxy with Central Bulge')

    # Sidebar controls
    st.sidebar.header("Galaxy Parameters")
    num_stars = st.sidebar.slider('Stars per Arm', 500, 5000, 1000, 500)  # ⭐ That's a lot of stars! ✨
    num_core_stars = st.sidebar.slider('Core Stars', 1000, 5000, 2000, 500)  # Bulge stars need love too 💖
    spiral_openness = st.sidebar.slider('Spiral Openness', -0.5, 0.0, -0.3, 0.05)  # Less open? More open? Choose your swirl!
    scale = st.sidebar.slider('Galactic Scale', 100, 500, 350, 50)  # Bigger galaxy = More chaos 🧠
    rotation_speed = st.sidebar.slider('Rotation Speed', 10, 100, 50, 10)  # Spin that galaxy faster - wheeeee! 🌀
    # New slider for galaxy height
    height_scale = st.sidebar.slider('Galactic Height', 1, 100, 100, 1)  # Make that galaxy TALLER 🌱

    # Update global SCALE
    global SCALE
    SCALE = scale

    # Assign scale factor, rotation factor, and fuzz factor for spiral arms.
    arms_info = [(SCALE, 1, 1.5), (SCALE, 0.91, 1.5),
                 (-SCALE, 1, 1.5), (-SCALE, -1.09, 1.5),
                 (-SCALE, 0.5, 1.5), (-SCALE, 0.4, 1.5),
                 (-SCALE, -0.5, 1.5), (-SCALE, -0.6, 1.5)]

    # Create lists of star positions for galaxy:
    leading_arm = []
    trailing_arm = []
    for i, arm_info in enumerate(arms_info):
        arm = build_spiral_stars_np(
            b=spiral_openness,
            r=arm_info[0],
            rot_fac=arm_info[1],
            fuz_fac=arm_info[2],
            num_stars=num_stars,
            height_scale=height_scale
        )
        if i % 2 != 0:
            leading_arm.extend(arm)  # This is the leading arm - look at all those overachieving stars! 💥
        else:
            trailing_arm.extend(arm)  # Trailing arm - these stars like to take it slow 🦌
    core_stars = spherical_coords(num_core_stars, SCALE / 15, height_scale)  # Central core being extra as always 🌟

    # Prepare data for Plotly
    x_leading, y_leading, z_leading = np.array(leading_arm).T
    x_trailing, y_trailing, z_trailing = np.array(trailing_arm).T
    x_core, y_core, z_core = core_stars.T

    # Create color gradients
    leading_colors = np.random.uniform(0, 1, len(x_leading))  # Leading arm is extra colorful 🟡
    trailing_colors = np.random.uniform(0, 1, len(x_trailing))  # Trailing arm got some style too 🟢
    core_colors = np.random.uniform(0, 1, len(x_core))  # Core stars are HOT 🔥

    # Create Plotly traces
    trace_leading = go.Scatter3d(
        x=x_leading, y=y_leading, z=z_leading,
        mode='markers',
        marker=dict(size=2, color=leading_colors, colorscale='Viridis', opacity=0.8),
        hoverinfo='none'
    )

    trace_trailing = go.Scatter3d(
        x=x_trailing, y=y_trailing, z=z_trailing,
        mode='markers',
        marker=dict(size=2, color=trailing_colors, colorscale='Plasma', opacity=0.8),
        hoverinfo='none'
    )

    trace_core = go.Scatter3d(
        x=x_core, y=y_core, z=z_core,
        mode='markers',
        marker=dict(size=2, color=core_colors, colorscale='Hot', opacity=0.8),
        hoverinfo='none'
    )

    data = [trace_leading, trace_trailing, trace_core]

    # Create initial figure layout
    layout = go.Layout(
        paper_bgcolor='black',  # Spaaace! The final frontier 🚀
        scene=dict(
            xaxis=dict(visible=False),  # We don't need those boring old axes 🤨
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
            bgcolor='black',
            camera=dict(eye=dict(x=1.25, y=1.25, z=0.3))  # Setting up the galactic view 😉
        ),
        margin=dict(l=0, r=0, b=0, t=0),  # Full screen galaxy, yes please! 😍
        showlegend=False,
        updatemenus=[dict(
            type="buttons",
            buttons=[dict(label="Animate",
                          method="animate",
                          args=[None, {"frame": {"duration": 1000 / rotation_speed, "redraw": True},
                                       "fromcurrent": True, "transition": {"duration": 0}}])])]
    )

    # Create frames for animation
    frames = []
    for angle in range(0, 360, 5):
        camera = dict(
            eye=dict(
                x=1.5 * np.cos(np.radians(angle)),
                y=1.5 * np.sin(np.radians(angle)),
                z=0.3
            )
        )
        frames.append(go.Frame(layout=dict(scene_camera=camera)))  # Let the camera roll, galaxy in action! 🎭

    fig = go.Figure(data=data, layout=layout, frames=frames)

    # Display the figure
    st.plotly_chart(fig, use_container_width=True)

    # Educational content
    st.sidebar.header("About Spiral Galaxies")
    st.sidebar.info("""
    Spiral galaxies consist of a flat, rotating disk containing stars, gas, and dust, and a central concentration of stars known as the bulge.
    - **Arms**: Sites of ongoing star formation.
    - **Core**: Contains older stars.

    [Learn More](https://en.wikipedia.org/wiki/Spiral_galaxy)
    """)

if __name__ == '__main__':
    main()
