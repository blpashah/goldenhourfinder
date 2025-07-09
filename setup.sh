mkdir -p ~/.streamlit/

echo "\
[server]
headless = true
port = $PORT
enableCORS = false
\n\
" > ~/.streamlit/config.toml
