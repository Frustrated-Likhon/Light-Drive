from flask import Flask, request, render_template, send_from_directory, redirect, url_for, session
import os
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  


BASE_DIRS = {
    "C": "C:/",
    "D": "D:/", 
    "E": "E:/"
}


USERS = {
    "admin": "password123",  # username: password
    "user": "user123"
}

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def get_files(path):
    """Returns a list of visible files and folders."""
    items = []
    try:
        for item in os.listdir(path):
            full_path = os.path.join(path, item)

           
            if (item.startswith(".") or item.startswith("$") or 
                "desktop.ini" in item.lower() or 
                "System Volume Information" in item or
                item.startswith("~")):
                continue

            
            try:
                size = os.path.getsize(full_path) if os.path.isfile(full_path) else 0
                modified = os.path.getmtime(full_path)
            except:
                size = 0
                modified = 0

            
            if os.path.isdir(full_path):
                file_type = "folder"
                icon = "📁"
            else:
                ext = item.split(".")[-1].lower() if "." in item else ""
                if ext in ["mp4", "mkv", "avi", "mov", "wmv"]:
                    file_type = "video"
                    icon = "🎬"
                elif ext in ["mp3", "m4a", "wav", "flac", "aac"]:
                    file_type = "audio" 
                    icon = "🎵"
                elif ext in ["jpg", "jpeg", "png", "gif", "bmp", "webp"]:
                    file_type = "image"
                    icon = "🖼️"
                elif ext in ["pdf", "doc", "docx", "txt", "rtf"]:
                    file_type = "document"
                    icon = "📄"
                elif ext in ["zip", "rar", "7z", "tar", "gz"]:
                    file_type = "archive"
                    icon = "📦"
                else:
                    file_type = "file"
                    icon = "📄"

            items.append({
                "name": item, 
                "type": file_type,
                "icon": icon,
                "size": size,
                "modified": modified,
                "path": full_path
            })
        
        
        items.sort(key=lambda x: (not os.path.isdir(x['path']), x['name'].lower()))
        
    except PermissionError:
        print(f"Permission denied: {path}")
    except Exception as e:
        print(f"Error reading {path}: {e}")
    
    return items

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username in USERS and USERS[username] == password:
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error="Invalid credentials")
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/')
@login_required
def home():
    """Home page with drive selection."""
    return render_template("home.html", drives=BASE_DIRS)

@app.route('/list')
@login_required
def list_files():
    """Lists files in a given directory."""
    path = request.args.get('path')

    if not path:
        return "No path provided", 400

    if not any(path.startswith(base) for base in BASE_DIRS.values()):
        return "Access Denied", 403

    if not os.path.exists(path):
        return "Path Not Found", 404

    files = get_files(path)
    parent_dir = os.path.dirname(path) if path not in BASE_DIRS.values() else None
    
    return render_template("index.html", 
                         files=files, 
                         path=path,
                         parent_dir=parent_dir,
                         base_dirs=BASE_DIRS)

@app.route('/file/<path:filename>')
@login_required
def serve_file(filename):
    """Serves a file for playback or viewing."""
    directory = os.path.dirname(filename)
    file_name = os.path.basename(filename)
    return send_from_directory(directory, file_name)

@app.route('/view')
@login_required
def view_file():
    """Displays a media file for playback."""
    path = request.args.get('path')

    if not path or not os.path.exists(path):
        return "File Not Found", 404

    return render_template("player.html", file=path)

@app.route('/image-viewer')
@login_required
def image_viewer():
    """Displays an image viewer with Next/Previous functionality."""
    path = request.args.get('path')
    if not path or not os.path.exists(path):
        return "Folder Not Found", 404

    images = [f for f in os.listdir(path) if f.split('.')[-1].lower() in ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp']]
    image = request.args.get('image', images[0] if images else None)
    return render_template("image_viewer.html", path=path, images=images, image=image)

@app.route('/image')
@login_required
def view_image():
    """Display a specific image from the folder."""
    image_path = request.args.get('image')
    directory = os.path.dirname(image_path)
    file_name = os.path.basename(image_path)
    return send_from_directory(directory, file_name)

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=80, debug=True)

