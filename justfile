
push:
  rm -rf dist && source .env && uv version --bump patch && uv build && uv publish 


update-deps:
  uv add ~/_UILCode/gqe-phd/fpopt/utils4plans/
  uv add ~/_UILCode/gqe-phd/fpopt/geomeppy/

update-geomeppy:
  uv add ~/_UILCode/gqe-phd/fpopt/geomeppy/


test-ops:
  uv run pytest tests/test_ops


################### 
################### 
# TRIALS
################### 

study-case:
  uv run replan studies study-case
