from flask import Flask, render_template, send_file, redirect
import os

app = Flask(__name__)

@app.route('/', defaults = {'path':'./'})
@app.route('/<path:path>')
def direct(path):
    if path.endswith('/'):
        if os.path.isdir(path):
            dirs = os.listdir(path)
            print(dirs)                 
            hrefs = []
            for f in dirs:
                if f == 'index.html':
                    with open(path+f) as page:
                        contents = page.read()
                    return contents
                if os.path.isdir(path+f):
                    hrefs.append(f+'/')
                else:
                    hrefs.append(f)
            return render_template("directfor.html", dirs = hrefs)
        return render_template('404.html'), 404
    if os.path.isdir(path):
        return redirect(path.split('/')[-1]+'/')
    if os.path.isfile(path):
        if path.endswith('html'):
            with open(path) as f:
                contents = f.read()
            return contents
        return send_file(path, as_attachment=True)
    return render_template('404.html'), 404

  
if __name__ == "__main__":
    app.run(debug = True, port=5000)