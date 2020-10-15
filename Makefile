# HexLang by Alexander Abraham
# licensed under the MIT license
build: ; python setup.py sdist
install: ; python -m pip uninstall HexLang && python -m pip install git+https://github.com/RealAAbraham/HexLang.git
clean: ; rm -rf *egg-info build dist hexlang/*.c hexlang/__pycache__ *.html
