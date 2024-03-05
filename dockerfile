FROM python:3.10

# Establecer el directorio de trabajo
WORKDIR /Abbott_ec2_V2

# Copiar los archivos de la aplicación
COPY . .

RUN apt-get update && apt-get install -y portaudio19-dev

RUN apt-get install -y \
    alsa-utils \
    libasound2-dev \
    && rm -rf /var/lib/apt/lists/*
RUN pip install pyaudio

# Copia el ambiente virtual
COPY myenv/ ./myenv

# Activa el ambiente virtual
ENV PATH="/Abbott_ec2_V2/myenv/bin:$PATH"

# Instalar las dependencias
RUN pip install -r requirements.txt

# Exponer el puerto utilizado por Streamlit
EXPOSE 8501

# Comando para ejecutar la aplicación Streamlit
CMD ["streamlit", "run", "app_abbott_v2.py"]
