import streamlit as st

# 1. Set up the layout and style of the dashboard app window (MUST BE FIRST)
st.set_page_config(page_title="ERW Climate Framework", layout="centered")

# 2. Main Title and Dashboard Identification
st.title("🛰️ ERW Carbon Capture App")
st.markdown("An interactive simulator that shows how crushed rocks trap greenhouse gases when it rains.")
st.markdown("---")

# 3. Simple Rock Selection Dropdown
st.subheader("🪨 Choose Your Type of Rock")
rock_choice = st.selectbox(
    "Select a rock to spread on the ground:",
    ["Standard Volcanic Rock (Basalt)", "Green Volcano Rock (Dunite)", "Super-Fast Melting Rock (Wollastonite)"]
)

# Set the constant 'k' based on how fast the rock melts/reacts in the rain
if rock_choice == "Standard Volcanic Rock (Basalt)":
    k = 5.0  
    rock_desc = "This is normal black lava rock. It is super common and traps carbon at a steady, normal speed."
elif rock_choice == "Green Volcano Rock (Dunite)":
    k = 3.5  
    rock_desc = "This rock is full of a green mineral called Olivine. It reacts quickly and traps carbon faster than normal rock."
else:
    k = 1.5  
    rock_desc = "This is a special calcium rock. It melts in the rain incredibly fast, catching carbon at maximum speed!"

# Simple info banner for the user
st.info(f"**Rock Info:** {rock_desc} (Speed factor 'k' is set to: `{k}`)")
st.markdown("---")

# 4. Create the real-time Interactive Sliders (The Inputs)
st.subheader("📊 Adjust Weather & Rock Amounts")

R = st.slider("🌧️ NASA Rainfall Amount (R in mm/inches)", min_value=0.0, max_value=11.0, value=1.0, step=0.1)
T = st.slider("☀️ NASA Temperature (T in Celsius)", min_value=-25.0, max_value=45.0, value=1.0, step=0.1)
u = st.slider("🚜 Amount of Rock Spread on Fields(u in t/ha(ton per hectare))", min_value=0, max_value=100, value=10, step=1)

st.markdown("---")

# 5. RUN THE ALGEBRA FORMULA (The Core Engine)
capture_factor = (u / (u + k)) * (R * T)

# Calculate trapping percentage based on a peak scale
max_possible_capture = (20 / (20 + 1.5)) * (11.0 * 4.0)
if capture_factor > 0:
    trapped_percentage = min(int((capture_factor / max_possible_capture) * 100), 100)
else:
    trapped_percentage = 0

# 6. Display the calculations and simple metrics
st.subheader("🧮 Math Results")
col1, col2 = st.columns(2)
col1.metric(label="Calculated Capture Factor", value=f"{capture_factor:.2f}")
col2.metric(label="Percentage of Carbon Trapped", value=f"{trapped_percentage}%")

st.markdown("---")

# 7. EMBEDDED JAVASCRIPT PARTICLE SIMULATION
st.write("### 🧬 Microscopic Animation")
st.write("Watch floating orange CO₂ gas dots get trapped and turn into green solid minerals on the rock grid:")

simulation_html = f"""
<div style="text-align: center; font-family: sans-serif; background-color: #1e1e1e; padding: 15px; border-radius: 10px; border: 1px solid #333;">
    <canvas id="erwCanvas" width="500" height="250" style="background: #111; border-radius: 5px; box-shadow: inset 0 0 10px #000;"></canvas>
</div>

<script>
const canvas = document.getElementById('erwCanvas');
const ctx = canvas.getContext('2d');

const pctTrapped = {trapped_percentage};
const totalMolecules = 60;
const targetTrappedCount = Math.round((pctTrapped / 100) * totalMolecules);

const rockNodes = [];
const rows = 4;
const cols = 6;
for (let i = 0; i < rows; i++) {{
    for (let j = 0; j < cols; j++) {{
        rockNodes.push({{
            x: 60 + j * 75,
            y: 50 + i * 50,
            radius: 8,
            occupied: false
        }});
    }}
}}

const molecules = [];
for (let i = 0; i < totalMolecules; i++) {{
    molecules.push({{
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        vx: (Math.random() - 0.5) * 1.5,
        vy: (Math.random() - 0.5) * 1.5,
        radius: 4,
        isTrapped: false,
        targetNode: null
    }});
}}

function animate() {{
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    rockNodes.forEach(node => {{
        ctx.beginPath();
        ctx.arc(node.x, node.y, node.radius, 0, Math.PI * 2);
        ctx.fillStyle = '#444';
        ctx.fill();
        ctx.closePath();
    }});

    molecules.forEach((mol, index) => {{
        if (index < targetTrappedCount) {{
            if (!mol.isTrapped) {{
                let openNode = rockNodes.find(n => !n.occupied);
                if (openNode) {{
                    openNode.occupied = true;
                    mol.isTrapped = true;
                    mol.targetNode = openNode;
                }}
            }}
        }} else {{
            if (mol.isTrapped) {{
                if (mol.targetNode) mol.targetNode.occupied = false;
                mol.isTrapped = false;
                mol.targetNode = null;
                mol.vx = (Math.random() - 0.5) * 1.5;
                mol.vy = (Math.random() - 0.5) * 1.5;
            }}
        }}

        if (mol.isTrapped && mol.targetNode) {{
            let dx = mol.targetNode.x - mol.x;
            let dy = mol.targetNode.y - mol.y;
            mol.x += dx * 0.1;
            mol.y += dy * 0.1;
            
            ctx.beginPath();
            ctx.arc(mol.x, mol.y, mol.radius, 0, Math.PI * 2);
            ctx.fillStyle = '#00ffcc';
            ctx.fill();
            ctx.closePath();
        }} else {{
            mol.x += mol.vx;
            mol.y += mol.vy;

            if (mol.x < 0 || mol.x > canvas.width) mol.vx *= -1;
            if (mol.y < 0 || mol.y > canvas.height) mol.vy *= -1;

            ctx.beginPath();
            ctx.arc(mol.x, mol.y, mol.radius, 0, Math.PI * 2);
            ctx.fillStyle = '#ff9900';
            ctx.fill();
            ctx.closePath();
        }}
    }});

    rockNodes.forEach(n => n.occupied = false);

    requestAnimationFrame(animate);
}}

animate();
</script>
"""

st.components.v1.html(simulation_html, height=300)
st.markdown("---")

# 8. Simple Action Strategy
if capture_factor >= 1.0:
    st.success("🚀 ACTION: START SPREADING ROCK")
    st.info("The weather is perfect! Go ahead and spread the crushed rock on the fields to trap carbon.")
else:
    st.error("🛑 ACTION: WAIT / HOLD POSITION")
    st.warning("It is too dry or cold. Keep the rocks stored until the weather gets better.")




