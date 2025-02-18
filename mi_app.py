import streamlit as st
import google.generativeai as generative_ai
import os

CLAVE_DE_API = "AIzaSyCbGeNYZ-T5QNDUig6OAudFnHVoSy50EXw"

if not CLAVE_DE_API:
    st.error("Falta la clave de API. Configúrala antes de ejecutar la aplicación.")
else:
    generative_ai.configure(api_key=CLAVE_DE_API)

    st.title("Generador de código SQL con Gemini")

    database_description = st.text_area("Describe la base de datos:", height=150)
    problem_description = st.text_area("Describe el problema:", height=150)

    if st.button("Generar código SQL"):
        prompt = f"""
        Base de datos:
        {database_description}

        Problema:
        {problem_description}

        Genera el código SQL correspondiente:
        """

        try:
            model = generative_ai.GenerativeModel("gemini-pro")
            response = model.generate_content(prompt)  # Método correcto

            if response and hasattr(response, "text"):
                st.code(response.text, language="sql")
            else:
                st.error("No se recibió una respuesta válida de la API.")

        except Exception as e:
            st.error(f"Error al generar código SQL: {str(e)}")