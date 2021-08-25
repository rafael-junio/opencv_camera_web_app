from flask import Flask, render_template, Response, request, session
from pipeline.app_pipeline import AppPipeline

app = Flask(__name__)
camera = AppPipeline()


@app.route('/background', methods=['GET', 'POST'])
def render_background_remover() -> render_template:
    if request.method == 'POST':
        if request.form.get('capturabg') == 'capturabg':
            session['background_set'] = True
            camera.set_background()
    if request.method == 'GET':
        session['background_set'] = False
    return render_template('background.html')


@app.route('/')
def render_home() -> render_template:
    return render_template('index.html')


@app.route('/camera_render')
def camera_render() -> Response:
    return Response(camera.stream(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/background_render')
def background_render() -> Response:
    return Response(camera.background_subtract(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.secret_key = 'secret_key'
    app.run(debug=False, host='localhost', port=5000)
