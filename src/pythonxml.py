import os
import xml.etree.ElementTree as ET
import pandas as pd

datafinal=[]

for root, dirs, files in os.walk('C:/REPOSITORIOS/PythonXML'):
    #print(root)-
    if 'DataSource' in root:
        full_path = os.path.join(root)
        if 'v_20230331' in full_path:
            print(full_path)
            print(os.listdir(full_path))
            for file in files:
                if file.endswith('.xml'):
                    # Construir ruta completa del archivo
                    file_path=full_path+"\\"+file
                    print(f"Leyendo archivo: {file_path}")
                    # Procesar el archivo XML capturando el error
                    try:
                        tree = ET.parse(file_path)
                        root_xml = tree.getroot()
                        # Buscar todas las etiquetas <name> y extraer su texto
                        nombreDS = root_xml.find(".//property[@name='name']").get('value')
                        if nombreDS :
                            print(f"Nombre encontrado: {nombreDS}")
                            dataconsol ={'nombreDS':nombreDS,'nombreCampo':'','tipoDeDato':'','longitud':''}
                        else:
                            print("Etiqueta <property> encontrada, pero falta información en los atributos.")

                        for obj in root_xml.findall(".//object[@type='DataSource:field']"):
                            name_property = obj.find(".//property[@name='name']")
                            type_property = obj.find(".//property[@name='type']")
                            if name_property is not None:
                                nombre_campo = name_property.get('value')
                                tipo_campo = type_property.get('value')
                                if tipo_campo == "VARCHAR":
                                    size_property = obj.find(".//property[@name='size']")
                                    size_campo = size_property.get('value')
                                    dataconsol=dataconsol.copy()
                                    dataconsol['nombreCampo'] = nombre_campo
                                    dataconsol['tipoDeDato'] = tipo_campo
                                    dataconsol['longitud'] = size_campo
                                    datafinal.append(dataconsol)
                                    print(f"Nombre campo {nombre_campo} y el tipo {tipo_campo} y el size es {size_campo}")
                                else:
                                    dataconsol=dataconsol.copy()
                                    dataconsol['nombreCampo'] = nombre_campo
                                    dataconsol['tipoDeDato'] = tipo_campo
                                    datafinal.append(dataconsol)
                                    print(f"Nombre campo {nombre_campo} y el tipo {tipo_campo}")
                                
                    
                    except ET.ParseError as e:
                        print(f"Error al procesar el archivo {file}: {e}")

# Creamos un Dataframe con los datos obtenidos
df = pd.DataFrame(datafinal)

# Generamos la salida en un informe de tipo excel
df.to_excel('C:/REPOSITORIOS/PythonXML/salidaxmlcv.xlsx')