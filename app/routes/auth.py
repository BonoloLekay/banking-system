from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from app.database import get_connection
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.user import User

auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth"
)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        first_name = request.form.get("first_name", "").strip()
        last_name = request.form.get("last_name", "").strip()
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        phone = request.form.get("phone", "").strip()
        id_number = request.form.get("id_number", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not all([
            first_name,
            last_name,
            username,
            email,
            id_number,
            password,
            confirm_password
        ]):
            flash("Please complete all required fields.", "danger")
            return render_template("auth/register.html")

        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return render_template("auth/register.html")

        if len(password) < 8:
            flash("Password must be at least 8 characters long.", "danger")
            return render_template("auth/register.html")

        connection = get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(
                """
                SELECT user_id
                FROM users
                WHERE username = %s OR email = %s
                """,
                (username, email)
            )

            if cursor.fetchone():
                flash("Username or email already exists.", "danger")
                return render_template("auth/register.html")

            cursor.execute(
                """
                SELECT customer_id
                FROM customers
                WHERE id_number = %s
                """,
                (id_number,)
            )

            if cursor.fetchone():
                flash("A customer with this ID number already exists.", "danger")
                return render_template("auth/register.html")

            cursor.execute(
                """
                INSERT INTO customers (
                    first_name,
                    last_name,
                    email,
                    phone,
                    id_number
                )
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    first_name,
                    last_name,
                    email,
                    phone,
                    id_number
                )
            )

            customer_id = cursor.lastrowid

            password_hash = generate_password_hash(password)

            cursor.execute(
                """
                INSERT INTO users (
                    customer_id,
                    username,
                    email,
                    password_hash,
                    role
                )
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    customer_id,
                    username,
                    email,
                    password_hash,
                    "CUSTOMER"
                )
            )

            connection.commit()

            flash(
                "Registration successful. You can now log in.",
                "success"
            )

            return redirect(url_for("auth.login"))

        except Exception as error:
            connection.rollback()
            print(error)

            flash(
                "Unable to create your account.",
                "danger"
            )

        finally:
            cursor.close()
            connection.close()

    return render_template("auth/register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("auth.dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username or not password:
            flash(
                "Please enter your username and password.",
                "danger"
            )
            return render_template("auth/login.html")

        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        try:
            cursor.execute(
                """
                SELECT
                    user_id,
                    customer_id,
                    username,
                    email,
                    password_hash,
                    role,
                    is_active
                FROM users
                WHERE username = %s
                """,
                (username,)
            )

            data = cursor.fetchone()

            if not data or not check_password_hash(
                data["password_hash"],
                password
            ):
                flash(
                    "Invalid username or password.",
                    "danger"
                )
                return render_template("auth/login.html")

            if not data["is_active"]:
                flash(
                    "This account is inactive.",
                    "danger"
                )
                return render_template("auth/login.html")

            user = User(
                user_id=data["user_id"],
                customer_id=data["customer_id"],
                username=data["username"],
                email=data["email"],
                role=data["role"],
                is_active=data["is_active"]
            )

            login_user(user)

            return redirect(url_for("auth.dashboard"))

        finally:
            cursor.close()
            connection.close()

    return render_template("auth/login.html")


@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()

    flash(
        "You have been logged out.",
        "success"
    )

    return redirect(url_for("auth.login"))


@auth_bp.route("/dashboard")
@login_required
def dashboard():
    return render_template(
        "customer/dashboard.html"
    )