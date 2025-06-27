if [ ! -d ".venv" ]; then
    python -m venv .venv
fi
source .venv/bin/activate
pip install .
pip install pytest
pytest .
deactivate