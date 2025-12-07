# app_V3.py
import subprocess
import os
import requests
import json
import re
import glob
import sys
import time
from pathlib import Path

# --- Configuration ---
# Set this to True to keep the .mmd files for inspection
DEBUG_MODE = True 

OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_CHAT_URL = f"{OLLAMA_BASE_URL}/api/chat"
OLLAMA_TAGS_URL = f"{OLLAMA_BASE_URL}/api/tags"

INPUT_DIR = Path("./input")
OUTPUT_DIR = Path("./output")

def check_mmdc_installed():
    """Checks if 'mmdc' is installed."""
    try:
        subprocess.run(['mmdc', '--version'], check=True, capture_output=True, timeout=5)
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired, subprocess.CalledProcessError):
        print("Error: Mermaid CLI (mmdc) not found or misconfigured.")
        print("Try: npm install -g @mermaid-js/mermaid-cli")
        return False

# ------------------------------------------------------------------
# MODEL SELECTION
# ------------------------------------------------------------------
def get_installed_models():
    """Fetches locally installed Ollama models."""
    try:
        response = requests.get(OLLAMA_TAGS_URL, timeout=5)
        response.raise_for_status()
        return sorted([m['name'] for m in response.json().get('models', [])])
    except:
        return []

def select_model_interactive():
    """Interactive menu to choose a model."""
    print("\n--- Ollama Model Selection ---")
    models = get_installed_models()

    if not models:
        return input("No models found. Enter model name manually (e.g., llama3): ").strip() or "llama3"

    for idx, model in enumerate(models, 1):
        print(f"{idx}. {model}")

    while True:
        choice = input(f"\nSelect a model (1-{len(models)}) or type custom name: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(models):
            return models[int(choice) - 1]
        elif choice:
            return choice

# ------------------------------------------------------------------
# CLEANING & GENERATION
# ------------------------------------------------------------------
def clean_mermaid_code(code_string):
    """Clean common LLM formatting errors from Mermaid code."""
    # Remove non-breaking spaces and zero-width spaces
    cleaned = code_string.replace(u'\xa0', ' ').replace(u'\u200b', '')
    
    # Remove markdown code blocks if the regex missed them earlier
    cleaned = cleaned.replace("```mermaid", "").replace("```", "")
    
    # Normalize whitespace (except newlines)
    cleaned = re.sub(r'[ \t\r\f\v]+', ' ', cleaned)
    
    lines = cleaned.splitlines()
    rebuilt = []
    for line in lines:
        s_line = line.strip()
        if s_line:
            rebuilt.append(s_line)
    
    final = '\n'.join(rebuilt)
    # Fix joined brackets (e.g. node]Text -> node]\nText)
    final = re.sub(r'(\])([A-Za-z0-9])', r'\1\n\2', final)
    return final.strip()

def generate_mermaid_code(user_prompt, model_name):
    """Calls Ollama to generate the code."""
    system_msg = (
        "You are a Mermaid Diagram Generator. Output ONLY valid Mermaid code. "
        "Do not include explanations. Start with 'graph TD' or 'flowchart LR'. "
        "Use simple ASCII characters for node IDs."
    )
    
    payload = {
        "model": model_name,
        "messages": [{"role": "system", "content": system_msg}, {"role": "user", "content": user_prompt}],
        "stream": False,
        "options": {"temperature": 0.1}
    }

    try:
        print(f"Thinking ({model_name})...")
        response = requests.post(OLLAMA_CHAT_URL, json=payload, timeout=60)
        response.raise_for_status()
        content = response.json().get("message", {}).get("content", "").strip()
        
        # Try to extract code block
        match = re.search(r"```mermaid\n(.*?)\n```", content, re.DOTALL)
        code = match.group(1) if match else content
        return clean_mermaid_code(code)

    except Exception as e:
        print(f"Error communicating with Ollama: {e}")
        return None

# ------------------------------------------------------------------
# CRITICAL FIX: DEBUGGING SUPPORT ADDED HERE
# ------------------------------------------------------------------
def translate_mermaid_to_image(mermaid_definition, output_path_base, output_format='png'):
    """Generates image from Mermaid code."""
    if not check_mmdc_installed(): return False

    output_path_base.parent.mkdir(parents=True, exist_ok=True)
    output_file = output_path_base.with_suffix(f'.{output_format}')
    
    # We use a unique temp name so multiple runs don't overwrite each other immediately
    temp_file = f"debug_{int(time.time())}.mmd"

    try:
        with open(temp_file, "w", encoding='utf-8') as f:
            f.write(mermaid_definition)

        command = ['mmdc', '-i', temp_file, '-o', str(output_file)]
        
        # Run mmdc
        process = subprocess.run(command, capture_output=True, text=True)

        if process.returncode != 0:
            print(f"\n❌ ERROR: mmdc failed for {output_file.name}")
            print(f"--- STDERR ---\n{process.stderr}\n--------------")
            if DEBUG_MODE:
                print(f"⚠️  DEBUG MODE: Kept temporary file at: {os.path.abspath(temp_file)}")
                print("   Open this file in a text editor to check for syntax errors.")
            return False

        print(f"✅ Saved: {output_file}")
        return True

    except Exception as e:
        print(f"Unexpected error: {e}")
        return False
    finally:
        # Only delete if NOT in debug mode and the file exists
        if not DEBUG_MODE and os.path.exists(temp_file):
            os.remove(temp_file)

# ------------------------------------------------------------------
# MAIN LOOP
# ------------------------------------------------------------------
def main():
    print("Welcome to the Ollama Mermaid Generator (Debug Mode)")
    if not check_mmdc_installed(): return

    selected_model = select_model_interactive()
    OUTPUT_DIR.mkdir(exist_ok=True)

    while True:
        choice = input("\n(1) Describe flowchart  (2) Process files  (q) Quit\n> ").strip().lower()

        mermaid_codes = []
        
        if choice == '1':
            desc = input("Describe flowchart: ")
            if not desc: continue
            code = generate_mermaid_code(desc, selected_model)
            if code:
                name = f"chart_{int(time.time())}"
                mermaid_codes.append((code, OUTPUT_DIR / name))
        
        elif choice == '2':
            if not INPUT_DIR.exists(): INPUT_DIR.mkdir(); print(f"Created {INPUT_DIR}"); continue
            files = list(INPUT_DIR.glob('**/*.mmd'))
            if not files: print("No files found."); continue
            for f in files:
                try:
                    code = clean_mermaid_code(f.read_text(encoding='utf-8'))
                    mermaid_codes.append((code, OUTPUT_DIR / f.relative_to(INPUT_DIR).with_suffix('')))
                except Exception as e: print(f"Error reading {f}: {e}")

        elif choice == 'q': break
        
        # Generation & Error Pause
        for code, path in mermaid_codes:
            print(f"\nProcessing {path.name}...")
            # Print code preview if debugging
            if DEBUG_MODE:
                print(f"--- Code Preview ---\n{code[:100]}...\n--------------------")

            success = translate_mermaid_to_image(code, path)
            
            if not success:
                # Pause so the user can see the error message
                input("\n⚠️ Generation failed. Read errors above and press Enter to continue...")

if __name__ == "__main__":
    main()