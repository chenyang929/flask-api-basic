import argparse


def get_args():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--HOST", default="127.0.0.1", help="Host IP")
    arg_parser.add_argument("--PORT", default=5000, help="Host port", type=int)
    arg_parser.add_argument("--DEBUG", default=True, help="DEBUG ENABLE", type=str2bool)
    arg_parser.add_argument("--TOKEN_EXPIRATION", default=3600 * 2, help="TOKEN_EXPIRATION")
    arg_parser.add_argument("--SECRET_KEY", default="hard to guess", help="SECRET_KEY")  # os.urandom(24)
    arg_parser.add_argument("--MONGO_URI", default="mongodb://coder:coder@localhost:27017/test", help="Mongo uri for storing datasets")
    arg_parser.add_argument("--MONGO_DB", default="test", help="Mongo Database Name")
    return arg_parser.parse_args()


# boolean类型的参数不能自动转换参数类型，命令行任何值都会变成True
def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Unsupported value encountered.')


