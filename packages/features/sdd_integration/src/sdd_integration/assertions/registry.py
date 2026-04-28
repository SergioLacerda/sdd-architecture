from .config import ConfigHasKeyAssertion, ConfigIsValidPathAssertion
from .filesystem import FsExistsAssertion
from .git import GitHasCommitAssertion
from .process import ProcessExitAssertion

REGISTRY = {
    "fs.exists": FsExistsAssertion,
    "config.has_key": ConfigHasKeyAssertion,
    "config.is_valid_path": ConfigIsValidPathAssertion,
    "process.exit_code": ProcessExitAssertion,
    "git.has_commit": GitHasCommitAssertion,
}
