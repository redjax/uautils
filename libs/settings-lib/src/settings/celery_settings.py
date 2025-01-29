from __future__ import annotations

from dynaconf import Dynaconf

## Celery settings loaded with dynaconf
CELERY_SETTINGS: Dynaconf = Dynaconf(
    environments=True,
    envvar_prefix="CELERY",
    settings_files=["celery/settings.toml", "celery/.secrets.toml"],
)
