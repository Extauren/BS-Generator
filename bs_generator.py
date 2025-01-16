import sys
from weasyprint import HTML
from jinja2 import Environment, FileSystemLoader
from spire.doc import *
from data import Data
# from gui import gui

def print_help() -> None:
    print('python bs_generator.py "{structure_name} --bsa_air"')

def html_to_pdf(html_content, output_path) -> None:
    HTML(string=html_content).write_pdf(output_path)

def generate_pfd(data: Data) -> None:
    env = Environment(loader = FileSystemLoader('templates'))
    template = env.get_template('template.jinja')
    html: str = template.render(data = data)
    
    convert_html_to_docx(html)
    html_to_pdf(html, "bulletin_de_souscription.pdf")
    print("PDF have been generated succesfully")

def convert_html_to_docx(html):
    document = Document()
    sec = document.AddSection()
    paragraph = sec.AddParagraph()

    paragraph.AppendHTML(html)
    document.SaveToFile("test.docx", FileFormat.Docx2016)
    document.Close()
    print("Docx have been generated succesfully")

    # output = pypandoc.convert_text(
    #     html, format='html', to='docx', extra_args=pdoc_args, outputfile="output2.docx"
    # )

def get_arguments() -> str:
    argv: list = sys.argv
    argv_nb: int = len(argv)
    bsa_air: bool = False

    if (argv_nb < 2):
        print(f"Wrong number of argument. Got {argv_nb - 1} but expected only 1")
        exit()
    if (argv[1] == '-h' or argv[1] == "--help"):
        print_help()
        exit()
    if argv_nb == 3 and argv[2] == "--bsa-air":
        bsa_air = True
    return argv[1], bsa_air

def main():
    structure: str = None
    bsa_air: bool = False

    structure, bsa_air = get_arguments()
    data = Data(structure, bsa_air)
    generate_pfd(data)
    # gui()

if __name__ == "__main__":
    main()