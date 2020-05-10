 #Helper method that implements the logic to look up an application.
 def get_app(self, reference_app=None):
        if reference_app is not None:
            return reference_app

        if self.app is not None:
            return self.app

        if current_app:
            return current_app._get_current_object()

        raise RuntimeError(
            'No application found.See'
            ' http://flask-sqlalchemy.pocoo.org/contexts/.'
        )