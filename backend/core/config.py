import os
import sys

def get_app_data_dir():
    custom_dir = os.environ.get("OMNIVOICE_DATA_DIR")
    if custom_dir:
        return custom_dir
    
    path = os.path.abspath(__file__)
    
    for _ in range(4):
        path = os.path.dirname(path)
        
    return path


def _ensure_short_hf_cache_on_windows():
    if sys.platform != "win32":
        return
    if os.environ.get("OMNIVOICE_CACHE_DIR") or os.environ.get("HF_HOME") or os.environ.get("HF_HUB_CACHE"):
        return
    
    data_dir = get_app_data_dir()
    short_cache = os.path.join(data_dir, "hf_cache")
    os.makedirs(short_cache, exist_ok=True)
    os.environ["HF_HOME"] = short_cache
    os.environ["HF_HUB_CACHE"] = short_cache

_ensure_short_hf_cache_on_windows()


DATA_DIR = get_app_data_dir()
VOICES_DIR = os.path.join(DATA_DIR, "voices")
OUTPUTS_DIR = os.path.join(DATA_DIR, "outputs")
DUB_DIR = os.path.join(DATA_DIR, "dub_jobs")
DB_PATH = os.path.join(DATA_DIR, "omnivoice.db")
PREVIEW_DIR = os.path.join(DATA_DIR, "preview")
CRASH_LOG_PATH = os.path.join(DATA_DIR, "crash_log.txt")
LOG_PATH = os.path.join(DATA_DIR, "omnivoice.log")

IDLE_TIMEOUT_SECONDS = int(os.environ.get("OMNIVOICE_IDLE_TIMEOUT", "900"))
CPU_POOL_WORKERS = int(os.environ.get("OMNIVOICE_CPU_POOL", "0")) or min(8, (os.cpu_count() or 4))

def ensure_dirs():
    for d in [DATA_DIR, VOICES_DIR, OUTPUTS_DIR, DUB_DIR, PREVIEW_DIR]:
        os.makedirs(d, exist_ok=True)

ensure_dirs()

if sys.platform != "win32":
    for _fpath in ["/opt/homebrew/bin", "/usr/local/bin"]:
        if _fpath not in os.environ.get("PATH", "") and os.path.exists(_fpath):
            os.environ["PATH"] = _fpath + os.pathsep + os.environ.get("PATH", "")