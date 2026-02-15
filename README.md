# Dictionary Builder (dicbuilder)

## Overview

**Dictionary Builder** is a Python-based utility designed to parse raw dictionary files (specifically in a format similar to Apertium `.dix` files) and populate a MySQL database with the structured data. It extracts lemmas, word forms, and morphological tags, maps the tags to a standardized format, and stores them for further linguistic processing or application usage.

## Features

-   **Custom Parsing Engine**: Utilizes a multiprocessing-capable parser (`SDParser`) to efficiently process large dictionary files.
-   **Database Integration**: Built on top of **SQLAlchemy** for robust database interactions, supporting table creation, data insertion, and resumption of interrupted builds.
-   **Morphological Tag Mapping**: detailed mapping system (`morphtypes.py`) to standardize language-specific tags (currently supporting Norwegian 'NO' and German 'DE') into a common format.
-   **Resumable Builds**: Includes logic to resume the database build process from a specific point, useful for large datasets.

## structure

-   `main.py`: The entry point of the application. Configures the database schema and initiates the build process.
-   `dictionary_builder.py`: Contains the `DictionaryBuilder` class, which orchestrates the parsing and database insertion.
-   `raw_parser.py`: Implements `SDParser`, a custom parser that uses multiprocessing to read and structure the raw text data.
-   `database_wrapper.py`: A wrapper around SQLAlchemy to handle common database operations like table creation and row fetching.
-   `morphtypes.py`: Defines the mapping rules for translating morphological tags from the source file to the database.
-   `utils.py`: Utility functions for URI creation, string manipulation, and timing.

## Requirements

-   Python 3.x
-   SQLAlchemy
-   regex

## Usage

The application is run from the command line and expects specific arguments for the database connection.

```bash
python main.py db_user db_pass db_host db_name
```

### Arguments:
1.  `db_user`: Database username
2.  `db_pass`: Database password
3.  `db_host`: Database host (e.g., localhost)
4.  `db_name`: Name of the database to use

### Configuration

Input file settings (filename, extension, language) are currently configured in `main.py`:

```python
LANG = load_tagname(0) # Defaults to 'NO' (Norwegian)
FILENAME = 'C'
EXT = 'dix'
DATA_DIR = 'data'
```

## Data Schema

The tool creates a table (default name based on input file) with the following schema:
-   `word_id`: Integer (Primary Key)
-   `word`: String (The word form)
-   `category_1` ... `category_12`: Strings (Morphological tags/categories)

## Developer Notes

-   **Concurrency**: The project uses `multiprocessing.Process` in `raw_parser.py` to handle data extraction.
-   **Extensibility**: New languages can be added by updating `TAGS` in `morphtypes.py`.
