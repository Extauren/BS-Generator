import argparse
from weasyprint import HTML
from jinja2 import Environment, FileSystemLoader
from spire.doc import *
from data import Data

def print_help() -> None:
    print('python bs_generator.py "{structure_name} --bsa_air"')

def html_to_pdf(html_content, output_path) -> None:
    HTML(string=html_content).write_pdf(output_path)

def generate_pfd(data: Data, docx: bool) -> None:
    env = Environment(loader = FileSystemLoader('templates'))
    template = env.get_template('template.jinja')
    html: str = template.render(data = data)
    
    if docx is True:
        convert_html_to_docx(html)
    html_to_pdf(html, "bulletin_de_souscription.pdf")
    print("PDF have been generated succesfully")

def get_arguments():
    parser = argparse.ArgumentParser()
    
    parser.add_argument('structure', type = str, help='structure name')
    parser.add_argument('--docx', action='store_true', help='generate docx')
    parser.add_argument('--bsa-air', action='store_true', help='generate bsa air bs')
    args = parser.parse_args()
    return args

def convert_html_to_docx(html):
    document = Document()
    sec = document.AddSection()
    paragraph = sec.AddParagraph()

    paragraph.AppendHTML(html)
    document.SaveToFile("test.docx", FileFormat.Docx2016)
    document.Close()
    print("Docx have been generated succesfully")

def main():
    args = None

    args = get_arguments()
    data = Data(args.structure, args.bsa_air)
    generate_pfd(data, args.docx)

if __name__ == "__main__":
    main()