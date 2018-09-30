import logging.config
import os
import yaml
from app import create_app
from app.libs.error import APIException
from werkzeug.exceptions import HTTPException
from app.libs.error import ServerError
from app.config.args import get_args

app = create_app()


@app.errorhandler(Exception)
def framework_error(e):
    if isinstance(e, APIException):
        return e
    elif isinstance(e, HTTPException):
        code = e.code
        msg = e.description
        error_code = 1007
        return APIException(msg, code, error_code)
    else:
        # log记录
        logger = logging.getLogger('error_log')
        logger.exception(e)
        if not app.config['DEBUG']:
            return ServerError()
        else:
            raise e


def setup_logging(default_path="logging.yaml", default_level=logging.INFO):
    path = default_path
    if os.path.exists(path):
        with open(path, "r") as f:
            logging.config.dictConfig(yaml.load(f))
    else:
        logging.basicConfig(level=default_level)


if __name__ == '__main__':
    setup_logging()
    app.config.from_object(get_args())  # 在create_app中调用，会和pytest命令行冲突
    app.run(host=app.config['HOST'], port=app.config['PORT'])
