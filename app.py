from flask import Flask, render_template, send_file, redirect
import os
import sys
"""
CWD: current working directory
"""
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

def path_exists(fs_path):
    if fs_path.endswith('/') and not os.path.isdir(fs_path):
        return False
    if not fs_path.endswith('/') and not os.path.isfile(fs_path):
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
    =======Note========
    For redirect(location)
        pass an absolute url as the location para
        or a relative url as the location para like: redirect(url_path.split('/')[-1] + '/', code = 301)
    """
    # print(simplified)
    if simplified != url_path:
        return redirect(simplified, code = 301)
    
    fs_path = os.path.join(CWD, url_path)

    if os.path.isdir(fs_path) and not fs_path.endswith('/'):
        # print(url_path+'/')
        return redirect('/'+ url_path + '/', code = 301) 
    
    if not path_exists(fs_path):
        return render_template('404.html'), 404

def handle_directory(url_path, fs_path):
    subs = [sub.name+'/' if sub.is_dir() else sub.name for sub in os.scandir(fs_path)]
    subs.append('../')
    subs.sort()
    if 'index.html' in subs:
        with open(os.path.join(fs_path, 'index.html')) as page:
            contents = page.read()
        return contents
    return render_template('directfor.html', cur_dir = '/' + url_path, subs = subs)

def handle_file(fs_path):
    with open(fs_path) as page:
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
    """
    Now, url_path is the normal path
    Expose a URL path to the outside, and use the file system path to check for existence and retrieve data.
    """
    fs_path = os.path.join(CWD, url_path)
    
    if fs_path.endswith('/'):
        return handle_directory(url_path, fs_path)
    return handle_file(fs_path)

if __name__ == "__main__":
    CWD = '.'
    if len(sys.argv) > 1:
        CWD = sys.argv[1]
    print(sys.argv)
    app.run(debug = True, port=9000)