FROM python:3.13-slim

WORKDIR /app

# Install system dependencies and Node.js
RUN apt-get update && apt-get install -y \
    curl \
    git \
    build-essential \
    ca-certificates \
    gnupg \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install --upgrade pip && pip install uv

# Copy source files into container
COPY . .

# Create virtual environment and install dependencies
RUN uv venv && uv pip install --upgrade pip && uv sync --no-dev

# Override mcp.client.sse.py using Python path detection
RUN cp utils/sse.py $(.venv/bin/python -c "import mcp.client, os; print(os.path.join(os.path.dirname(mcp.client.__file__), 'sse.py'))")

# Expose necessary ports
EXPOSE 5555

# Run GitHub MCP server + your agent
CMD ["uv", "run", "python", "2-camel-CodeDiffReviewAgent.py"]

