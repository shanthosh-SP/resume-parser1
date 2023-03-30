#!/bin/bash

# Install poppler-utils and pkg-config
apt-get update
apt-get install -y poppler-utils pkg-config

# Create Streamlit config file
mkdir -p ~/.streamlit/
echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
" > ~/.streamlit/config.toml
