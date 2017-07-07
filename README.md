# Find Penguins Parser
This project contains tree scripts for transforming Find Penguins Trips Into PDFs or HTML Documents.

## Downloading Trips
The first script is the `penguin_parser.py` which requires two arguments, the storage path and the trip. This script will download all footprints, including text and images from the given trip into the given directory.
Usage:
```
python3 penguin_parser.py <path-to-local-storage-directory> "<find-penguins-user>/trip/<trip-name>"
```

After termination, the storage path should contain folders for the days inside of which folders for the different footprints are located. These folders contain the images as well as a json file for the meta information.

## Generators
At the moment, two generators exist. These generators are supposed to take the data inside of the previously created storage directory and convert it into another representation.
Generators expect two arguments, the storage path and the trip title. The latter is free text.

* `pdf_generator.py` creates a PDF
* `html_generator.py`creates a HTML document

Usage:
```
python3 pdf_generator.py <path-to-local-storage-directory> "<your-trip-title>"
```

## Requirements
All scripts require Python 3 and the requirements, specified in the `requirements.txt`.
