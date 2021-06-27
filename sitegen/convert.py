from nbconvert import MarkdownExporter
from nbconvert.writers import FilesWriter
from traitlets.config import get_config
from pathlib import Path

from preprocessors.yaml import YAMLFrontMatterPreProcessor
from preprocessors.hidecell import HideCell
from filters.jekyllify import jekyllify
from sitegen import Notebooks, Posts

import tempfile

class Config:
    @staticmethod
    def config():
        c = get_config()
        c.TemplateExporter.template_file = "my.tpl"
        c.MarkdownExporter.preprocessors = [YAMLFrontMatterPreProcessor, HideCell]
        c.ExtractOutputPreprocessor.output_filename_template = '{unique_key}_{cell_index}_{index}{extension}'
        c.MarkdownExporter.enabled = True
        c.Application.log_level = 0
        c.TemplateExporter.filters = {'jekyllify': jekyllify}
        return c


def convert_notebook(notebook):
    """ converts notebook into markdown with custom preprocessors and filters. 
        notebook should already have valid jekyll name 
    """

    dest = notebook.parent.parent / "_posts"/ f'{notebook.stem}.md'
    exporter = MarkdownExporter(config=Config.config())
    (output, resources) = exporter.from_filename(filename=notebook)

    with tempfile.TemporaryDirectory() as tmpdirname:
        c = Config.config()
        c.FilesWriter.build_directory = tmpdirname
        fw = FilesWriter(config=c)
        fw.write(output, resources, notebook_name=notebook.stem)
        (Path(tmpdirname) / f'{notebook.stem}.md').rename(dest)

    #  jupyter nbconvert --config mycfg.py --to markdown  99-sample-notebook.ipynb

if __name__ == '__main__':
    nb = Path.home() / 'idrisr.github.io/_jupyter/2021-06-26-kaggle-api.ipynb'
    convert_notebook(nb)
