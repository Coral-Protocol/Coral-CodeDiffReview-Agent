### Responsibility

Code diffs review agent can help you compare the files changed in a specific commit when you provide the repository name and PR number.

### Details

* Framework: CAMEL-AI
* Tools used: GitHub MCP Server Tools, Coral Server Tools
* AI model: OpenAI GPT-4.1/Groq Llama 3.3 70B
* Date added: 02/05/25
* Licence: MIT

## Use the Agent

### 1. Clone & Install Dependencies

Run [Interface Agent](https://github.com/Coral-Protocol/Coral-Interface-Agent)
<details>


If you are trying to run Open Deep Research agent and require an input, you can either create your agent which communicates on the coral server or run and register the Interface Agent on the Coral Server. In a new terminal clone the repository:


```bash
git clone https://github.com/Coral-Protocol/Coral-Interface-Agent.git
```
Navigate to the project directory:
```bash
cd Coral-Interface-Agent
```

Install `uv`:
```bash
pip install uv
```
Install dependencies from `pyproject.toml` using `uv`:
```bash
uv sync
```

Configure API Key
```bash
export OPENAI_API_KEY=
```

Run the agent using `uv`:
```bash
uv run python 0-langchain-interface.py
```

</details>

Agent Installation

<details>

Clone the repository:
```bash
git clone https://github.com/Coral-Protocol/Coral-CodeDiffReview-Agent.git
```

Navigate to the project directory:
```bash
cd Coral-CodeDiffReview-Agent
```

Install `uv`:
```bash
pip install uv
```

Install dependencies from `pyproject.toml` using `uv`:
```bash
uv sync
```

This command will read the `pyproject.toml` file and install all specified dependencies in a virtual environment managed by `uv`.

Copy the client sse.py from utils to mcp package
```bash
cp -r utils/sse.py .venv/lib/python3.10/site-packages/mcp/client/sse.py
```

OR Copy this for windows
```bash
cp -r utils\sse.py .venv\Lib\site-packages\mcp\client\sse.py
```

</details>

### 2. Configure Environment Variables

<details>

Copy the example file and update it with your credentials:

```bash
cp .env.example .env
```

Required environment variables:

* `OPENAI_API_KEY`
* `GROQ_API_KEY`
* `GITHUB_ACCESS_TOKEN`

* **OPENAI_API_KEY:**
  Sign up at [platform.openai.com](https://platform.openai.com/), go to “API Keys” under your account, and click “Create new secret key.”

* **GROQ_API_KEY:**
  Register at [groq.com](https://groq.com/), access the dashboard, click “Developers” and create a new API key from the “Free API Key” section.

* **GITHUB_ACCESS_TOKEN:**
  Log in to [github.com](https://github.com/), go to **Settings → Developer settings → Personal access tokens**, then “Generate new token,” select the required scopes, and copy the generated token.

</details>
  
### 3. Run Agent

<details>
  
Run the agent using `uv`:
```bash
uv run 2-camel-CodeDiffReviewAgent.py
```

</details>

### 4. Example

<details>

Input:

```bash
#Send message to the interface agent:
Please get the code diffs for PR #2 in the repo `renxinxing123/camel-software-testing`
```

Output:

```bash
Here are the code diffs/changed files for PR #2 in the repo `renxinxing123/camel-software-testing`:

---
**File:** `camel/toolkits/semantic_scholar_toolkit.py`

```diff
@@ -113,11 +113,11 @@ def fetch_paper_data_id(
             ]
 
         url = f&quot;{self.base_url}/paper/{paper_id}&quot;
-        query_params = {&quot;fields&quot;: &quot;,&quot;.join(fields)}
+        query_params = {&quot;wrong_key&quot;: &quot;,&quot;.join(fields)}
         try:
             response = requests.get(url, params=query_params)
             response.raise_for_status()
-            return response.json()
+            return {&quot;wrong_key&quot;: &quot;wrong_value&quot;}
         except requests.exceptions.RequestException as e:
             return {
                 &quot;error&quot;: f&quot;Request failed: {e!s}&quot;,

**Summary:**
- The query parameter key was changed from `fields` to `wrong_key`.
- The return value was changed from the response JSON to a hardcoded dictionary: `{ &quot;wrong_key&quot;: &quot;wrong_value&quot; }`.
```

</details>

## Creator details

* Name: Xinxing
* Affiliation: Coral Protocol
* Contact: [Discord](https://discord.com/invite/Xjm892dtt3)
