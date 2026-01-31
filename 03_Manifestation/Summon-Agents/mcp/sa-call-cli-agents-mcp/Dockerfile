FROM python:3.12-slim

WORKDIR /app

# Install system dependencies + Node.js
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    ca-certificates \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Install all CLI agents globally
RUN npm install -g \
    @anthropic-ai/claude-code \
    @openai/codex \
    @google/gemini-cli \
    && echo "Installed CLI tools:" \
    && which claude || echo "claude not found" \
    && which codex || echo "codex not found" \
    && which gemini || echo "gemini not found"

## (Optional) Google Cloud SDK
## Gemini CLI is provided by @google/gemini-cli above, so gcloud is not required for core operation.

# Copy MCP server package
COPY pyproject.toml README.md ./
COPY src/ ./src/

# Install MCP server
RUN pip install --no-cache-dir -e .

# Create workspace directory structure
RUN mkdir -p /workspace/02_Swarm/Context-Orchestrated-Filesystem/skills

# Environment variables
ENV AAOS_ROOT=/workspace
ENV COF_ROOT=/workspace/02_Swarm/Context-Orchestrated-Filesystem

# API keys must be provided at runtime via:
#   -e ANTHROPIC_API_KEY=sk-ant-...
#   -e OPENAI_API_KEY=sk-...
#   -e GOOGLE_API_KEY=...

ENTRYPOINT ["sa-call-cli-agents-mcp"]
