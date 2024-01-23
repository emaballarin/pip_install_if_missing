#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess
import sys
from typing import List
from typing import Optional
from typing import Set
from typing import Tuple

import pkg_resources

__all__ = ["pip_install_if_missing"]


def _no_op(*args, **kwargs) -> None:
    _ = args
    _ = kwargs
    del _


def _pip_install(
    name: str,
    upgrade: bool = False,
    nodeps: bool = False,
    force: bool = False,
    indexurl: Optional[str] = None,
) -> None:
    preargs: List[str] = []
    postargs: List[str] = []
    preargs.append("--upgrade") if upgrade else _no_op()
    preargs.append("--no-deps") if nodeps else _no_op()
    preargs.append("--force") if force else _no_op()
    postargs.extend(("--index-url", indexurl)) if indexurl is not None else _no_op()
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", *preargs, name, *postargs],
        stdout=subprocess.DEVNULL,
    )


def _get_workingset() -> Set[str]:
    return {pkg.key.lower() for pkg in pkg_resources.working_set}


def _pip_install_if_missing(
    name: str,
    upgrade: bool = False,
    nodeps: bool = False,
    force: bool = False,
    indexurl: Optional[str] = None,
    workingset: Optional[Set[str]] = None,
) -> Set[str]:
    if upgrade or force:
        _pip_install(
            name=name, upgrade=upgrade, nodeps=nodeps, force=force, indexurl=indexurl
        )
    else:
        workingset: Set[str] = _get_workingset() if workingset is None else workingset
        _pip_install(
            name=name, upgrade=upgrade, nodeps=nodeps, force=force, indexurl=indexurl
        ) if name.lower() not in workingset else _no_op()

    return _get_workingset()


def pip_install_if_missing(
    name: str,
    upgrade: bool = False,
    nodeps: bool = False,
    force: bool = False,
    indexurl: Optional[str] = None,
    strictorder=False,
    workingset: Optional[Set[str]] = None,
) -> None:
    if isinstance(name, str):
        name: Tuple[str] = (name,)
    elif strictorder:
        name: Tuple[str, ...] = tuple(name)
    else:
        name: Set[str] = set(name)
    for subname in name:
        workingset: Set[str] = _pip_install_if_missing(
            name=subname,
            upgrade=upgrade,
            nodeps=nodeps,
            force=force,
            indexurl=indexurl,
            workingset=workingset,
        )
