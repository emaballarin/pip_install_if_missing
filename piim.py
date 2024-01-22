from typing import Set, Optional, Union, Iterable, Tuple
import pkg_resources
import sys
import subprocess

__all__ = ["pip_install_if_missing"]


def _no_op(*args, **kwargs) -> None:
    pass


def _pip_install(name: str, indexurl: Optional[str] = None) -> None:
    indexargs = [] if indexurl is None else ["--index-url", indexurl]
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", name, *indexargs],
        stdout=subprocess.DEVNULL,
    )


def _pip_install_if_missing(
    name: str, workingset: Optional[Set[str]] = None, indexurl: Optional[str] = None
) -> Optional[Set[str]]:
    if workingset is None:
        workingset: Set[str] = {pkg.key for pkg in pkg_resources.working_set}
    _pip_install(name, indexurl) if name not in workingset else _no_op()
    return workingset


def pip_install_if_missing(
    name: Union[str, Iterable[str]],
    workingset: Optional[Set[str]] = None,
    indexurl: Optional[str] = None,
) -> None:
    if isinstance(name, str):
        name: Tuple[str] = (name,)
    else:
        name: Set[str] = set(name)
    for subname in name:
        workingset: Set[str] = _pip_install_if_missing(subname, workingset, indexurl)
