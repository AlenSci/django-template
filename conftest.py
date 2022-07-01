from django.conf import settings


def pytest_configure():
    settings.CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer', #For testing
    },
        }
    settings.TEST_RUNNER = 'djcelery.contrib.test_runner.CeleryTestSuiteRunner'

    if not settings.configured:
        settings.configure(
            INSTALLED_APPS=(
                "django.contrib.auth",
                "django.contrib.contenttypes",
                "django.contrib.sessions",
                "channels",
                "tests",
            ),
            SECRET_KEY="any",
            DATABASES={
                "default": {
                    "ENGINE": "django.db.backends.sqlite3",
                }
            },
            MIDDLEWARE_CLASSES=[],
        )
