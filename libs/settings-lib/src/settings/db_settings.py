from __future__ import annotations

from dynaconf import Dynaconf

## Database settings loaded with dynaconf
DB_SETTINGS: Dynaconf = Dynaconf(
    environments=True,
    envvar_prefix="DB",
    settings_files=["database/settings.toml", "database/.secrets.toml"],
)
