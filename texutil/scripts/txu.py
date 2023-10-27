import rich_click as click
import os, re

@click.group()
def cli():
    pass

@click.command()
@click.argument('directory', type=click.Path(exists=True))
@click.option('-i', '--ignore', multiple=True,
            help='Filetype to ignore. (e.g. pdf, dvi)')
def clean(directory, ignore):
    """
    Cleans a directory of generated files after TeX compilation. By default, includes everything except .tex
    Use the -i flag to ignore a specific file type. This option can be repeated as necessary. 
    """
    if directory.endswith('/'):
        directory = directory[:-1]

    tex_detritus_extensions = ['aux', 'fdb_latexmk', 'fls', 'log', 'out', 'pdf', 'dvi', 'synctex.gz']

    for extension in ignore:
        tex_detritus_extensions.remove(extension)
    
    extension_search_pattern =  f".*\.({'|'.join(tex_detritus_extensions)})"
    regex = re.compile(extension_search_pattern)
    
    file_deletion_count = 0
    for file in os.listdir(directory):
        if regex.match(file):
            file_path = f"{directory}/{file}"
            os.remove(file_path)
            file_deletion_count += 1
    
    click.echo(f"Removed {file_deletion_count} files.")

cli.add_command(clean)
if __name__ == '__main__':
    cli()