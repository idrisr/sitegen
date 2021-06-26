from nbconvert.preprocessors import Preprocessor
import re
import ast



class YAMLFrontMatterPreProcessor(Preprocessor):
    def _check_front_matter(self, cell):
        pattern = re.compile(r"^#frontmatter")
        return pattern.match(cell.source)
    
    def preprocess(self, nb, resources):
        if self._check_front_matter(nb.cells[0]):
            resources['front_matter'] = ast.literal_eval(nb.cells[0]['source'])
            nb.cells = nb.cells[1:]
        else:
            resources['front_matter'] = {}
        return nb, resources
