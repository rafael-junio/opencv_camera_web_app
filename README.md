# Opencv Web App

### Funcionalidades:
- Index
  - Visualizador sem nenhuma transformação da webcam
- Background Removal
  - Remove o background usando um frame capturado anteriormente
- Binarize
  - Cria uma máscara binária configurável a partir de valores RGB e uma constante K
- Crop
  - Recorta um frame e o prepara para o download
- Detect Faces
  - Detecta a face no frame utilizando Opencv Cascade Classifier

### Dependências
```bash
  Flask
  Numpy
  Opencv-python
```

### Instruções de uso
```python
  git clone https://github.com/rafael-junio/opencv_camera_web_app.git
  cd opencv_camera_web_app
  pip install -r requirements.txt
  python main.py
```
Acesse qualquer navegador no endereço http://localhost:5000/
