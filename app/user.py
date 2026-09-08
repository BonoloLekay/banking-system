from flask_login import UserMixin


class User(UserMixin):
    def __init__(
        self,
        user_id,
        customer_id,
        username,
        email,
        role,
        is_active=True
    ):
        self.id = user_id
        self.customer_id = customer_id
        self.username = username
        self.email = email
        self.role = role
        self.active = bool(is_active)

    @property
    def is_active(self):
        return self.active