import pandas as pd


# Listado de magnitudes de contaminación de la Comunidad de Madrid
# -----------------------------------------------------------------
maglist_com = {
# código     magnitud         unidades    
1 	:  ('Dióxido de azufre', 'μg/m³'),
6 	:  ('Monóxido de carbono', 'mg/m³'),
7 	:  ('Monóxido de nitrógeno', 'μg/m³'),
8 	:  ('Dióxido de nitrógeno', 'μg/m³'),
9 	:  ('Partículas en suspensión < PM2.5', 'μg/m³'),
10 	:  ('Partículas en suspensión < PM10',  'μg/m³'),
12 	:  ('Óxidos de nitrógeno', 'μg/m³'),
14 	:  ('Ozono', 'μg/m³'),
20 	:  ('Tolueno', 'μg/m³'),
22 	:  ('Black Carbon', 'μg/m³'),
30 	:  ('Benceno', 'μg/m³'),
42 	:  ('Hidrocarburos totales', 'mg/m³'),
44 	:  ('Hidrocarburos no metánicos', 'mg/m³'),
431 :  ('MetaParaXileno', 'μg/m³')
}

# Listado de estaciones de medida de contaminación de la Comunidad de Madrid
# -----------------------------------------------------------------------------
estalist_com = {
# código       municipio nombre_estación    
28005002   :    (  5,  'ALCALÁ DE HENARES'), 
28006004   :    (  6,  'ALCOBENDAS'), 
28007004   :    (  7,  'ALCORCÓN'), 
28009001   :	(  9,  'ALGETE'), 
28013002   :	( 13,  'ARANJUEZ'), 
28014002   :	( 14,  'ARGANDA DEL REY'),
28016001   :	( 16,  'EL ATAZAR'),
28045002   :	( 45,  'COLMENAR VIEJO'), 
28047002   :	( 47,  'COLLADO VILLALB A'), 
28049003   :	( 49,  'COSLADA'), 
28058004   :	( 58,  'FUENLABRADA'), 
28065014   :	( 65,  'GETAFE'), 
28067001   :	( 67,  'GUADALIX DE LA SIERRA'), 
28074007   :	( 74,  'LEGANÉS'), 
28080003   :	( 80,  'MAJADAHONDA'), 
28092005   :	( 92,  'MÓSTOLES'), 
28102001   :	(102,  'ORUSCO DE TAJUÑA'), 
28120001   : 	(120,  'PUERTO DE COTOS'), 
28123002   :	(123,  'RIVAS-VACIAMADRID'), 
28133002   :	(133,  'SAN MARTÍN DE VALDEIGLESIAS'), 
28148004   :	(148,  'TORREJÓN DE ARDOZ'), 
28161001   :	(161,  'VALDEMORO'), 
28171001   :	(171,  'VILLA DEL PRADO'), 
28180001   :	(180,  'VILLAREJO DE SALVANÉS')
}

# Listado de estaciones meteorológicas (AEMET) en Madrid
# -------------------------------------------------------
estalist_meteo = {
# código       municipio nombre_estación    
28005002   :    (  5,  'ALCALÁ DE HENARES'), 
28006004   :    (  6,  'ALCOBENDAS'), 
28007004   :    (  7,  'ALCORCÓN'), 
28009001   :	(  9,  'ALGETE'), 
28013002   :	( 13,  'ARANJUEZ'), 
28014002   :	( 14,  'ARGANDA DEL REY'),
28016001   :	( 16,  'EL ATAZAR'),
28045002   :	( 45,  'COLMENAR VIEJO'), 
28047002   :	( 47,  'COLLADO VILLALB A'), 
28049003   :	( 49,  'COSLADA'), 
28058004   :	( 58,  'FUENLABRADA'), 
28065014   :	( 65,  'GETAFE'), 
28067001   :	( 67,  'GUADALIX DE LA SIERRA'), 
28074007   :	( 74,  'LEGANÉS'), 
28080003   :	( 80,  'MAJADAHONDA'), 
28092005   :	( 92,  'MÓSTOLES'), 
28102001   :	(102,  'ORUSCO DE TAJUÑA'), 
28120001   : 	(120,  'PUERTO DE COTOS'), 
28123002   :	(123,  'RIVAS-VACIAMADRID'), 
28133002   :	(133,  'SAN MARTÍN DE VALDEIGLESIAS'), 
28148004   :	(148,  'TORREJÓN DE ARDOZ'), 
28161001   :	(161,  'VALDEMORO'), 
28171001   :	(171,  'VILLA DEL PRADO'), 
28180001   :	(180,  'VILLAREJO DE SALVANÉS')
}

# Listado de magnitudes meteorológicas (AEMET) en Madrid
# --------------------------------------------------------
maglist_meteo = {
# código     magnitud                unidades    
81 :	('Velocidad del viento',     'm/s'), 
82 :	('Dirección del viento',     'º'), 
83 :	('Temperatura',              'ºC'), 
86 :	('Humedad relativa',         '%'), 
87 :	('Presión atmosférica',      'hPa'), 
88 :	('Radiación solar',          'W/m2'), 
89 :	('Precipitación',            'mm')
}


