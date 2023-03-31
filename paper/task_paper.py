"""Tasks for compiling the paper and presentation(s)."""
import shutil

import pytask
from pytask_latex import compilation_steps as cs
from replication_child_benefit.config import BLD, PAPER_DIR


@pytask.mark.latex(
    script=PAPER_DIR / "replication_child_benefit.tex",
    document=BLD / "latex" / "replication_child_benefit.pdf",
    compilation_steps=cs.latexmk(
        options=("--pdf", "--interaction=nonstopmode", "--synctex=1", "--cd"),
    ),
)

def task_compile_document():
    """Compile the document specified in the latex decorator."""
    pass

@pytask.mark.depends_on(BLD / "latex" / "replication_child_benefit.pdf")
@pytask.mark.produces(BLD.parent.resolve() / "replication_child_benefit.pdf")
def task_copy_to_root(depends_on, produces):
    """Copy a document to the root directory for easier retrieval."""
    shutil.copy(depends_on, produces)
