## [Coral CodeDiffReview Agent](https://github.com/Coral-Protocol/Coral-CodeDiffReview-Agent)
 
The CodeDiffReview Agent helps you compare the files changed in a specific commit when you provide the repository name and PR number.

## Responsibility

The CodeDiffReview Agent automates code diff review for pull requests, making it easy to see what changed in a PR and summarize the impact.

## Details
- **Framework**: CAMEL-AI
- **Tools used**: GitHub MCP Server Tools, Coral Server Tools
- **AI model**: OpenAI GPT-4.1/Groq Llama 3.3 70B
- **Date added**: 02/05/25
- **License**: MIT

## Setup the Agent

### 1. Clone & Install Dependencies

<details>  

```bash
# In a new terminal clone the repository:
git clone https://github.com/Coral-Protocol/Coral-CodeDiffReview-Agent.git

# Navigate to the project directory:
cd Coral-CodeDiffReview-Agent

# Download and run the UV installer, setting the installation directory to the current one
curl -LsSf https://astral.sh/uv/install.sh | env UV_INSTALL_DIR=$(pwd) sh

# Create a virtual environment named `.venv` using UV
uv venv .venv

# Activate the virtual environment
source .venv/bin/activate

# install uv
pip install uv

# Install dependencies from `pyproject.toml` using `uv`:
uv sync
```

</details>

### 2. Configure Environment Variables

Get the API Key:
[OpenAI](https://platform.openai.com/api-keys) or [GROQ](https://console.groq.com/keys)

<details>

```bash
# Create .env file in project root
cp -r .env.example .env
```
</details>

## Run the Agent

You can run in either of the below modes to get your system running.  

- The Executable Model is part of the Coral Protocol Orchestrator which works with [Coral Studio UI](https://github.com/Coral-Protocol/coral-studio).  
- The Dev Mode allows the Coral Server and all agents to be seaprately running on each terminal without UI support.  

### 1. Executable Mode

Checkout: [How to Build a Multi-Agent System with Awesome Open Source Agents using Coral Protocol](https://github.com/Coral-Protocol/existing-agent-sessions-tutorial-private-temp) and update the file: `coral-server/src/main/resources/application.yaml` with the details below, then run the [Coral Server](https://github.com/Coral-Protocol/coral-server) and [Coral Studio UI](https://github.com/Coral-Protocol/coral-studio). You do not need to set up the `.env` in the project directory for running in this mode; it will be captured through the variables below.

<details>

For Linux or MAC:

```bash
# PROJECT_DIR="/PATH/TO/YOUR/PROJECT"

applications:
  - id: "app"
    name: "Default Application"
    description: "Default application for testing"
    privacyKeys:
      - "default-key"
      - "public"
      - "priv"

registry:
  CodeDiff:
    options:
      - name: "API_KEY"
        type: "string"
        description: "API key for the service"
      - name: "GITHUB_ACCESS_TOKEN"
        type: "string"
        description: "key for the github service"
    runtime:
      type: "executable"
      command: ["bash", "-c", "${PROJECT_DIR}/run_agent.sh main.py"]
      environment:
        - name: "API_KEY"
          from: "API_KEY"
        - name: "GITHUB_ACCESS_TOKEN"
          from: "GITHUB_ACCESS_TOKEN"
        - name: "MODEL_NAME"
          value: "gpt-4.1"
        - name: "MODEL_PROVIDER"
          value: "openai"
        - name: "MODEL_TOKEN"
          value: "16000"
        - name: "MODEL_TEMPERATURE"
          value: "0.3"

```

For Windows, create a powershell command (run_agent.ps1) and run:

```bash
command: ["powershell","-ExecutionPolicy", "Bypass", "-File", "${PROJECT_DIR}/run_agent.ps1","main.py"]
```

</details>

### 2. Dev Mode

Ensure that the [Coral Server](https://github.com/Coral-Protocol/coral-server) is running on your system and run below command in a separate terminal.

<details>

```bash
# Run the agent using `uv`:
uv run python main.py
```
</details>


## Example

<details>

```bash
# Input:
Please get the code diffs for PR #2 in the repo `renxinxing123/camel-software-testing`

# Output:
Here are the code diffs/changed files for PR #2 in the repo `renxinxing123/camel-software-testing`:

---
**File:** `camel/toolkits/semantic_scholar_toolkit.py`

```diff
@@ -113,11 +113,11 @@ def fetch_paper_data_id(
             ]
 
         url = f"{self.base_url}/paper/{paper_id}"
-        query_params = {"fields": ",".join(fields)}
+        query_params = {"wrong_key": ",".join(fields)}
         try:
             response = requests.get(url, params=query_params)
             response.raise_for_status()
-            return response.json()
+            return {"wrong_key": "wrong_value"}
         except requests.exceptions.RequestException as e:
             return {
                 "error": f"Request failed: {e!s}",

**Summary:**
- The query parameter key was changed from `fields` to `wrong_key`.
- The return value was changed from the response JSON to a hardcoded dictionary: `{ "wrong_key": "wrong_value" }`.
```

</details>


## Creator Details
- **Name**: Xinxing
- **Affiliation**: Coral Protocol
- **Contact**: [Discord](https://discord.com/invite/Xjm892dtt3)