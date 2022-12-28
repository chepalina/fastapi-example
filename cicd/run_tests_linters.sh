#!/bin/sh

PROJECT_DIR=$1 ;
if [ -z $PROJECT_DIR ]; then
    PROJECT_DIR=$(pwd)
fi

PYTHON_DIRS=$(find $PROJECT_DIR -type f -name '__init__.py' -mindepth 2 -maxdepth 2 -exec dirname "{}" \;);
PYTHON_SCRIPTS=$(find $PROJECT_DIR -type f -name '*.py' -maxdepth 1);
PYTHON_PATHS="$PYTHON_DIRS $PYTHON_SCRIPTS"

RESULT_CODE=0 ;
UTILS_WITH_ERROR="";

echo RUN pytest;
pytest tests \
|| { RESULT_CODE=1; UTILS_WITH_ERROR="$UTILS_WITH_ERROR pytest"; }

echo RUN black ;
black $PYTHON_PATHS --check\
|| { RESULT_CODE=1; UTILS_WITH_ERROR="$UTILS_WITH_ERROR black"; }

echo RUN isort ;
isort $PYTHON_PATHS --check-only\
|| { RESULT_CODE=1; UTILS_WITH_ERROR="$UTILS_WITH_ERROR isort"; }

echo RUN pylint ;
pylint --rcfile=$PROJECT_DIR/pyproject.toml $PYTHON_PATHS\
|| { RESULT_CODE=1; UTILS_WITH_ERROR="$UTILS_WITH_ERROR pylint"; }

echo RUN pycodestyle ;
pycodestyle $PYTHON_PATHS\
|| { RESULT_CODE=1; UTILS_WITH_ERROR="$UTILS_WITH_ERROR pycodestyle"; }

echo RUN pydocstyle ;
pydocstyle $PYTHON_PATHS\
|| { RESULT_CODE=1; UTILS_WITH_ERROR="$UTILS_WITH_ERROR pydocstyle"; }

echo RUN mypy ;
mypy $PYTHON_PATHS --cache-dir=/dev/null --config-file=$PROJECT_DIR/pyproject.toml\
|| { RESULT_CODE=1; UTILS_WITH_ERROR="$UTILS_WITH_ERROR mypy"; }

echo "RESULT_CODE = $RESULT_CODE";
echo "UTILS_WITH_ERROR =$UTILS_WITH_ERROR";
exit $RESULT_CODE
