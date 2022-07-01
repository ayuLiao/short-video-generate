from flask import Flask, render_template

app = Flask(
    __name__,
    static_folder='statics',
    template_folder='templates',
    static_url_path='',
)


@app.route('/')
def index():
    return render_template('iphonex.html')

if __name__ == '__main__':
    app.run()