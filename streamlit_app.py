import json
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components


ROOT = Path(__file__).resolve().parent
CATALOG_FILES = ("feats.json", "talents.json", "equipment.json")


def build_app_html() -> str:
    catalogs = {
        filename: json.loads((ROOT / "data" / filename).read_text(encoding="utf-8"))
        for filename in CATALOG_FILES
    }
    catalog_json = json.dumps(catalogs, ensure_ascii=False)
    for character, replacement in (("<", "\\u003c"), (">", "\\u003e"), ("&", "\\u0026")):
        catalog_json = catalog_json.replace(character, replacement)

    bridge = f"""<script>
      (() => {{
        const catalogs = {catalog_json};
        const nativeFetch = window.fetch.bind(window);
        window.fetch = async (input, init) => {{
          const url = typeof input === 'string' ? input : input instanceof URL ? input.href : input.url;
          const filename = String(url).split(/[?#]/, 1)[0].split('/').pop();
          if (Object.prototype.hasOwnProperty.call(catalogs, filename)) {{
            const data = catalogs[filename];
            return new Response(JSON.stringify(data), {{
              status: 200,
              headers: {{ "Content-Type": "application/json" }}
            }});
          }}
          return nativeFetch(input, init);
        }};
      }})();
    </script>"""

    html = (ROOT / "index.html").read_text(encoding="utf-8")
    script_tag = "  <script>\n"
    if script_tag not in html:
        raise RuntimeError("Could not find the app script insertion point in index.html")
    return html.replace(script_tag, f"{bridge}\\n{script_tag}", 1)


def main() -> None:
    st.set_page_config(
        page_title="Outer Rim Character Ledger",
        page_icon="✦",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    st.markdown(
        """
        <style>
          .block-container { max-width: 100%; padding: 1rem 1rem 0; }
          header[data-testid="stHeader"], footer { display: none; }
          iframe[title="streamlit.components.v1.html"] { width: 100%; }
        </style>
        """,
        unsafe_allow_html=True,
    )
    components.html(build_app_html(), height=1050, scrolling=True)


if __name__ == "__main__":
    main()
