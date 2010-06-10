#!/usr/bin/env python

import re, sys, os

# Extend PYTHONPATH with 'lib'
sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), os.pardir, "lib")))

from narcissus.Tokenizer import Tokenizer
from narcissus.Statements import Script, CompilerContext


def parse(source, filename=None):
    """Parse some Javascript

    Args:
        source: the Javascript source, as a string
        filename: the filename to include in messages
    Returns:
        the parsed source code data structure
    Raises:
        ParseError
    """
    tokenizer = Tokenizer(source, filename)
    root = Script(tokenizer, CompilerContext(False))
    
    if not tokenizer.done:
        raise tokenizer.newSyntaxError("Syntax error")
        
    return root


if __name__ == "__main__":
    print parse(file(sys.argv[1]).read(),sys.argv[1]).toJson()
