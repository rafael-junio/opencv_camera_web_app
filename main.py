from flask import Flask, render_template, Response, request, session, send_file
from pipeline.app_pipeline import AppPipeline

app = Flask(__name__)
camera = AppPipeline()


@app.route('/')
def render_home() -> render_template:
    return render_template('index.html')


@app.route('/crop', methods=['GET', 'POST'])
def render_crop() -> render_template:
    if request.method == 'POST' and request.form.get('x') and request.form.get('y') \
            and request.form.get('dx') and request.form.get('dy'):
        camera.set_crop_values(request.form.get('x'), request.form.get('y'),
                               request.form.get('dx'), request.form.get('dy'))
        session['crop_valid'] = True
    if request.method == 'GET':
        session['crop_valid'] = False
    return render_template('crop.html')


@app.route('/background', methods=['GET', 'POST'])
def render_background() -> render_template:
    camera.set_background()
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


@app.route('/detect_faces')
def render_detect_faces() -> render_template:
    return render_template('detect_faces.html')


@app.route('/binarize_frame', methods=['GET', 'POST'])
def binarize_frame() -> Response:
    return Response(camera.binarize_render(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/detect_faces_frame', methods=['GET', 'POST'])
def detect_faces_frame() -> Response:
    return Response(camera.detect_faces_render(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/camera_frame')
def camera_frame() -> Response:
    return Response(camera.camera_render(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/background_frame')
def background_frame() -> Response:
    return Response(camera.background_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/crop_frame')
def crop_frame() -> Response:
    return Response(camera.camera_render(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/freezed_frame')
def freezed_frame() -> Response:
    return Response(camera.crop_image(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/download_cropped_image', methods=['POST'])
def download_cropped_image():
    return send_file('assets/cropped_image.jpg', as_attachment=True)


if __name__ == '__main__':
    app.secret_key = 'secret_key'
    app.run(debug=False, host='localhost', port=5000)
