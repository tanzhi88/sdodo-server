from app.libs.redprint import Redprint
from app.libs.token_auth import auth

api = Redprint('ad')


@api.route('')
@auth.login_required
def create_ad():
    save_path = ''
