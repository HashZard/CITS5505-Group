from functools import wraps

from flask import session, redirect


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = session.get('user_id')
        if not user_id:
            return redirect('/pages/auth/login.html')  # 跳转登录页
        return f(*args, **kwargs)  # ✅ 不改动参数
    return decorated_function