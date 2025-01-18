import sys
from weasyprint import HTML
from jinja2 import Environment, FileSystemLoader
from data import Data
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QObject, Slot
from PySide6.QtQml import QmlElement

QML_IMPORT_NAME = "bs_generator"
QML_IMPORT_MAJOR_VERSION = 1

@QmlElement
class Console(QObject):
    @Slot(str, str, str)
    def generate_bs(self, structure: str, bs_type: str, path: str):
        data = Data(structure)
        generate_pfd(data, path.replace("file://", ""))

def print_help() -> None:
    print('python bs_generator.py "{structure_name}"')

def html_to_pdf(html_content, output_path) -> None:
    HTML(string=html_content).write_pdf(output_path)

def generate_pfd(data: Data, path: str) -> None:
    print(path)
    env = Environment(loader = FileSystemLoader('templates'))
    template = env.get_template('template.jinja')
    html: str = template.render(data = data)
    
    html_to_pdf(html, path)
    print("PDF have been generated succesfully")

def get_arguments() -> str:
    argv: list = sys.argv
    argv_nb: int = len(argv)

    if (argv_nb != 2):
        print(f"Wrong number of argument. Got {argv_nb - 1} but expected only 1")
        exit()
    if (argv[1] == '-h' or argv[1] == "--help"):
        print_help()
        exit()
    return argv[1]

def start_gui():
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    engine.addImportPath(sys.path[0])
    engine.loadFromModule("Example", "Main")
    if not engine.rootObjects():
        sys.exit(-1)
    exit_code = app.exec()
    del engine
    sys.exit(exit_code)

def generate_bs(structure: str):
    data = Data(structure)
    generate_pfd(data)

def main():
    # structure: str = None

    # structure = get_arguments()
    # data = Data(structure)
    # generate_pfd(data)
    start_gui()

if __name__ == "__main__":
    main()