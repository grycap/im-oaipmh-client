# OAI-PMH Client for Infrastructure Manager (IM)

This Python client is designed to interact with the **Infrastructure Manager (IM)** repository via the **OAI-PMH (Open Archives Initiative Protocol for Metadata Harvesting)** interface. It provides various commands to harvest metadata, including repository information, available identifiers, metadata formats, sets, and records.


## Features

- Retrieve repository identity information (`identify`).
- List available metadata formats (`list_metadata_formats`).
- List available identifiers (`list_identifiers`).
- List available sets (`list_sets`).
- Retrieve specific records (`get_record`).
- List all available records (`list_records`).


## Prerequisites

- Python 3.x
- `lxml` library (for XML parsing)
- `oaipmh_scythe` library (for interacting with the OAI-PMH interface)

You can install the required dependencies using `pip`:

```bash
pip install lxml oaipmh_scythe
```


## Setup

Clone this repository and navigate into the project directory:

```bash
git clone <repository_url>
cd <project_directory>
```


## Usage
The script supports various commands through the command line interface (CLI). Below is a list of the available commands and their arguments:

1. **identify**  
Retrieve repository identity information.

    ```bash
    python3 oaim-client.py identify
    ```


2. **list_metadata_formats**  
Retrieve all available metadata formats in the repository.

    ```bash
    python3 oaim-client.py list_metadata_formats [identifier]
    ```
    - `identifier`: Optional. Specify the record identifier to filter the metadata formats.


3. **list_identifiers**  
Retrieve all available record identifiers in the repository.

    ```bash
    python3 oaim-client.py list_identifiers <metadata_prefix> [--from <from_date>] [--until <until_date>] [--set <set_name>]
    ```

    - `metadata_prefix`: Required. The metadata prefix (e.g., oai_dc).

    - `from_date`: Optional. Lower bound of datestamps (YYYY-MM-DD).

    - `until`: Optional. Upper bound of datestamps (YYYY-MM-DD).

    - `set_name`: Optional. Set of records to retrieve.

4. **list_sets**  
Retrieve the set structure of the repository.

    ```bash
    python3 oaim-client.py list_sets
    ```

5. **get_record**  
Retrieve a specific record from the repository.

    ```bash
    python3 oaim-client.py get_record <identifier> <metadata_prefix>
    ```

    - `identifier`: Required. The identifier of the record to retrieve.

    - `metadata_prefix`: Required. The metadata prefix (e.g., oai_dc).

6. **list_records**  
Retrieve all records available in the repository.

    ```bash
    python3 oaim-client.py list_records <metadata_prefix> [--from <from_date>] [--until <until_date>] [--set <set_name>]
    ```

    - `metadata_prefix`: Required. The metadata prefix (e.g., oai_dc).

    - `from_date`: Optional. Lower bound of datestamps (YYYY-MM-DD).

    - `until`: Optional. Upper bound of datestamps (YYYY-MM-DD).

    - `set_name`: Optional. Set of records to retrieve.


## Example
To retrieve repository identity information:

```bash
python3 oaim-client.py identify
```

To list available metadata formats for a specific identifier:

```bash
python3 oaim-client.py list_metadata_formats
```

To retrieve all records with metadata prefix oai_dc:

```bash
python3 oaim-client.py list_records oai_dc --from 2020-01-21
```
