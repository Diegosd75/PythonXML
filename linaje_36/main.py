import pandas as pd
import sys
import read_path
import process_xml
import execute_export
import argparse
import zipfile

argparser = argparse.ArgumentParser(description='Procesa archivos XML')
argparser.add_argument('-p', '--project', help='Proyecto a procesar', required=True)
argparser.add_argument('-b', '--branch', help='Branch a procesar', required=True)
argparser.add_argument('-w', '--wf', help='Workflow a procesar', required=True)
args = argparser.parse_args()
project = args.project
branch = args.branch
wf_name = args.wf

def main(project, branch):
    print(f'Leyendo path ./formato/{project}', file=sys.stdout)
    rp = read_path.ReadPath(f'./formato/{project}', '.xml')
    pxml = process_xml.ProcessXML()
    datafinal = []
    
    for file_path in rp.read(branch):
        print(f"Leyendo archivo: {file_path}", file=sys.stdout)
        datafinal.extend(pxml.process_xml_file(file_path))
    return datafinal

if __name__ == "__main__":
    try:
        #print('Ejecutando API export...', file=sys.stdout)
        #execute_export.run_process(project,branch,wf_name)
        
        print('Descomprimiendo export...', file=sys.stdout)
        with zipfile.ZipFile(f'./export_{project}_{branch}.zip', 'r') as zip_ref:
            zip_ref.extractall(f'./formato/{project}')

        print('Generando data...', file=sys.stdout)
        datafinal=main(project, branch)
        df = pd.DataFrame(datafinal)
        df.to_excel(f'./Fuentes_{project}_{branch}.xlsx', index=False)
        print("Proceso finalizado correctamente.")
    except Exception as ex:
        print(f"Error: {ex}", file=sys.stderr)
        sys.exit(1)