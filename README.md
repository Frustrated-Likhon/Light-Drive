"
# 💻 LightDrive  

**LightDrive** is a lightweight **Flask-based remote file browser and media server** that allows users to **browse, view, and play files** on your computer through a web interface with login protection.  

Designed for:  
- 💻 Users who want a **secure, local file browsing solution**  
- ⚡ Quickly access files and media on your PC  
- 🛠️ Works on Windows; minor modifications needed for Linux/macOS  

## 🚀 Features  
- 🔑 User login with session management  
- 📂 Browse drives and directories securely  
- 🎬 Play video and audio files in-browser  
- 🖼️ Image viewer with next/previous functionality  
- 📄 View documents (PDF, TXT, DOCX)  
- Supports multiple drives (C, D, E)  

## 🛠️ Tech Stack  
- **Backend:** Python (Flask)  
- **Frontend:** HTML, CSS, JavaScript  
- **Other:** Jinja2 templates, OS filesystem integration  

## 📂 Project Structure  
```
LightDrive/
│── app.py                # Flask app
│── templates/            # HTML templates
│── static/               # CSS, JS, icons
│── README.md
```

## ⚙️ Installation  

1. Clone this repository:  
```bash
git clone https://github.com/yourusername/LightDrive.git
cd LightDrive
```

2. Install dependencies:  
```bash
pip install flask
```

3. Run the app:  
```bash
python app.py
```

4. Open in your browser:  
```
http://127.0.0.1
```

5. To access from other devices, replace `127.0.0.1` with your **PC’s IP address**:  
```
http://YOUR_PC_IP
```

6. For **Linux/macOS**, update the `BASE_DIRS` paths in `app.py` accordingly:  
```python
BASE_DIRS = {
    "Root": "/", 
    "Home": "/home/username"
}
```

---

## 🎮 Usage  

1. Log in using one of the predefined users in `app.py`  
2. Browse drives and folders  
3. Click on files to view/play them  
4. Use the **image viewer** to navigate images in a folder
5. Use the **media player** to view your media from the browser 
   no need to download the files to view them  

---

## 🤝 Contributing  
Pull requests are welcome! For major changes, please open an issue first to discuss what you’d like to change.  


