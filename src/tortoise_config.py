try:
    from config import settings
    DATABASE_URL = settings.DATABASE_URL
except ImportError:
    from src.config import settings
    print("ImportError")
    DATABASE_URL = settings.DATABASE_URL

DATABASE_URL = DATABASE_URL.replace('sqlite://', 'sqlite://src/')

TORTOISE_ORM = {
    "connections": {"default": DATABASE_URL},
    "apps": {
        "models": {
            "models": ["db.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}
