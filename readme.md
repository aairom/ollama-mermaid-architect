## 🎨 Ollama Mermaid Diagram Generator



This Python application provides an interactive command-line interface (CLI) to generate and render **Mermaid diagrams** (flowcharts) using two primary methods:

1. **AI Generation:** Describing a flowchart in natural language, which is then converted to Mermaid syntax by a local **Ollama** large language model (`granite3.3`).
2. **File Rendering:** Providing a pre-written Mermaid definition file (`.mmd`) for direct rendering.

The application leverages the external **Mermaid CLI (`mmdc`)** tool to convert the Mermaid code into rendered image files (PNG and SVG).

------



## 🚀 Features

- **AI-Powered Generation:** Uses a locally running **Ollama** server and the **`granite3.3`** model to convert text descriptions into valid Mermaid syntax.
- **Mermaid File Rendering:** Renders existing `.mmd` files placed in the `input/` directory.
- **Robust Cleaning:** Includes specialized code to clean and normalize non-standard whitespace characters often introduced by LLMs, preventing common Mermaid parsing errors.
- **Image Output:** Generates both high-quality **PNG** and **SVG** files for easy integration into documents and websites.



## ⚙️ Prerequisites

This application requires three main components to be installed and running on your system:

### 1. Python & Dependencies

You need **Python 3.8+** and the following libraries

```
pip install requests
```



### 2. Ollama and Model

You must have the **Ollama server** running locally and the specified model pulled.

1. **Install Ollama:** Follow the instructions on the [Ollama website](https://ollama.com/).

2. **Start the Ollama Server:** Ensure the server process is running in a terminal or background service (usually by running `ollama serve`).

3. **Pull the Model:** The application is configured to use the `granite3.3` model.

   Bash

   ```
   ollama pull granite3.3
   ```

### 3. Mermaid CLI (`mmdc`)

The application uses the Node.js-based Mermaid command-line tool for image generation.

1. **Install Node.js/npm** (if not already installed).

2. **Install `mmdc` globally:**

   Bash

   ```
   npm install -g @mermaid-js/mermaid-cli
   ```

------



## 💻 Installation and Usage

| **1) Describe a flowchart**    | The application calls Ollama with your description and attempts to extract the Mermaid code. | Requires Ollama server (`ollama serve`) to be running. |
| ------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------ |
| **(2) Provide a Mermaid file** | The application reads a file (e.g., `rag.mmd`) from the `input/` folder. | Useful for rendering pre-existing or complex diagrams. |

### 4. Output



Generated images will be saved in the same directory as `app.py`.

- **AI Generation:** Outputs `generated_flowchart.png` and `generated_flowchart.svg`.
- **File Rendering:** Outputs files named after your input (e.g., `rag.png` and `rag.svg`).

------



## 🛠️ Configuration



The core settings are defined at the top of the `app.py` file. You should only need to modify these if your Ollama setup is non-standard.

| Variable         | Default Value                         | Description                                  |
| ---------------- | ------------------------------------- | -------------------------------------------- |
| `OLLAMA_API_URL` | `http://localhost:11434/api/generate` | The endpoint for Ollama's generation API.    |
| `OLLAMA_MODEL`   | `"granite3.3"` (or other)             | The specific model used for code generation. |

Creating a comprehensive `README.md` for your Ollama-powered Mermaid Diagram Generator application.

------



## 🎨 Ollama Mermaid Diagram Generator



This Python application provides an interactive command-line interface (CLI) to generate and render **Mermaid diagrams** (flowcharts) using two primary methods:

1. **AI Generation:** Describing a flowchart in natural language, which is then converted to Mermaid syntax by a local **Ollama** large language model (`granite3.3`).
2. **File Rendering:** Providing a pre-written Mermaid definition file (`.mmd`) for direct rendering.

The application leverages the external **Mermaid CLI (`mmdc`)** tool to convert the Mermaid code into rendered image files (PNG and SVG).

------



## 🚀 Features



- **AI-Powered Generation:** Uses a locally running **Ollama** server and the **`granite3.3`** model to convert text descriptions into valid Mermaid syntax.
- **Mermaid File Rendering:** Renders existing `.mmd` files placed in the `input/` directory.
- **Robust Cleaning:** Includes specialized code to clean and normalize non-standard whitespace characters often introduced by LLMs, preventing common Mermaid parsing errors.
- **Image Output:** Generates both high-quality **PNG** and **SVG** files for easy integration into documents and websites.

------



## ⚙️ Prerequisites



This application requires three main components to be installed and running on your system:



### 1. Python & Dependencies

You need **Python 3.8+** and the following libraries:

```bash
pip install requests
```



### 2. Ollama and Model



You must have the **Ollama server** running locally and the specified model pulled.

1. **Install Ollama:** Follow the instructions on the [Ollama website](https://ollama.com/).

2. **Start the Ollama Server:** Ensure the server process is running in a terminal or background service (usually by running `ollama serve`).

3. **Pull the Model:** The application is configured to use the `granite3.3` model.

   

   ```bash
   ollama pull granite3.3
   ```



### 3. Mermaid CLI (`mmdc`)



The application uses the Node.js-based Mermaid command-line tool for image generation.

1. **Install Node.js/npm** (if not already installed).

2. **Install `mmdc` globally:**

   

   ```bash
   npm install -g @mermaid-js/mermaid-cli
   ```

------



## 💻 Installation and Usage

### 1. Setup

Clone or download the repository containing `app.py`.

Create a directory named `input` in the same folder as `app.py`:

```bash
mkdir input
```



### 2. Running the Application

Execute the Python script from your terminal:

```bash
python app.py
```



### 3. Interactive Prompts

The application will prompt you for input:

| Option                         | Action                                                       | Notes                                                  |
| ------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------ |
| **(1) Describe a flowchart**   | The application calls Ollama with your description and attempts to extract the Mermaid code. | Requires Ollama server (`ollama serve`) to be running. |
| **(2) Provide a Mermaid file** | The application reads a file (e.g., `rag.mmd`) from the `input/` folder. | Useful for rendering pre-existing or complex diagrams. |

### 4. Output

Generated images will be saved in the same directory as `app.py`.

- **AI Generation:** Outputs `generated_flowchart.png` and `generated_flowchart.svg`.
- **File Rendering:** Outputs files named after your input (e.g., `rag.png` and `rag.svg`).

------



## 🛠️ Configuration

The core settings are defined at the top of the `app.py` file. You should only need to modify these if your Ollama setup is non-standard.

| Variable         | Default Value                         | Description                                  |
| ---------------- | ------------------------------------- | -------------------------------------------- |
| `OLLAMA_API_URL` | `http://localhost:11434/api/generate` | The endpoint for Ollama's generation API.    |
| `OLLAMA_MODEL`   | `"granite3.3"`                        | The specific model used for code generation. |



------



## ⚠️ Troubleshooting



| Error Message                                          | Cause                                                        | Solution                                                     |
| ------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| `404 Client Error: Not Found`                          | Ollama server is not running, or the `/api/generate` route is unavailable. | Ensure `ollama serve` is running in a separate terminal. Verify the model is pulled (`ollama list`). |
| `Error translating Mermaid: ... Parse error on line X` | The Mermaid syntax is invalid, often due to whitespace or character errors. | The `clean_mermaid_code` function attempts to fix this. If it persists, manually check the outputted `temp_mermaid_diagram.mmd` file for collapsed lines or bad characters. |
| `mmdc not found`                                       | Mermaid CLI is not installed or not in your system's PATH.   | Run `npm install -g @mermaid-js/mermaid-cli`.                |