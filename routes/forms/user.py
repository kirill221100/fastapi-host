from fastapi import Request


class UserForm:

    def __init__(self, request: Request):
        self.request = request
        self.username: str = ''
        self.password: str = ''

    async def load_data(self):
        form = await self.request.form()
        self.username = form.get('username')
        self.password = form.get('password')
