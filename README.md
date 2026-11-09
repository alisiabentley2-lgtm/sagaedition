# Outer Rim Character Ledger

## Run with Streamlit

From the project directory, create a Python environment, install the app dependency, and start Streamlit:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
streamlit run streamlit_app.py
```

On Windows PowerShell, activate the environment with `.venv\Scripts\Activate.ps1`.

The Streamlit entry point embeds the existing character app and its feat, talent, and equipment catalogs, so the browser does not need to fetch the local `data/` files separately. Character records continue to use browser-local storage; they are not synchronized to the Streamlit server or between devices. The app can also be deployed to Streamlit Community Cloud by selecting `streamlit_app.py` as the main file and using `requirements.txt` for dependencies.