import sys
import argparse
from weasyprint import HTML
from jinja2 import Environment, FileSystemLoader
from data import Data
from spire.doc import *
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
        data = Data(structure, False)
        generate_pfd(data, False, path.replace("file://", ""))

def convert_html_to_docx(html):
    document = Document()
    sec = document.AddSection()
    paragraph = sec.AddParagraph()

    paragraph.AppendHTML(html)
    document.SaveToFile("test.docx", FileFormat.Docx2016)
    document.Close()
    print("Docx have been generated succesfully")

def html_to_pdf(html_content, output_path) -> None:
    HTML(string=html_content).write_pdf(output_path)

def generate_pfd(data: Data, docx: bool, path: str) -> None:
    env = Environment(loader = FileSystemLoader('templates'))
    template = env.get_template('template.jinja')
    html: str = template.render(data = data)
    
    if docx is True:
        convert_html_to_docx(html)
    html_to_pdf(html, path)
    print("PDF have been generated succesfully")

def get_arguments():
    parser = argparse.ArgumentParser()
    
    parser.add_argument('structure', type = str, help='structure name')
    parser.add_argument('--docx', action='store_true', help='generate docx')
    parser.add_argument('--bsa-air', action='store_true', help='generate bsa air bs')
    args = parser.parse_args()
    return args

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
    args = None

    # args = get_arguments()
    # data = Data(args.structure, args.bsa_air)
    # generate_pfd(data, args.docx)
    start_gui()

if __name__ == "__main__":
    main()