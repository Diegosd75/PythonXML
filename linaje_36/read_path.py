import os, sys

class ReadPath:
    def __init__(self, path, extension):
        self.path = path
        self.extension = extension

    def read(self, branch):
        print(f'Leyendo archivos de la ruta {self.path}...', file=sys.stdout)
        try:
            for root, dirs, files in os.walk(self.path, self.extension):
                if ('DataSource') in root:
                    full_path = os.path.join(root)
                    if branch in full_path:# and branch==branch_file:
                        for file in files:
                            if file.endswith(self.extension):
                                yield os.path.join(full_path, file)                                    
                            #case False:
                            #    for file in files:
                            #                match file.endswith(self.extension):
                            #                    case True:
                            #                        yield os.path.join(full_path, file)
        except Exception as e:
            raise FileNotFoundError(f"Error al leer el directorio: {e}")
        
    def read_agg(self, project, branch):
        print(f'Leyendo archivos de la ruta {self.path}...', file=sys.stdout)
        try:
            for root, dirs, files in os.walk(self.path, self.extension):                                
                if (('Aggregation') in root) or (('Portfolio') in root):
                    full_path = os.path.join(root)
                    project_file = root.split('/')[4]
                    if branch in full_path and project==project_file:
                        for file in files:
                            if file.endswith(self.extension):
                                yield os.path.join(full_path, file)
                        #case False:
                        #    for file in files:
                        #                match file.endswith(self.extension):
                        #                    case True:
                        #                        yield os.path.join(full_path, file)
        except Exception as e:
            raise FileNotFoundError(f"Error al leer el directorio: {e}")
