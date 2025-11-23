"""Carga modelos al arrancar la app FastAPI. """ 
import os 
import joblib

BASE = os.path.dirname(os.path.dirname(__file__))  # project_root/server/.. -> project_root

MODELS = {}

def load_categoria_model(): 
    model_path = os.path.join(BASE, "models", "categoria_model", "model.pkl") 
    if os.path.exists(model_path): 
        MODELS['categoria'] = joblib.load(model_path) 
        print('Categoria model loaded') 
    else: 
        print('Categoria model not found at', model_path)

def load_soluciones_model():
    model_path = os.path.join(BASE, "models", "soluciones_model", "model.pkl")
    if os.path.exists(model_path):
        MODELS['soluciones'] = joblib.load(model_path)
        print('Soluciones model loaded')
    else:
        print('Soluciones model not found at', model_path)


#Llama a esta función al arrancar server

def load_all():
    load_categoria_model()
    load_soluciones_model()
