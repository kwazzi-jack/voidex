from pathlib import Path
from appdirs import AppDirs

_app_dirs = AppDirs(appname="voidex")

CACHE_DIR = Path(_app_dirs.user_cache_dir)
CONFIG_DIR = Path(_app_dirs.user_config_dir)
DATA_DIR = Path(_app_dirs.user_data_dir)
LOG_DIR = Path(_app_dirs.user_log_dir)
STATE_DIR = Path(_app_dirs.user_state_dir)
APP_DIR = Path(__file__).parent


# Resource paths
STREAMLIT_CSS_PATH = APP_DIR / "app.css"


if __name__ == "__main__":
    print(f"{CACHE_DIR=}")
    print(f"{CONFIG_DIR=}")
    print(f"{DATA_DIR=}")
    print(f"{LOG_DIR=}")
    print(f"{STATE_DIR=}")
    print(f"{APP_DIR=}")
    print(f"{STREAMLIT_CSS_PATH=}")
