import pathlib

INPUT_DATA_DIR_PATH = pathlib.Path(__file__).parent.resolve()
AUTHORITY_TABLES_DIR_PATH = INPUT_DATA_DIR_PATH / "authority_tables"
DEPENDENCIES_PREFIX_DIR_PATH = INPUT_DATA_DIR_PATH / "dependencies_prefix"
COUNTRIES_SKOS_FILE_PATH = AUTHORITY_TABLES_DIR_PATH / "countries-skos.rdf"

PREFIX_DEFINITION_FILE_PATH = DEPENDENCIES_PREFIX_DIR_PATH / "prefix_definition.csv"