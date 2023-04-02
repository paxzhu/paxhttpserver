from flask import Flask, render_template, send_file, redirect
import os

app = Flask(__name__)

def handle_path(path: str) -> str:
    if path == './':
        return path
    stack = []
    path = path.split('/')
    # print(path)
    for sub in path:
        if sub == '..':
            if stack:
                stack.pop()
        elif sub != '.' and sub != '':
            stack.append(sub)
    
    path = '/'.join(stack)
    if os.path.isdir(path):
        path += '/'
    # print(path)
    return path

@app.route('/', defaults = {'path':'./'})
@app.route('/<path:path>')
def direct(path):
    path = handle_path(path)
    if path.endswith('/'):
        if not os.path.isdir(path):
            return render_template('404.html'), 404
        subs = os.listdir(path)
        # print(subs)         
        if 'index.html' in subs:
            with open(path+'index.html') as page:
                contents = page.read()
            return contents
        hrefs = [f+'/' if os.path.isdir(path+f) else f for f in subs]
        cur_dir = '/'
        if path != './':
            cur_dir += path
        return render_template("directfor.html", cur_dir = cur_dir, subs = hrefs)
        
    if os.path.isdir(path):
        return redirect(path.split('/')[-1]+'/')
    
    if not os.path.isfile(path):
        return render_template('404.html'), 404
    if path.endswith('html'):
        with open(path) as f:
            contents = f.read()
        return contents
    return send_file(path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug = True, port=5000)