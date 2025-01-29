from __future__ import annotations

from dynaconf import Dynaconf

APP_SETTINGS = Dynaconf(
    environments=True,
    envvar_prefix="APP",
    settings_files=["settings.toml", ".secrets.toml"]
)
