import sys
from weasyprint import HTML
from jinja2 import Environment, FileSystemLoader
from data import Data

def print_help() -> None:
    print('python bs_generator.py "{structure_name}"')

def html_to_pdf(html_content, output_path) -> None:
    HTML(string=html_content).write_pdf(output_path)

def generate_pfd(data: Data) -> None:
    env = Environment(loader = FileSystemLoader('templates'))
    template = env.get_template('template.jinja')
    html: str = template.render(data = data)
    
    html_to_pdf(html, "bulletin_de_souscription.pdf")
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

def main():
    #generate word format
    structure: str = None

    structure = get_arguments()
    data = Data(structure)
    generate_pfd(data)

if __name__ == "__main__":
    main()