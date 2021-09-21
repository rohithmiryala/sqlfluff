"""An example of a custom rule implemented through the plugin system."""

from sqlfluff.core.plugin import hookimpl
from sqlfluff.core.rules.base import (
    BaseRule,
    LintResult,
)
from sqlfluff.core.rules.doc_decorators import (
    document_fix_compatible,
    document_configuration,
)
from typing import List
import os.path
from sqlfluff.core.config import ConfigLoader


@hookimpl
def get_rules() -> List[BaseRule]:
    """Get plugin rules."""
    return [Rule_Dunzo_L001]


@hookimpl
def load_default_config() -> dict:
    """Loads the default configuration for the plugin."""
    return ConfigLoader.get_global().load_default_config_file(
        file_dir=os.path.dirname(__file__),
        file_name="plugin_default_config.cfg",
    )


@hookimpl
def get_configs_info() -> dict:
    """Get rule config validations and descriptions."""
    return {
        "forbidden_columns": {"definition": "A list of column to forbid"},
    }


# These two decorators allow plugins
# to be displayed in the sqlfluff docs
@document_fix_compatible
@document_configuration
class Rule_Dunzo_L001(BaseRule):
    """ORDER BY on these columns is forbidden!

    | **Anti-pattern**
    | Using ORDER BY one some forbidden columns.

    .. code-block:: sql

        SELECT *
        FROM foo
        ORDER BY
            bar,
            baz

    | **Best practice**
    | Do not order by these columns.

    .. code-block:: sql

        SELECT *
        FROM foo
        ORDER BY bar
    """

    config_keywords = ["forbidden_columns"]

    def __init__(self, *args, **kwargs):
        """Overwrite __init__ to set config."""
        super().__init__(*args, **kwargs)
        self.forbidden_columns = [
            col.strip() for col in self.forbidden_columns.split(",")
        ]

    def _eval(self, segment, raw_stack, **kwargs):
        """We should not use ORDER BY."""
        if segment.is_type("update_statement"):
            where_clause = False
            for seg in segment.segments:
                if seg.is_type("WhereClauseSegment"):
                    where_clause = True
            if not where_clause:
                return LintResult(
                    anchor=None,
                    description=f"update statement without where clause not allowed",
                )
