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
    def exporter():
        c = get_config()
        c.TemplateExporter.template_file = "my.tpl"
        c.MarkdownExporter.preprocessors = [YAMLFrontMatterPreProcessor, HideCell]
        c.ExtractOutputPreprocessor.output_filename_template = '{unique_key}_{cell_index}_{index}{extension}'
        c.MarkdownExporter.enabled = True
        #  c.FilesWriter.build_directory = "moveme"
        c.Application.log_level = 0
        c.TemplateExporter.filters = {'jekyllify': jekyllify}
        return c

    @staticmethod
    def file_writer():
        return get_config()


def convert_notebook(notebook: Path):
    """ converts notebook into markdown. notebook should already have valid
    jekyll name 
    """

    exporter = MarkdownExporter(config=Config.exporter())
    (output, resources) = exporter.from_filename(filename=notebook)

    fw = FilesWriter(config=get_config())
    with tempfile.TemporaryDirectory() as tmpdirname:
        c = Config.file_writer()
        #  c.FilesWriter.build_directory = tmpdirname
        fw.write(output, resources, notebook_name=notebook.stem)
        print(list(Path(tmpdirname).glob("*")))
        import ipdb; ipdb.set_trace()

    #  jupyter nbconvert --config mycfg.py --to markdown  99-sample-notebook.ipynb

if __name__ == '__main__':
    nb = Path.home() / 'idrisr.github.io/_jupyter/2021-06-26-kaggle-api.ipynb'
    convert_notebook(nb)
