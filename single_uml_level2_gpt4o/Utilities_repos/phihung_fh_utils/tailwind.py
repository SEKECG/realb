import os
import subprocess
from pathlib import Path

TAILWIND_CONFIG = "tailwind.config.js"
TAILWIND_DAISYCSS_CONFIG = "tailwind.daisyui.config.js"
TAILWIND_SOURCE_CSS = "src/styles/tailwind.css"
TAILWIND_URI = "/static/tailwind.css"

def add_daisy_and_tailwind(app, cfg, css, uri):
    _add(app, cfg, css, uri)

def add_tailwind(app, cfg, css, uri):
    _add(app, cfg, css, uri)

def tailwind_compile(outpath, cfg, css):
    cli_path = _cached_download_tailwind_cli("latest")
    subprocess.run([cli_path, "-c", cfg, "-i", css, "-o", outpath])

def _add(app, cfg, css, uri):
    @app.on_event("startup")
    async def startup_event():
        outpath = Path(app.static_dir) / uri.lstrip("/")
        tailwind_compile(outpath, cfg, css)

    @app.get(uri)
    async def get_tailwind_css():
        outpath = Path(app.static_dir) / uri.lstrip("/")
        return await app.send_static_file(outpath)

def _cached_download_tailwind_cli(version):
    cache_dir = Path(os.getenv("CACHE_DIR", ".cache"))
    cache_dir.mkdir(parents=True, exist_ok=True)
    cli_path = cache_dir / f"tailwindcss-{version}"
    if not cli_path.exists():
        url = _get_download_url(version)
        subprocess.run(["curl", "-L", url, "-o", cli_path])
        cli_path.chmod(0o755)
    return cli_path

def _get_download_url(version):
    os_name = os.name
    arch = os.uname().machine
    return f"https://github.com/tailwindlabs/tailwindcss/releases/download/v{version}/tailwindcss-{os_name}-{arch}"