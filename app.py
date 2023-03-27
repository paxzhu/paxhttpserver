from flask import Flask, render_template, send_file
import os

app = Flask(__name__)

@app.route('/', defaults = {'path':'.'})
@app.route('/<path:path>/')
def direct(path):
    if os.path.isdir(path):
        path += '/'
        dirs = os.listdir(path)                 
        navi = []
        for f in dirs:
            if f == 'index.html':
                with open(path+f) as page:
                    contents = page.read()
                return contents
            if os.path.isdir(path+f):
                navi.append(f+'/')
            else:
                navi.append(f)            
        return render_template("directfor.html", dirs = navi)
    elif path.endswith('.html'):
        with open(path) as f:
            contents = f.read()
        return contents
    return send_file(path, as_attachment=True)
    
if __name__ == "__main__":
    app.run(debug = True)