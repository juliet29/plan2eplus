
push:
  rm -rf dist && source .env && uv version --bump patch && uv build && uv publish 


update-deps:
  uv add ~/_UILCode/gqe-phd/fpopt/utils4plans
  uv add ~/_UILCode/gqe-phd/fpopt/geomeppy


test-ops:
  uv run pytest tests/test_ops


  
