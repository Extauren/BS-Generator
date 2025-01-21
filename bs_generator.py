import os
import argparse
from dotenv import load_dotenv
from weasyprint import HTML
from jinja2 import Environment, FileSystemLoader
from spire.doc import *
from data import Data

def convert_html_to_docx(html, name: str):
    path: str = os.environ["FOLDER"] + name + ".docx"
    document = Document()
    sec = document.AddSection()
    paragraph = sec.AddParagraph()

    paragraph.AppendHTML(html)
    document.SaveToFile(path, FileFormat.Docx2016)
    document.Close()
    print("Docx have been generated succesfully")

def html_to_pdf(html_content, output_path) -> None:
    HTML(string=html_content).write_pdf(output_path)

def generate_pfd(data: Data, docx: bool, name: str) -> None:
    path: str = os.environ["FOLDER"] + name + ".pdf"
    env = Environment(loader = FileSystemLoader('templates'))
    template = env.get_template('template.jinja')
    html: str = template.render(data = data)
    
    if docx is True:
        convert_html_to_docx(html, name)
    
    html_to_pdf(html, path)
    print("PDF have been generated succesfully")

def get_arguments():
    parser = argparse.ArgumentParser()
    
    parser.add_argument('-s', type = str, help='structure name')
    parser.add_argument('-n', type = str, help = "bs name")
    parser.add_argument('--docx', action='store_true', help='generate docx')
    parser.add_argument('--bsa-air', action='store_true', help='generate bsa air bs')
    args = parser.parse_args()
    return args

def main():
    args = None

    load_dotenv()
    args = get_arguments()
    data = Data(args.s, args.bsa_air)
    generate_pfd(data, args.docx, args.n)

if __name__ == "__main__":
    main()