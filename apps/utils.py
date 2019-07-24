from rest_framework.response import Response


class AfterResponseAction(Response):
    def __init__(self, *args, **kwargs):
        self.after_response_action = kwargs.get('after_response_action', None)
        kwargs.pop('after_response_action')
        super().__init__(*args, **kwargs)

    def close(self):
        super().close()

        if self.status_code == 200 and callable(self.after_response_action):
            self.after_response_action()
