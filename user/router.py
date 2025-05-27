class AuthRouter:
    """
    A router to control all database operations on models in the
    users application.
    """

    route_app_labels = {'user','admin','contenttypes','sessions', 'auth','messages'}

    def db_for_read(self, model, **hints):
        """
        Attempts to read users models go to users_db.
        """
        if model._meta.app_label in self.route_app_labels:
            return 'users'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write users models go to users_db.
        """
        if model._meta.app_label in self.route_app_labels:
            return 'users'
        return None
    def allow_relation(self, obj1, obj2, **hints):
        if (
            obj1._meta.app_label in self.route_app_labels or
            obj2._meta.app_label in self.route_app_labels  
        ):
            return True
        return None
    
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Ensure that the users app only appears in the 'users_db'
        database.
        """
        if app_label in self.route_app_labels:
            return db == 'users'
        return None