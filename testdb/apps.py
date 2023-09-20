from django.apps import AppConfig


class TestdbConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'testdb'
    # name = 'full.python.path.to.your.app.testdb'
    # label = 'my.testdb'
    
