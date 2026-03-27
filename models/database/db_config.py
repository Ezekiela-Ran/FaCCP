import os
import json
from pathlib import Path

from utils.path_utils import get_app_data_dir


DEFAULT_DB_NAME = 'invoicing'
DEFAULT_DB_ENGINE = 'sqlite'
DEFAULT_DB_HOST = 'localhost'
DEFAULT_DB_PORT = 3306
DEFAULT_DB_USER = 'sam'
DEFAULT_DB_PASSWORD = ''


def _config_file_candidates() -> list[Path]:
    custom_path = os.getenv('LFCA_DB_CONFIG', '').strip()
    candidates = []
    if custom_path:
        candidates.append(Path(os.path.expandvars(custom_path)).expanduser())
    candidates.append(get_app_data_dir('LFCA') / 'database.json')
    candidates.append(Path.cwd() / 'database.json')
    return candidates


def _default_sqlite_path() -> str:
    return str(get_app_data_dir('LFCA') / 'lfca.db')


def _write_default_config_template(config_path: Path):
    config_path.parent.mkdir(parents=True, exist_ok=True)
    if config_path.exists():
        return

    config_path.write_text(
        json.dumps(
            {
                'engine': DEFAULT_DB_ENGINE,
                'sqlite_path': _default_sqlite_path(),
                'mysql': {
                    'host': DEFAULT_DB_HOST,
                    'port': DEFAULT_DB_PORT,
                    'user': DEFAULT_DB_USER,
                    'password': DEFAULT_DB_PASSWORD,
                    'database': DEFAULT_DB_NAME,
                },
            },
            indent=2,
        ),
        encoding='utf-8',
    )


def _load_file_config() -> tuple[dict, Path]:
    candidates = _config_file_candidates()
    primary_path = get_app_data_dir('LFCA') / 'database.json'
    _write_default_config_template(primary_path)

    for candidate in candidates:
        if not candidate.exists():
            continue
        try:
            loaded = json.loads(candidate.read_text(encoding='utf-8'))
        except (json.JSONDecodeError, OSError):
            continue
        if isinstance(loaded, dict):
            return loaded, candidate
    return {}, primary_path


FILE_CONFIG, DB_CONFIG_FILE = _load_file_config()


def _file_mysql_config() -> dict:
    mysql_config = FILE_CONFIG.get('mysql', {}) if isinstance(FILE_CONFIG.get('mysql', {}), dict) else {}
    return mysql_config


def _pick_setting(env_key: str, file_value, default_value):
    env_value = os.getenv(env_key)
    if env_value is not None and str(env_value).strip() != '':
        return env_value
    if file_value is not None and str(file_value).strip() != '':
        return file_value
    return default_value


def _expand_path(value: str) -> str:
    return os.path.expandvars(str(value or '')).strip()


def _get_port() -> int:
    raw_port = _pick_setting('DB_PORT', _file_mysql_config().get('port'), DEFAULT_DB_PORT)
    try:
        return int(raw_port)
    except ValueError:
        return DEFAULT_DB_PORT


DB_NAME = str(_pick_setting('DB_NAME', _file_mysql_config().get('database'), DEFAULT_DB_NAME)).strip()
DB_ENGINE = str(_pick_setting('DB_ENGINE', FILE_CONFIG.get('engine'), DEFAULT_DB_ENGINE)).strip().lower()
DB_PATH = _expand_path(_pick_setting('DB_PATH', FILE_CONFIG.get('sqlite_path'), _default_sqlite_path()))


# Configuration de la base de données
DB_CONFIG = {
    'host': str(_pick_setting('DB_HOST', _file_mysql_config().get('host'), DEFAULT_DB_HOST)).strip(),
    'port': _get_port(),
    'user': str(_pick_setting('DB_USER', _file_mysql_config().get('user'), DEFAULT_DB_USER)).strip(),
    'password': str(_pick_setting('DB_PASSWORD', _file_mysql_config().get('password'), DEFAULT_DB_PASSWORD)),
}