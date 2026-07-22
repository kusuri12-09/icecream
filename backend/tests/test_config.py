from app.core.config import Settings


def test_legacy_psycopg2_url_uses_installed_psycopg_driver():
    settings = Settings(database_url="postgresql+psycopg2://user:password@localhost/icecream")

    assert settings.resolved_database_url == "postgresql+psycopg://user:password@localhost/icecream"


def test_postgresql_url_without_driver_uses_installed_psycopg_driver():
    settings = Settings(database_url="postgresql://user:password@localhost/icecream")

    assert settings.resolved_database_url == "postgresql+psycopg://user:password@localhost/icecream"
