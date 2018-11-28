from werkzeug.exceptions import HTTPException

from app import create_app
from app.libs.error import APIException
from app.libs.error_code import ServerError

app = create_app()


@app.errorhandler(Exception)
def framework_error(e):
    if isinstance(e, APIException):
        return e
    if isinstance(e, HTTPException):
        return APIException(msg=e.description, code=e.code, error_code=1007)
    else:
        # log 最好先记录日志
        if not app.config['DEBUG']:
            return ServerError()
        else:
            raise e


if __name__ == '__main__':

    app.run(debug=True)