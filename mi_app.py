import streamlit as st
import google.generativeai as generative_ai
import os

CLAVE_DE_API = "AIzaSyCbGeNYZ-T5QNDUig6OAudFnHVoSy50EXw"

if not CLAVE_DE_API:
    st.error("Falta la clave de API. Configúrala antes de ejecutar la aplicación.")
else:
    generative_ai.configure(api_key=CLAVE_DE_API)

    st.title("Generador de código SQL con Gemini")

    # Entradas de usuario
    database_description = st.text_area("Describe la base de datos:", height=150)
    problem_description = st.text_area("Describe el problema:", height=150)

    if st.button("Generar código SQL"):
        prompt = f"""
        Base de datos:
        {database_description}

        Problema:
        {problem_description}

        Genera el código SQL correspondiente y proporciona una explicación detallada.
        Formato de respuesta:
        - Código SQL encerrado entre etiquetas <SQL></SQL>.
        - Explicación encerrada entre etiquetas <EXPLICACION></EXPLICACION>.
        """

        try:
            model = generative_ai.GenerativeModel("gemini-pro")
            response = model.generate_content(prompt)

            if response and hasattr(response, "text"):
                response_text = response.text

                # Extraer el código SQL y la explicación usando etiquetas personalizadas
                sql_code = "Código no encontrado"
                explanation = "Explicación no encontrada"

                if "<SQL>" in response_text and "</SQL>" in response_text:
                    sql_code = response_text.split("<SQL>")[1].split("</SQL>")[0].strip()

                if "<EXPLICACION>" in response_text and "</EXPLICACION>" in response_text:
                    explanation = response_text.split("<EXPLICACION>")[1].split("</EXPLICACION>")[0].strip()

                # Mostrar el código SQL generado
                st.subheader("Código SQL Generado:")
                st.code(sql_code, language="sql")

                # Mostrar la explicación del código SQL
                st.subheader("Explicación del Código:")
                st.write(explanation)

            else:
                st.error("No se recibió una respuesta válida de la API.")

        except Exception as e:
            st.error(f"Error al generar código SQL: {str(e)}")
