#!/bin/bash

function printUsage() {
	echo "Usage: ./buildapp.sh [options]"
	echo "  [-h --help help] - Prints usage instructions"
	echo "  [test]           - Development build with symbolic links to dev files"
	echo "  [no options]     - Builds final version"
}

if [[ "$#" -eq 1 ]]; then

	if [[ "$1" == "help" ]] || [[ "$1" == "-h" ]] || [[ "$1" == "--help" ]]; then
		printUsage

	elif [[ "$1" == "clean" ]]; then
		rm -rf build dist Scraper.zip

	elif [[ "$1" == "test" ]]; then
		python3 ./setup.py py2app -A

	elif [[ "$1" == "zip" ]] || [[ "$1" == "dist" ]] || [[ "$1" == "distribution" ]] || [[ "$1" == "archive" ]]; then
		ditto -c -k --sequesterRsrc --keepParent dist Scraper.zip
	fi

elif [[ "$#" -eq 0 ]]; then
	python3 setup.py py2app
else
	printUsage
fi



