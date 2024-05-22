import os, sys

class ReadPath:
    def __init__(self, path, extension):
        self.path = path
        self.extension = extension

    def read(self, branch):
        print(f'Leyendo archivos de la ruta {self.path}...', file=sys.stdout)
        print(f'Branch: {branch}', file=sys.stdout)        
        try:
            for root, dirs, files in os.walk(self.path, self.extension):
                if ('DataSource') in root:
                    full_path = os.path.join(root)
                    branch_file = full_path.split('/')[6]
                    project_file = full_path.split('/')[4]                    
                    if branch in full_path:# and branch==branch_file:
                        print(f'Project File: {project_file}', file=sys.stdout)
                        print(f'Branch File: {branch_file}', file=sys.stdout)
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
        print('Leyendo archivos...', file=sys.stdout)
        try:
            for root, dirs, files in os.walk(self.path, self.extension):
                project_file = root.split('/')[2]
                if project==project_file:
                    if ('Aggregation') in root:
                        full_path = os.path.join(root)
                        if branch in full_path:
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
