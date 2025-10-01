import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import numpy as np

def _crear_features(df: pd.DataFrame) -> pd.DataFrame:
    """Crea nuevas features a partir de los datos existentes para mejorar el modelo."""
    df_copy = df.copy()

    # Convertir 'hora_hecho' a datetime
    df_copy['hora_hecho'] = pd.to_datetime(df_copy['hora_hecho'], format='%H:%M:%S', errors='coerce').dt.hour
    
    # Defino las zonas horarias aca
    bins = [-1, 6, 12, 19, 24]
    labels = ['Madrugada', 'Mañana', 'Tarde', 'Noche']
    df_copy['zona_horaria'] = pd.cut(df_copy['hora_hecho'], bins=bins, labels=labels, right=False)

    # Defino los dias de la seamna aca
    df_copy['fecha_hecho'] = pd.to_datetime(df_copy['fecha_hecho'], errors='coerce')
    df_copy['dia_semana'] = df_copy['fecha_hecho'].dt.day_name()
    
    return df_copy

@st.cache_resource
def entrenar_modelo_y_preprocesador(df: pd.DataFrame):
    """
    Prepara los datos, entrena un modelo RandomForest y devuelve el pipeline entrenado.
    Se cachea para no re-entrenar en cada interacción del usuario.
    """
    with st.spinner("🧠 Entrenando el modelo de predicción por primera vez... Esto puede tardar un momento."):
        
        df_ml = _crear_features(df)
        
        # Features
        features = [
            'provincia_nombre', 'mes', 'zona_horaria', 'dia_semana', 'tipo_lugar'
        ]
        target = 'calle_nombre'
        
        df_ml = df_ml.dropna(subset=features + [target])
        df_ml = df_ml[df_ml[target].str.lower() != 'sin determinar']
        df_ml = df_ml[df_ml[target].str.lower() != 'perdido']

        # Solo dejar calles con suficientes datos (10 al menos)
        top_streets = df_ml[target].value_counts()
        streets_to_keep = top_streets[top_streets > 10].index 
        
        if len(streets_to_keep) < 10:
             st.error("No hay suficientes datos históricos para entrenar un modelo fiable. Se necesitan más incidentes por calle.")
             return None

        df_ml = df_ml[df_ml[target].isin(streets_to_keep)]
        
        X = df_ml[features]
        y = df_ml[target]
        
        
        X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
        
        # creo el pipeline
        preprocessor = ColumnTransformer(
            transformers=[
                ('cat', OneHotEncoder(handle_unknown='ignore'), features)
            ])
            
        model_pipeline = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('classifier', RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced'))
        ])
        
        # Entrenamienot
        model_pipeline.fit(X_train, y_train)
        
    return model_pipeline

def mostrar_interfaz_prediccion(df: pd.DataFrame):
    """Muestra la interfaz de usuario en Streamlit para hacer predicciones."""
    
    
    st.markdown(
        "Esta herramienta utiliza un modelo de Machine Learning para predecir las **5 calles con mayor probabilidad** "
        "de que ocurra un siniestro vial, según las condiciones que selecciones."
    )
    st.info("ℹ️ **Nota:** El modelo se ha entrenado con datos históricos y su precisión depende de la cantidad y calidad de los mismos. Por ello, la mejor prediccion sera en provincia de BS AS por la cantidad de datos.")

    pipeline = entrenar_modelo_y_preprocesador(df)
    
    if pipeline is None:
        return

    st.markdown("#### Selecciona los parámetros para la predicción:")

    col1, col2 = st.columns(2)
    
    
    # Meses a su valor numerico
    meses_map = {
        'Enero': 1, 'Febrero': 2, 'Marzo': 3, 'Abril': 4, 'Mayo': 5, 'Junio': 6, 
        'Julio': 7, 'Agosto': 8, 'Septiembre': 9, 'Octubre': 10, 'Noviembre': 11, 'Diciembre': 12
    }
    

    with col1:
        provincia = st.selectbox(
            "Provincia:",
            options=sorted(df['provincia_nombre'].unique())
        )
        
        
        # Usamos los nombres de los meses como opciones y quitamos el format_func incorrecto
        mes_nombre_seleccionado = st.selectbox(
            "Mes:",
            options=list(meses_map.keys())
        )
        

        tipo_lugar = st.selectbox(
            "Tipo de Lugar:",
            options=sorted(df['tipo_lugar'].dropna().unique())
        )

    with col2:
        zona_horaria = st.selectbox(
            "Franja Horaria:",
            options=['Mañana', 'Tarde', 'Noche', 'Madrugada']
        )
        dia_semana = st.selectbox(
            "Día de la Semana:",
            options=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
            format_func=lambda x: {'Monday':'Lunes', 'Tuesday':'Martes', 'Wednesday':'Miércoles', 'Thursday':'Jueves', 'Friday':'Viernes', 'Saturday':'Sábado', 'Sunday':'Domingo'}.get(x, x)
        )

    if st.button("🚀 Predecir Calles de Riesgo", type="primary"):
        
        
        # Convertimos 
        mes_numero = meses_map[mes_nombre_seleccionado]
        

        input_data = pd.DataFrame({
            'provincia_nombre': [provincia],
            'mes': [mes_numero], # <--- Usamos el valor numérico correcto
            'zona_horaria': [zona_horaria],
            'dia_semana': [dia_semana],
            'tipo_lugar': [tipo_lugar]
        })

        with st.spinner("🤖 Analizando patrones y calculando probabilidades..."):
            probabilities = pipeline.predict_proba(input_data)[0]
            classes = pipeline.classes_
            
            results_df = pd.DataFrame({
                'Calle': classes,
                'Probabilidad': probabilities
            }).sort_values(by='Probabilidad', ascending=False)
            
            top_5_results = results_df.head(5)
            
        st.success("✅ ¡Análisis completado! Estas son las 5 calles con mayor probabilidad de siniestro:")

        for index, row in top_5_results.iterrows():
            st.metric(
                label=f"📍 {row['Calle']}",
                value=f"{row['Probabilidad']:.2%}"
            )
        
        st.markdown("---")
        st.subheader("Detalle de las probabilidades")
        st.dataframe(top_5_results.style.format({'Probabilidad': '{:.2%}'}), use_container_width=True)

