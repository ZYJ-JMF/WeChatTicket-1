from codex.baseview import APIView
from codex.baseerror import ValidateError, PrivilegeError, DatabaseError
from django.contrib import auth


class AdminLogin(APIView):

    def validate_super_user(self):
        username = self.input['username']
        password = self.input['password']
        user = auth.authenticate(username=username, password=password)
        if not user:
            raise ValidateError(self.input)
        if not user.is_superuser:
            raise PrivilegeError(self.input)
        try:
            auth.login(self.request, user)
        except:
            raise DatabaseError(self.input)

    def get(self):
        if not self.request.user.is_superuser:
            raise PrivilegeError(self.input)

    def post(self):
        self.check_input('username', 'password')
        self.validate_super_user()


class AdminLogout(APIView):

    def post(self):
        if not self.request.user.is_superuser:
            raise ValidateError(self.input)
        try:
            auth.logout(self.request)
        except:
            raise DatabaseError(self.input)