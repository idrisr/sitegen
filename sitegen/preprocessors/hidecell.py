from nbconvert.preprocessors import Preprocessor
import re

class HideCell(Preprocessor):
    def _check_hidden(self, cell):
        pattern = re.compile(r"^#hide")
        return not pattern.match(cell.source)

    def preprocess(self, nb, resources):
        nb.cells = list(filter(self._check_hidden, nb.cells))
        return nb, resources

