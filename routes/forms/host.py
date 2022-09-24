from fastapi import Request


class HostForm:

    def __init__(self, request: Request):
        self.request = request
        self.site_name: str = ''
        self.url: str = ''
        self.site_content: str = ''
        self.errors = []

    async def load_data(self):
        form = await self.request.form()
        self.site_name = form.get('site-name')
        self.url = form.get('url')
        self.site_content = form.get('site-content')

    async def is_valid(self):
        if ' ' in self.url:
            self.errors.append("Route shouldn't contain spaces")
        elif self.url[0] == '/' or self.url[-1] == '/':
            self.errors.append("Route shouldn't start or end with '/'")
        elif '\\' in self.url:
            self.errors.append("Route shouldn't contain backslashes")
        elif '' in self.url.split('/'):
            self.errors.append("Too much '/'")

        # elif self.url.split('/')[0] in ['create', 'delete_page', 'update_page', 'login', 'register', 'logout']:
        #     self.errors.append('Make another route')
