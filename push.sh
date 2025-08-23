# TODO run from root -> pass path 
rm -rf dist && source .env && uv version --bump patch && uv build && uv publish 