from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
import traceback

app = Flask(__name__)
app.secret_key = "stupify_secret_key_2024"

# Debug: Log all requests
@app.before_request
def debug_request():
    print(f"🔍 REQUEST: {request.method} {request.path}")

# ─────────────────────────────────────────────
#  DATABASE CONNECTION
#  Update these credentials to match your setup
# ─────────────────────────────────────────────
DB_CONFIG = {
    "host":     "localhost",
    "user":     "root",          # your MySQL username
    "password": "Ijcrs@123",  # your MySQL password
    "database": "stupify"     # your database name
}

# ─────────────────────────────────────────────
#  ROLE MAPPING
# ─────────────────────────────────────────────
ROLES = {
    "admin": {"username": "admin_2", "password": "admin_pass123"},
    "manager": {"username": "database_manager", "password": "manager_pass_123"},
    "analyst": {"username": "analyst", "password": "analyst_pass_123"}
}

def get_db():
    """Connect using root credentials"""
    return mysql.connector.connect(**DB_CONFIG)

def get_db_with_user(username, password):
    """Connect to MySQL with specific user credentials"""
    return mysql.connector.connect(
        host="localhost",
        user=username,
        password=password,
        database="stupify"
    )

def get_db():
    """Connect to MySQL with root credentials (for public pages)"""
    return mysql.connector.connect(**DB_CONFIG)


# ─────────────────────────────────────────────
#  ROUTES
# ─────────────────────────────────────────────

@app.route("/login", methods=["GET", "POST"])
def login():
    error = ""
    if request.method == "POST":
        role = request.form.get("role", "").strip()
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if not all([role, username, password]):
            error = "All fields are required."
        elif role not in ROLES:
            error = "Invalid role selected."
        else:
            try:
                # Verify credentials
                db = get_db_with_user(username, password)
                cursor = db.cursor(buffered=True)
                cursor.execute("SELECT 1")  # Test query
                result = cursor.fetchall()
                cursor.close()
                db.close()

                # Store in session
                session["username"] = username
                session["role"] = role
                session["password"] = password
                return redirect(url_for("home"))

            except mysql.connector.Error as e:
                error = f"Login failed: Invalid username or password"
                print(f"❌ Login error: {e}")
            except Exception as e:
                error = f"Connection error: {str(e)}"
                print(f"❌ Login error: {e}")

    return render_template("login.html", error=error, role=None, username=None, logged_in=False, roles=ROLES)


@app.route("/")
@app.route("/home.html")
def home():
    # Require login to access home
    if "username" not in session:
        return redirect(url_for("login"))
    
    # Get list of tables
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'stupify'")
        tables = [row[0] for row in cursor.fetchall()]
        cursor.close()
        db.close()
    except:
        tables = []
    
    print(f"✓ HOME PAGE LOADED - logged_in: {'username' in session}")
    return render_template("home.html", role=session.get("role"), username=session.get("username"), logged_in="username" in session, tables=tables)


@app.route("/records.html")
def records():
    # Require login to view records
    if "username" not in session:
        return redirect(url_for("login"))
    
    try:
        db = get_db()
        cursor = db.cursor()

        # Get list of tables
        cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'stupify' ORDER BY TABLE_NAME")
        tables = [row[0] for row in cursor.fetchall()]
        
        # Get selected table from query parameter (default to product)
        selected_table = request.args.get("table", "product").lower()
        print(f"🔍 RECORDS PAGE - Query param table: {request.args.get('table')} | Selected: {selected_table}")
        
        # Validate table name to prevent SQL injection
        if selected_table not in tables:
            print(f"⚠️  Invalid table {selected_table}, falling back to product")
            selected_table = "product"
        
        print(f"✓ Tables found: {tables}")
        print(f"✓ Viewing table: {selected_table}")

        # Get columns for the selected table
        cursor.execute(f"DESCRIBE {selected_table}")
        columns = [row[0] for row in cursor.fetchall()]
        
        # Get search term
        search = request.args.get("search", "").strip()
        
        # Get data from selected table
        if search and len(columns) > 1:
            # Search in second column (first is usually ID)
            cursor.execute(f"SELECT * FROM {selected_table} WHERE {columns[1]} LIKE %s LIMIT 100", (f"%{search}%",))
        else:
            cursor.execute(f"SELECT * FROM {selected_table} LIMIT 100")
        
        rows = cursor.fetchall()
        
        cursor.close()
        db.close()
        
        return render_template("records.html", 
                             products=rows, 
                             columns=columns,
                             selected_table=selected_table,
                             tables=tables,
                             search=search,
                             role=session.get("role"), 
                             username=session.get("username"), 
                             logged_in="username" in session)
    
    except Exception as e:
        print(f"\n\n❌ ERROR in /records.html: {e}")
        traceback.print_exc()
        return f"<h1>Database Error</h1><p style='color:red;'><strong>{str(e)}</strong></p><p>Check your terminal for details.</p>", 500


