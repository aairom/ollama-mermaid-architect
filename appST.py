# appST.py
import streamlit as st
import subprocess
import requests
import json
import re
import os
import time
from pathlib import Path

# --- Configuration ---
OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_CHAT_URL = f"{OLLAMA_BASE_URL}/api/chat"
OLLAMA_TAGS_URL = f"{OLLAMA_BASE_URL}/api/tags"
OUTPUT_DIR = Path("./output")
OUTPUT_DIR.mkdir(exist_ok=True)

# --- Page Config ---
st.set_page_config(
    page_title="Ollama Mermaid Architect",
    page_icon="🎨",
    layout="wide"
)

# --- Session State Initialization ---
if 'mermaid_code' not in st.session_state:
    st.session_state['mermaid_code'] = ""
if 'generated_image_path' not in st.session_state:
    st.session_state['generated_image_path'] = None

# --- Helper Functions (Reused & Adapted) ---

def check_mmdc_installed():
    """Checks if mmdc is available."""
    try:
        subprocess.run(['mmdc', '--version'], check=True, capture_output=True, timeout=5)
        return True
    except:
        return False

def get_installed_models():
    """Fetches models from Ollama."""
    try:
        response = requests.get(OLLAMA_TAGS_URL, timeout=2)
        if response.status_code == 200:
            return [m['name'] for m in response.json().get('models', [])]
        return []
    except:
        return []

def clean_mermaid_code(code_string):
    """Cleans up LLM output."""
    # Remove markdown tags
    clean = re.sub(r'```mermaid', '', code_string, flags=re.IGNORECASE)
    clean = re.sub(r'```', '', clean)
    
    # Fix common syntax issues
    clean = clean.replace(u'\xa0', ' ').replace(u'\u200b', '')
    
    # Normalize lines
    lines = [line.strip() for line in clean.splitlines() if line.strip()]
    return '\n'.join(lines)

def generate_code(prompt, model):
    """Calls Ollama API."""
    system_msg = (
        "You are a Mermaid Diagram Generator. "
        "Output ONLY valid Mermaid code. Start with 'graph TD' or 'flowchart LR'. "
        "Do NOT include explanations or markdown ticks."
    )
    
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": prompt}
        ],
        "stream": False,
        "options": {"temperature": 0.2}
    }
    
    try:
        response = requests.post(OLLAMA_CHAT_URL, json=payload, timeout=60)
        if response.status_code == 200:
            content = response.json()['message']['content']
            return clean_mermaid_code(content)
        else:
            st.error(f"Ollama Error: {response.text}")
            return None
    except Exception as e:
        st.error(f"Connection Error: {e}")
        return None

def render_diagram(mermaid_code):
    """Runs mmdc to generate an SVG for display."""
    timestamp = int(time.time())
    temp_mmd = OUTPUT_DIR / f"temp_{timestamp}.mmd"
    output_svg = OUTPUT_DIR / f"diagram_{timestamp}.svg"
    
    try:
        # Write MMD file
        with open(temp_mmd, "w", encoding='utf-8') as f:
            f.write(mermaid_code)
            
        # Run MMDC
        cmd = ['mmdc', '-i', str(temp_mmd), '-o', str(output_svg), '-b', 'transparent']
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            return str(output_svg)
        else:
            st.error("Mermaid Compilation Failed:")
            st.code(result.stderr)
            return None
            
    except Exception as e:
        st.error(f"System Error: {e}")
        return None
    finally:
        if temp_mmd.exists():
            temp_mmd.unlink()

# --- GUI Layout ---

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Check MMDC status
    if check_mmdc_installed():
        st.success("Mermaid CLI: Detected ✅")
    else:
        st.error("Mermaid CLI: Not Found ❌")
        st.info("Run: `npm install -g @mermaid-js/mermaid-cli`")
        st.stop()

    # Model Selector
    models = get_installed_models()
    if models:
        selected_model = st.selectbox("Select Ollama Model", models, index=0)
    else:
        st.warning("Ollama not detected or no models found.")
        selected_model = st.text_input("Manually enter model name", "llama3")
        
    st.markdown("---")
    st.markdown("### Tips")
    st.markdown("- Be specific about direction (Top-Down vs Left-Right).")
    st.markdown("- Mention specific node shapes if needed.")

# Main Content
st.title("🎨 Ollama Mermaid Architect")
st.markdown("Generate, Visualize, and Edit flowcharts using local LLMs.")

# Input Section
user_prompt = st.text_area("Describe your flowchart:", height=100, placeholder="e.g. Create a flowchart for a login process including password reset...")

col1, col2 = st.columns([1, 5])
with col1:
    generate_btn = st.button("🚀 Generate", type="primary")

if generate_btn and user_prompt:
    with st.spinner(f"Asking {selected_model} to design your chart..."):
        generated_code = generate_code(user_prompt, selected_model)
        
        if generated_code:
            st.session_state['mermaid_code'] = generated_code
            # Automatically render upon generation
            svg_path = render_diagram(generated_code)
            st.session_state['generated_image_path'] = svg_path

# Display Section (Only if we have code in state)
if st.session_state['mermaid_code']:
    st.markdown("---")
    
    # We use tabs to separate the Visuals from the Code
    tab_visual, tab_code = st.tabs(["🖼️ Diagram Visualization", "📝 Edit Code"])
    
    with tab_visual:
        if st.session_state['generated_image_path'] and os.path.exists(st.session_state['generated_image_path']):
            # Display the SVG image
            st.image(st.session_state['generated_image_path'], use_container_width=True)
            
            # Download Button
            with open(st.session_state['generated_image_path'], "rb") as file:
                btn = st.download_button(
                    label="📥 Download SVG",
                    data=file,
                    file_name="flowchart.svg",
                    mime="image/svg+xml"
                )
        else:
            st.warning("No image generated yet or generation failed.")

    with tab_code:
        st.info("You can edit the code below and press 'Update' to re-render.")
        # Text area allows editing the code manually
        edited_code = st.text_area("Mermaid Code", st.session_state['mermaid_code'], height=300)
        
        if st.button("🔄 Update Diagram"):
            st.session_state['mermaid_code'] = edited_code
            new_svg_path = render_diagram(edited_code)
            if new_svg_path:
                st.session_state['generated_image_path'] = new_svg_path
                st.rerun() # Refresh to show new image