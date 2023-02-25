
Importante
============

Este directorio contiene scripts Python correspondientes a los notebooks del repositorio.
Pueden ejecutarse directamente en Spyder en un entorno que contenga las extensiones necesarias.

Esta guía resume los pasos para el uso en Windows:

1.- Instalar miniconda, disponible en:

     https://docs.conda.io/en/latest/miniconda.html

2.- En la consola conda (Inicio > Miniconda) crear el entorno 'aire' con las extensiones necesarias:

    a) de forma automática:

          conda env create --file=aire.yml

    b) o bien de forma manual:

          # Creamos un entorno conda llamado aire
          # ------------------------------------
          conda create --name aire

          # Entramos en el entorno conda llamado aire
          # ----------------------------------------
          conda activate aire

          # Instalamos las extensiones necesarias
          # ------------------------------------
          conda install spyder
          conda install pandas
          conda install matplotlib
          conda install numpy
          conda install scipy
          conda install scikit-lyearn

3.- Iniciar el entorno de desarrollo spyder y acceder a los scripts de este directorio








