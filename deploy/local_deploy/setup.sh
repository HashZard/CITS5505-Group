#!/bin/bash

# === Define project root ===
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
VENV_PATH="$PROJECT_ROOT/venv"
NGINX_CONF="deploy/local_deploy/nginx.conf"

# === Shutdown previous Flask and Nginx processes ===
function shutdown_services() {
    echo "🧹 Stopping any existing services..."

    # Kill Flask (port 8000)
    FLASK_PIDS=$(lsof -ti tcp:8000)
    if [ -n "$FLASK_PIDS" ]; then
        echo "❌ Killing Flask process(es) on port 8000: $FLASK_PIDS"
        for pid in $FLASK_PIDS; do
            kill -9 "$pid"
        done
    else
        echo "✅ No Flask process found on port 8000"
    fi

    # Kill Nginx (port 3000)
    NGINX_PIDS=$(lsof -ti tcp:3000)
    if [ -n "$NGINX_PIDS" ]; then
        echo "❌ Killing processes on port 3000: $NGINX_PIDS"
        for pid in $NGINX_PIDS; do
            kill -9 "$pid"
        done
    else
        echo "✅ No process using port 3000"
    fi

    # Kill nginx master in this project path
    NGINX_MASTERS=$(ps aux | grep 'nginx: master' | grep "$PROJECT_ROOT" | awk '{print $2}')
    if [ -n "$NGINX_MASTERS" ]; then
        echo "❌ Killing project-specific nginx master(s): $NGINX_MASTERS"
        echo "$NGINX_MASTERS" | xargs kill -9
    else
        echo "✅ No nginx master process found in this project"
    fi

    # Fallback: kill all nginx
    echo "🔪 Killing all nginx-related processes..."
    ps aux | grep '[n]ginx' | awk '{print $2}' | xargs kill -9 2>/dev/null

    sleep 1
}

# === Set up virtual environment ===
function setup_venv() {
    if [ ! -d "$VENV_PATH" ]; then
        echo "🐍 Creating virtual environment..."
        python3 -m venv "$VENV_PATH"
    else
        echo "✅ Virtual environment already exists"
    fi

    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || "$OSTYPE" == "win32" ]]; then
        source "$VENV_PATH/Scripts/activate"
    else
        source "$VENV_PATH/bin/activate"
    fi

    if [ -f "$PROJECT_ROOT/requirements.txt" ]; then
        echo "📦 Installing dependencies..."
        pip install -r "$PROJECT_ROOT/requirements.txt"
    fi
}

# === Set up database using Flask-Migrate ===
function setup_db() {
    echo "🛠️ Setting up the database..."

    export FLASK_APP=backend/app/app.py
    export FLASK_ENV=development
    export PYTHONPATH="$PROJECT_ROOT"

    cd "$PROJECT_ROOT" || exit

    if [ -f "$PROJECT_ROOT/backend/app.db" ]; then
        echo "📦 Existing database found: app.db"
    else
        echo "🆕 Creating new SQLite database..."
    fi

    if [ ! -d "migrations" ]; then
        echo "📁 No migrations folder found. Initializing..."
        flask db init
        flask db migrate -m "Initial migration"
    else
        echo "🔁 Migrations folder found. Auto migrating..."
        flask db migrate -m "Auto migration"
    fi

    flask db upgrade
    echo "✅ Database setup complete."
}

# === Start Flask server ===
function start_flask() {
    echo "🚀 Starting Flask server on port 8000..."
    cd "$PROJECT_ROOT" || exit
    export FLASK_APP=backend/app/app.py
    export FLASK_ENV=development
    export PYTHONPATH="$PROJECT_ROOT"
    flask run --port=8000 &
    sleep 2
}

# === Start Nginx server ===
function start_nginx() {
    echo "🌐 Starting Nginx on port 3000..."
    cd "$PROJECT_ROOT" || exit

    mkdir -p "$PROJECT_ROOT/logs"

    nginx -p "$PROJECT_ROOT/" -c "$NGINX_CONF"
    if [ $? -ne 0 ]; then
        echo "❌ Failed to start Nginx. Aborting setup."
        exit 1
    fi

    sleep 2
}

# === Check if services are running ===
function check_services() {
    echo "🧪 Checking service status..."
    curl -s http://localhost:8000/ >/dev/null && echo "✅ Flask is running" || echo "❌ Flask not responding"
    curl -s http://localhost:3000/ >/dev/null && echo "✅ Nginx is running" || echo "❌ Nginx not responding"
}

# === Open browser to homepage ===
function open_browser() {
    echo "🌍 Opening browser: http://localhost:3000/"
    open "http://localhost:3000/"
}

# === Execute all steps ===
echo "🔧 Initializing local development environment"
shutdown_services
setup_venv
setup_db
start_flask
start_nginx
check_services
open_browser
echo "🎉 All services started successfully!"