def comunidad(ifile, codigo_magnitud=8, codigo_estacion=28067001) :
    
    # Lectura de datos
    # -------------------------------------------
    df = pd.read_csv(ifile,sep=';', decimal=',')
    
    # Selección de estación y contaminante
    # --------------------------------------
    df = df[ (df['estacion']  == int(str(codigo_estacion)[-3:])) 
           & (df['magnitud']  == codigo_magnitud) 
           & (df['municipio'] == estalist_com[codigo_estacion][0])]
  
    # Tamaño de la muestra
    # -------------------------
    print(' -Info: encontrados datos de %d días' % len(df))
    
    # Eliminamos información innecesaria
    # -----------------------------------------
    df = df.drop(columns=['provincia','municipio',
                          'estacion','punto_muestreo','magnitud'])
    
    # Pasamos los días de columnas a filas con
    # el contaminante como valor
    # -----------------------------------------
    df1 = df.melt(id_vars=['ano','mes','dia'],
                 value_vars = [ 'h%02d' % i for i in range(1,25)],
                 var_name='hora',
                 value_name='valor',  
                 )
       
    # Convertimos la hora a valor numérico
    # --------------------------------------------------
    df1['hora'] = df1['hora'].apply(lambda x : int(x[1:]))
    
 
    # Pasamos los días de columnas a filas con
    # el flag de calidad como valor
    # -----------------------------------------
    df2 = df.melt(id_vars=['ano','mes','dia'],
                 value_vars = [ 'v%02d' % i for i in range(1,25)],
                 var_name='hora',
                 value_name='flag',  
                 )
    
    # Convertimos el día a valor numérico
    # --------------------------------------------------
    df2['hora'] = df2['hora'].apply(lambda x : int(x[1:]))
    
    # Combinamos filas de columnas iguales
    # --------------------------------------------
    df = df1.merge(df2)
    
    # Retenemos solo valores válidos
    # -----------------------------------------------
    df = df[df['flag'] == 'V'].drop(columns='flag')
    
    # Generamos una fecha a partir de las columnas
    # -----------------------------------------------
    df['fecha'] = pd.to_datetime({'year':df.ano,'month':df.mes,'day':df.dia,'hour':df.hora})
    
    # Eliminamos columnas innecesarias
    # -------------------------------------
    df = df.drop(columns=['ano','mes','dia','hora'])
    
    # Reordenamos las columnas (no es necesario)
    # -------------------------------------------
    df = df[['fecha','valor']]

    # Establecemos el tiempo como índice
    # ------------------------------------
    df.set_index(['fecha'],inplace=True)

    # Ordenamos los datos por tiempo creciente
    # ------------------------------------------
    df.sort_index(inplace=True)
    
    return df, *maglist_com[codigo_magnitud], estalist_com[codigo_estacion][1]



def meteo(ifile, codigo_magnitud=83, codigo_estacion=28067001) :

    # Lectura de datos
    # -------------------------------------------
    df = pd.read_csv(ifile,sep=';', decimal='.')
    
    # Selección de estación y contaminante
    # --------------------------------------
    df = df[ (df['estacion']  == int(str(codigo_estacion)[-3:])) 
           & (df['magnitud']  == codigo_magnitud) 
           & (df['municipio'] == estalist_meteo[codigo_estacion][0])]
    
    # Tamaño de la muestra
    # -------------------------
    print(' -Info: encontrados datos de %d días' % len(df))
    
    # Eliminamos información innecesaria
    # -----------------------------------------
    df = df.drop(columns=['provincia','municipio',
                          'estacion','punto_muestreo','magnitud'])
    
    # Pasamos los días de columnas a filas con
    # el contaminante como valor
    # -----------------------------------------
    df1 = df.melt(id_vars=['ano','mes','dia'],
                 value_vars = [ 'h%02d' % i for i in range(1,25)],
                 var_name='hora',
                 value_name='valor',  
                 )
        
    # Convertimos la hora a valor numérico
    # --------------------------------------------------
    df1['hora'] = df1['hora'].apply(lambda x : int(x[1:]))
    

    # Pasamos los días de columnas a filas con
    # el flag de calidad como valor
    # -----------------------------------------
    df2 = df.melt(id_vars=['ano','mes','dia'],
                 value_vars = [ 'v%02d' % i for i in range(1,25)],
                 var_name='hora',
                 value_name='flag',  
                 )
    
    # Convertimos el día a valor numérico
    # --------------------------------------------------
    df2['hora'] = df2['hora'].apply(lambda x : int(x[1:]))
    
    # Combinamos filas de columnas iguales
    # --------------------------------------------
    df = df1.merge(df2)
    
    # Retenemos solo valores válidos
    # -----------------------------------------------
    df = df[df['flag'] == 'V'].drop(columns='flag')
    
    # Generamos una fecha a partir de las columnas
    # -----------------------------------------------
    df['fecha'] = pd.to_datetime({'year':df.ano,'month':df.mes,'day':df.dia,'hour':df.hora})
    
    # Eliminamos columnas innecesarias
    # -------------------------------------
    df = df.drop(columns=['ano','mes','dia','hora'])
    
    # Reordenamos las columnas (no es necesario)
    # -------------------------------------------
    df = df[['fecha','valor']]

    # Establecemos el tiempo como índice
    # ------------------------------------
    df.set_index(['fecha'],inplace=True)

    # Ordenamos los datos por tiempo creciente
    # ------------------------------------------
    df.sort_index(inplace=True)
    
    return df, *maglist_meteo[codigo_magnitud], estalist_meteo[codigo_estacion][1]



