
push:
  rm -rf dist && source .env && uv version --bump patch && uv build && uv publish 


update-deps:
  uv add /Users/julietnwagwuume-ezeoke/_UILCode/gqe-phd/fpopt/utils4plans


test-ops:
  uv run pytest tests/test_ops


  
