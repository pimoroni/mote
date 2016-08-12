#!/bin/bash

# function declarations

success() {
    echo "$(tput setaf 2)$1$(tput sgr0)"
}

warning() {
    echo "$(tput setaf 1)$1$(tput sgr0)"
}

newline() {
    echo ""
}

module="mote"
script="mote-demo.py"

# check for pyinstaller

if command -v pyinstaller > /dev/null; then
    success "PyInstaller found"
elif [ -f ./env/bin/activate ]; then
    warning "PyInstaller was not found but a virtualenv was"
    warning "Could it be that it is not activated?"
    echo "Try 'source ./env/bin/activate && ./build.sh'" && newline
    exit 1
else
    warning "PyInstaller was not found"
    exit 1
fi

# check for module

if ! python -c "import $module" 2>&1 >/dev/null | grep "No module named $module"; then
    success "$module module found"
elif [ -f ./env/bin/activate ]; then
    warning "The $module module was not found but a virtualenv was"
    warning "Could it be that it is not activated?"
    echo "Try 'source ./env/bin/activate && ./build.sh'" && newline
    exit 1
else
    warning "$module module was not found"
    exit 1
fi

pyinstaller --clean --onefile ./$script
success "binary created in ./dist"

exit 0