@app.route("/add.html", methods=["GET", "POST"])
def add_product():
    # REQUIRE LOGIN only when accessing Add Product page
    if "username" not in session:
        return redirect(url_for("login"))
    
    # Get list of tables
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'stupify'")
        tables = [row[0] for row in cursor.fetchall()]
        cursor.close()
        db.close()
    except:
        tables = []
    
    # Only staff and admin can add products
    if session.get("role") == "analyst":
        return render_template("add.html", 
                             error="Analysts cannot add products (read-only access).", 
                             message="",
                             role=session.get("role"),
                             username=session.get("username"),
                             logged_in=True,
                             tables=tables)
    
    message = ""
    error = ""

    if request.method == "POST":
        try:
            name     = request.form.get("name", "").strip()
            price    = request.form.get("price", "").strip()
            category = request.form.get("category", "").strip()
            stocks   = request.form.get("stocks", "").strip()

            if not all([name, price, category, stocks]):
                error = "All fields are required."
            else:
                db = get_db_with_user(session["username"], session["password"])
                cursor = db.cursor(buffered=True)
                cursor.execute(
                    "INSERT INTO PRODUCT (product_name, PRICE, CATEGORY_ID, STOCKS) VALUES (%s, %s, %s, %s)",
                    (name, float(price), int(category), int(stocks))
                )
                db.commit()
                cursor.close()
                db.close()
                message = f'Product "{name}" added successfully!'
                print(f"✓ Product added by {session['username']} ({session['role']}): {name}")
        except Exception as e:
            print(f"\n\n❌ ERROR in /add.html: {e}")
            traceback.print_exc()
            error = f"Database error: {str(e)}"

    return render_template("add.html", message=message, error=error, role=session.get("role"), username=session.get("username"), logged_in=True, tables=tables)


@app.route("/delete", methods=["POST"])
def delete_row():
    if "username" not in session:
        return {"error": "Not logged in"}, 401
    
    # Only admin and manager can delete
    if session.get("role") == "analyst":
        return {"error": "Analysts cannot delete records (read-only access)"}, 403
    
    try:
        table = request.form.get("table", "").lower()
        row_id = request.form.get("id", "")
        
        # Basic validation
        if not table or not row_id:
            return {"error": "Missing parameters"}, 400
        
        db = get_db_with_user(session["username"], session["password"])
        cursor = db.cursor(buffered=True)
        
        # Get the primary key column name (usually tablename_ID)
        cursor.execute(f"DESCRIBE {table}")
        columns = cursor.fetchall()
        pk_column = columns[0][0]  # First column is usually PK
        
        # Delete the row
        cursor.execute(f"DELETE FROM {table} WHERE {pk_column} = %s", (row_id,))
        db.commit()
        cursor.close()
        db.close()
        
        print(f"✓ Row {row_id} deleted from {table} by {session['username']}")
        return {"success": True, "message": f"Row deleted successfully"}, 200
    except Exception as e:
        print(f"❌ Delete error: {e}")
        return {"error": str(e)}, 500


@app.route("/edit-row", methods=["GET"])
def edit_row_page():
    if "username" not in session:
        return redirect(url_for("login"))
    
    if session.get("role") == "analyst":
        return {"error": "Read-only access"}, 403
    
    try:
        table = request.args.get("table", "").lower()
        row_id = request.args.get("id", "")
        
        db = get_db()
        cursor = db.cursor()
        
        # Get columns
        cursor.execute(f"DESCRIBE {table}")
        columns = [row[0] for row in cursor.fetchall()]
        
        # Get row data
        pk_column = columns[0]
        cursor.execute(f"SELECT * FROM {table} WHERE {pk_column} = %s", (row_id,))
        row = cursor.fetchone()
        
        cursor.close()
        db.close()
        
        if not row:
            return {"error": "Row not found"}, 404
        
        # Create dict of column names to values
        row_data = {columns[i]: row[i] for i in range(len(columns))}
        
        return {
            "success": True,
            "columns": columns,
            "data": row_data,
            "pk_column": pk_column
        }, 200
    except Exception as e:
        print(f"❌ Edit error: {e}")
        return {"error": str(e)}, 500

@app.route("/update", methods=["POST"])
def update_row():
    if "username" not in session:
        return {"error": "Not logged in"}, 401
    
    # Only admin and manager can update
    if session.get("role") == "analyst":
        return {"error": "Analysts cannot update records (read-only access)"}, 403
    
    try:
        table = request.form.get("table", "").lower()
        row_id = request.form.get("row_id", "")
        pk_column = request.form.get("pk_column", "")
        
        if not all([table, row_id, pk_column]):
            return {"error": "Missing parameters"}, 400
        
        db = get_db_with_user(session["username"], session["password"])
        cursor = db.cursor(buffered=True)
        
        # Get all form fields except table and row_id
        updates = {}
        for key, value in request.form.items():
            if key not in ['table', 'row_id', 'pk_column'] and value:
                updates[key] = value
        
        if not updates:
            return {"error": "No fields to update"}, 400
        
        # Build UPDATE query
        set_clause = ", ".join([f"{col} = %s" for col in updates.keys()])
        values = list(updates.values()) + [row_id]
        
        cursor.execute(f"UPDATE {table} SET {set_clause} WHERE {pk_column} = %s", values)
        db.commit()
        cursor.close()
        db.close()
        
        print(f"✓ Row {row_id} updated in {table} by {session['username']}")
        return {"success": True, "message": f"Record updated successfully"}, 200
    except Exception as e:
        print(f"❌ Update error: {e}")
        traceback.print_exc()
        return {"error": str(e)}, 500


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/about.html")
def readme():
    # Require login to view about
    if "username" not in session:
        return redirect(url_for("login"))
    
    # Get list of tables
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'stupify'")
        tables = [row[0] for row in cursor.fetchall()]
        cursor.close()
        db.close()
    except:
        tables = []
    
    return render_template("about.html", role=session.get("role"), username=session.get("username"), logged_in="username" in session, tables=tables)


# ─────────────────────────────────────────────
#  RUN
# ─────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True)