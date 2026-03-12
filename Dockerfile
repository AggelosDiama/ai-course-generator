# Use a slim Python image
FROM python:3.11-slim

# Install uv binary from the official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 1. Copy only dependency files first to leverage Docker layer caching
COPY pyproject.toml requirements.txt* ./

# 2. Install dependencies using uv (blazing fast)
# --system flag tells uv to install into the global site-packages
RUN uv pip install --system --no-cache -r requirements.txt

# 3. Copy the rest of the project
COPY . .

# Expose Streamlit's default port
EXPOSE 8501

# Run the application
# Using 'python -m' ensures the 'src' folder is treated as a package
CMD ["python", "-m", "streamlit", "run", "src/main.py", "--server.port=8501", "--server.address=0.0.0.0"]