Plaintext file that contains patterns of paths to ignore (one pattern per line) when committing/pushing.

**Use this to enforce the DONTs!**

### Examples:
`config.yaml` - any file named `config.yaml`
`__pycache__/` - anything in the `__pycache__/` directory
`*.py[cod]` - any file with the extension `.pyc`, `.pyo`, or `.pyd`
`**/output` - anything in any directory called `output`

May have multiple .gitignore files for subdirectories