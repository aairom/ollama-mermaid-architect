# 🎨 Ollama Mermaid Architect: Local AI Diagram Generator

**Generate, Visualize, and Edit Mermaid flowcharts using local LLMs (Ollama) in a simple Streamlit GUI.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)

---

## ✨ Features

This application enhances the local diagram generation workflow with several key features:

* **100% Local Execution:** No subscriptions, no cloud APIs. All computation runs on your machine using Ollama and local LLMs.
* **Dynamic LLM Selection:** Automatically detects and lets you select any installed model from your local **Ollama** server.
* **Interactive GUI:** Built with **Streamlit** for a simple, responsive, and iterative user experience.
* **Live Visualization:** Instantly renders the generated Mermaid code into an **SVG** diagram directly in the browser.
* **In-App Editing:** Allows manual code fixes and instant re-rendering without having to regenerate the prompt.
* **Error Debugging:** Provides clear `mmdc` output logs directly in the interface if code generation fails.

---

## ⚙️ Prerequisites

You must have the following tools installed and running before starting the application:

1.  **Ollama:** The local LLM runner must be installed and running on `http://localhost:11434`.
    * *Check:* Ensure you have at least one model pulled (e.g., `ollama pull llama3`).
2.  **Node.js & npm:** Required to install the Mermaid CLI tool.
3.  **Mermaid CLI (`mmdc`):** The command-line tool used to convert the Mermaid code into image files (SVG/PNG).

### Installation Steps for Mermaid CLI

Install the necessary dependencies globally using npm:

```bash
# Installs the official Mermaid CLI package
npm install -g @mermaid-js/mermaid-cli
```

## 🚀 Installation & Setup

1. **Clone the Repository**

   Bash

   ```
   git clone [https://github.com/aairom/ollama-mermaid-architect.git]
   (https://github.com/aairom/ollama-mermaid-architect.git)
   cd ollama-mermaid-architect
   ```

2. **Setup Python Environment** (Recommended)

   Bash

   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install Python Dependencies**

   Bash

   ```
   pip install -r requirements.txt
   ```

   *(Create a `requirements.txt` file containing `streamlit`, `requests`, and any other dependencies.)*

------

## ▶️ Usage

1. **Start Ollama:** Ensure your Ollama server is running in the background.

   Bash

   ```
   ollama run granite4 # Or any model you plan to use
   ```

2. **Run the Streamlit Application**

   Bash

   ```
   streamlit run appST.py
   ```

3. **Interface Guide**

   - The app will open in your default browser (`http://localhost:8501`).
   - **Sidebar:** Select your active Ollama model from the dropdown.
   - **Input:** Enter a natural language description of the flowchart you want (e.g., "Create a graph for a CI/CD pipeline showing stages for build, test, and deploy").
   - **Generate:** Click the `🚀 Generate` button.
   - **View/Edit:** Use the tabs to switch between the **Diagram Visualization** (image) and the **Edit Code** view. You can modify the code in the second tab and click **`🔄 Update Diagram`** to instantly see the changes.
   
   ##### !! Console version Interface Guide !!
   
   ```
   python app_V3.py
   ```

------

## 📂 Project Structure

```
.
├── app_V3.py								# The main console version application code.
├── appST.py                # The main Streamlit application code.
├── requirements.txt        # List of Python dependencies.
├── README.md               # This file.
└── input/  								# The foloder were MMD files could be stored to be processed recursivley
└── output/                 # Directory where generated SVG/PNG files are saved.

```

------

## 🤝 Contributing

Contributions are welcome! If you have suggestions for new features (like PDF export, new chart types, or improved error handling), please feel free to open an issue or submit a pull request.

------

## 📄 License

Distributed under the **MIT License**. See `LICENSE` for more information.