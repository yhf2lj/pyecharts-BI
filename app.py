from flask_login import LoginManager, login_required, login_user, logout_user
from flask import Flask, render_template, redirect, url_for, request

from user import User, LoginForm, get_user
from chart import bar_base, gauge_base
import warnings

warnings.filterwarnings("ignore")
app = Flask(__name__, static_folder="templates")
app.secret_key = 'pyecharts-flask'  # 设置表单交互密钥

login_manager = LoginManager()  # 实例化登录管理对象
login_manager.init_app(app)  # 初始化应用
login_manager.login_view = 'login'  # 设置用户登录视图函数 endpoint


@login_manager.user_loader  # 定义获取登录用户的方法
def load_user(user_id):
    return User.get(user_id)


@app.route("/")
@login_required
def index():
    return render_template("index.html")


@app.route('/login/', methods=('GET', 'POST'))  # 登录
def login():
    form = LoginForm()
    emsg = None
    if form.validate_on_submit():
        user_name = form.username.data
        password = form.password.data
        user_info = get_user(user_name)  # 从用户数据中查找用户记录
        if user_info is None:
            emsg = "用户名或密码密码有误"
        else:
            user = User(user_info)  # 创建用户实体
            if user.verify_password(password):  # 校验密码
                login_user(user)  # 创建用户 Session
                return redirect(request.args.get('next') or url_for('index'))
            else:
                emsg = "用户名或密码密码有误"
    return render_template('login.html', form=form, emsg=emsg)


@app.route('/logout')  # 登出跳转到登录页面
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/barChart", methods=['GET', "POST"])
def get_bar_chart():
    return bar_base().dump_options_with_quotes()


@app.route("/gaugeChart", methods=["POST"])
def get_gauge_chart():
    y = float(request.form['value'])
    print(request.form.getlist('select2'))
    return gauge_base(y).dump_options_with_quotes()


if __name__ == "__main__":
    app.run(debug=True)
