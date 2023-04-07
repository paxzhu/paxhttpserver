from flask import Flask, render_template, send_file, redirect
import os

app = Flask(__name__)
def simplify_logic_path(url_path):
    stack = []
    for sub in url_path.split('/'):
        if sub == '..' and stack:
            stack.pop()
        elif sub and sub != '..' and sub != '.': 
            stack.append(sub)
    if url_path.endswith('/'):
        stack.append('')
    return '/'.join(stack)

def path_exists(url_path):
    if url_path.endswith('/') and not os.path.isdir(url_path):
        return False
    if not url_path.endswith('/') and not os.path.isfile(url_path):
        return False
    return True

def preprocess(url_path):
    # Maybe the current path is not standardized, simplify it first
    simplified = simplify_logic_path(url_path)
    """
    now the path is clear,
    isdir and without trailing slash redirect to url_path+'/'
    Non-standard redirects to simplified ones
    not found return 404page
    the rest is normal
    """
    if simplified != url_path:
        return redirect(simplified)
    if os.path.isdir(url_path) and not url_path.endswith('/'):
        return redirect(url_path+'/')
    if url_path and not path_exists(url_path):
        return render_template('404.html'), 404

"""exception: type in templates/test will redirect to templates/templates/test"""
def handle_directory(url_path):
    temp = url_path
    if not url_path:
        temp = '.'
    subs = [sub.name+'/' if sub.is_dir() else sub.name for sub in os.scandir(temp)]
    if 'index.html' in subs:
        with open(os.path.join(url_path, 'index.html')) as page:
            contents = page.read()
        return contents
    return render_template('directfor.html', cur_dir = '/' + url_path, subs = subs)

def handle_file(url_path):
    with open(url_path) as page:
        contents = page.read()
    return contents

@app.route('/', defaults = {'url_path':''})
@app.route('/<path:url_path>')
def direct(url_path):
    """
    There may be a problem with user input, which will cause an exception, so preprocessing is required
    """
    handle = preprocess(url_path) 
    if handle:
        return handle

    """Now, url_path is the normal path"""
    
    if not url_path or url_path.endswith('/'):
        return handle_directory(url_path)
    return handle_file(url_path)

if __name__ == "__main__":
    app.run(debug = True, port=9000)