import os
from argparse import ArgumentParser, Namespace
from dotenv import load_dotenv
from weasyprint import HTML
from jinja2 import Environment, FileSystemLoader, Template
from spire.doc import Document, FileFormat, Section, Paragraph
from data import Data

def convert_html_to_docx(html, name: str) -> None:
    path: str = os.environ["FOLDER"] + name + ".docx"
    document: Document = Document()
    section: Section = document.AddSection()
    paragraph: Paragraph = section.AddParagraph()

    paragraph.AppendHTML(html)
    document.SaveToFile(path, FileFormat.Docx2016)
    document.Close()
    print("Docx have been generated succesfully")

def html_to_pdf(html_content, output_path) -> None:
    HTML(string=html_content).write_pdf(output_path)

def generate_pfd(data: Data, docx: bool, name: str) -> None:
    path: str = os.environ["FOLDER"] + name + ".pdf"
    env: Environment = Environment(loader = FileSystemLoader('templates'))
    template: Template = env.get_template('template.jinja')
    html: str = template.render(data = data)
    
    if docx is True:
        convert_html_to_docx(html, name)
    
    html_to_pdf(html, path)
    print("PDF have been generated succesfully")

def get_arguments() -> Namespace:
    parser: ArgumentParser = ArgumentParser()
    
    parser.add_argument('-s', type = str, help='structure name', required=True)
    parser.add_argument('-n', type = str, help = "bs name", required=True)
    parser.add_argument('--docx', action='store_true', help='generate docx')
    parser.add_argument('--bsa-air', action='store_true', help='generate bsa air bs')
    parser.add_argument('--sas', action='store_true', help='sas')
    return parser.parse_args()

def main() -> None:
    args: Namespace = None
    data: Data = None

    load_dotenv()
    args = get_arguments()
    data = Data(args.s, args.bsa_air, args.sas)
    generate_pfd(data, args.docx, args.n)

if __name__ == "__main__":
    main()