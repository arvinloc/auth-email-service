from bcrypt import checkpw, gensalt, hashpw


class HashHelper(object):

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str):
        # проверка на совпадение паролей
        if checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8')):
            return True
        return False

    @staticmethod
    def get_password_hash(plain_password: str):
        # получение хеша пароля
        return hashpw(
            plain_password.encode('utf-8'),
            gensalt()
        ).decode('utf-8')
