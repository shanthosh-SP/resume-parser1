mkdir -p ~/.streamlit/

echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
" > ~/.streamlit/config.toml

sudo apt-get update && sudo apt-get install -y pkg-config
sudo apt-get install -y poppler-utils
pip install -r requirements.txt
