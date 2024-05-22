import xml.etree.ElementTree as ET
import sys

class ProcessXML:
    def __init__(self):
        self.file_path = None

    def process_xml_file(self, file_path):
        print('Procesando XMLs...', file=sys.stdout)
        datafinal = []
        tree=ET.parse(file_path)
        root_xml=tree.getroot()
        nombre_ds=root_xml.find(".//property[@name='name']").get('value')
        project=file_path.split('/')[4]
        branch=file_path.split('/')[6]
        #project = file_path.split('/')[2]
        if nombre_ds:
            dataconsol = {'nombreDS':nombre_ds,'nombreCampo':'','tipoDeDato':'','longitud':'','Proyecto Contenedor':project,'Branch':branch}
        else:
            print("Etiqueta <property> encontrada, pero falta información en los atributos.")
            return []
        
        for obj in root_xml.findall(".//object[@type='DataSource:field']"):
            name_property = obj.find(".//property[@name='name']")
            type_property = obj.find(".//property[@name='type']")
            if name_property is not None:
                nombre_campo = name_property.get('value')
                tipo_campo = type_property.get('value')

                if tipo_campo=="VARCHAR":
                    size_property = obj.find(".//property[@name='size']")
                    size_campo = int(size_property.get('value'))
                else:
                    size_campo = 0

                dataconsol=dataconsol.copy()
                dataconsol['nombreCampo'] = nombre_campo
                dataconsol['tipoDeDato'] = tipo_campo
                dataconsol['longitud'] = size_campo
                datafinal.append(dataconsol)

        return datafinal