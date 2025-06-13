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

## Use the Agent

### 1. Run Coral Server
<details>

Ensure that the [Coral Server](https://github.com/Coral-Protocol/coral-server) is running on your system. In a new terminal, clone the repository:

```bash
# Clone the Coral Server repository
git clone https://github.com/Coral-Protocol/coral-server.git

# Navigate to the project directory
cd coral-server

# Run the server
./gradlew run
```
</details>

### 2. Run [Interface Agent](https://github.com/Coral-Protocol/Coral-Interface-Agent)
<details>

The Interface Agent is required to interact with the CodeDiffReview Agent. In a new terminal, clone the repository:

```bash
# Clone the Interface Agent repository
git clone https://github.com/Coral-Protocol/Coral-Interface-Agent.git

# Navigate to the project directory
cd Coral-Interface-Agent

# Install `uv`:
pip install uv

# Install dependencies from `pyproject.toml` using `uv`:
uv sync

# Run the agent using `uv`:
uv run python 0-langchain-interface.py
```
</details>

### 3. Run CodeDiffReview Agent
<details>

In a new terminal, clone the repository:

```bash
# Clone the CodeDiffReview Agent repository
git clone https://github.com/Coral-Protocol/Coral-CodeDiffReview-Agent.git

# Navigate to the project directory
cd Coral-CodeDiffReview-Agent

# Install `uv`:
pip install uv

# Install dependencies from `pyproject.toml` using `uv`:
uv sync
```
This command will read the `pyproject.toml` file and install all specified dependencies in a virtual environment managed by `uv`.

Copy the client sse.py from utils to mcp package (Linux/Mac):
```bash
cp -r utils/sse.py .venv/lib/python3.10/site-packages/mcp/client/sse.py
```
OR for Windows:
```bash
cp -r utils\sse.py .venv\Lib\site-packages\mcp\client\sse.py
```
</details>

### 4. Configure Environment Variables
<details>

Get the API Keys:
- [OpenAI API Key](https://platform.openai.com/api-keys)
- [Groq API Key](https://console.groq.com/keys)
- [GitHub Personal Access Token](https://github.com/settings/tokens)

Create a .env file in the project root:
```bash
cp -r .env.example .env
```

Add your API keys and any other required environment variables to the .env file.

Required environment variables:
- `OPENAI_API_KEY`
- `GROQ_API_KEY`
- `GITHUB_ACCESS_TOKEN`

</details>

### 5. Run Agent
<details>

Run the agent using `uv`:
```bash
uv run 2-camel-CodeDiffReviewAgent.py
```
</details>

### 6. Example
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
