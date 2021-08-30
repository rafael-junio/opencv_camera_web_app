from flask import Flask, render_template, Response, request, session
from pipeline.app_pipeline import AppPipeline

app = Flask(__name__)
camera = AppPipeline()


@app.route('/')
def render_home() -> render_template:
    return render_template('index.html')


@app.route('/background', methods=['GET', 'POST'])
def render_background() -> render_template:
    if request.method == 'POST':
        if request.form.get('capturabg') == 'capturabg':
            session['background_set'] = True
            camera.set_background()
    if request.method == 'GET':
        session['background_set'] = False
    return render_template('background.html')


@app.route('/binarize', methods=['GET', 'POST'])
def render_binarize() -> render_template:
    if request.method == 'POST' and request.form.get('red') and request.form.get('green') \
            and request.form.get('blue') and request.form.get('k'):
        camera.set_binarize_values(int(request.form.get('red')), int(request.form.get('green')),
                                   int(request.form.get('blue')), int(request.form.get('k')))
    else:
        camera.set_binarize_values()
    return render_template('binarize.html')


@app.route('/binarize_frame', methods=['GET', 'POST'])
def binarize_frame() -> Response:
    return Response(camera.binarize_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/camera_frame')
def camera_frame() -> Response:
    return Response(camera.camera_render(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/background_frame')
def background_frame() -> Response:
    return Response(camera.background_subtract(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.secret_key = 'secret_key'
    app.run(debug=False, host='localhost', port=5000)
