import argparse
from lxml import etree
from oaipmh_scythe import Scythe


def fetch_data_from_scythe(im_endpoint, func, *args, **kwargs):
    """Fetch data from Scythe."""
    try:
        with Scythe(im_endpoint) as scythe:
            result = func(scythe, *args, **kwargs)
            # Force generator evaluation to catch errors early
            if hasattr(result, '__iter__') and not isinstance(result, (str, bytes, dict)):
                return list(result)
            return result
    except Exception as e:
        print(f"{type(e).__name__}: {e}")
        return None


def identify(im_endpoint):
    """Harvest repository identity information."""
    identify_response = fetch_data_from_scythe(im_endpoint, lambda scythe: scythe.identify())
    if identify_response:
        print("Identify response:")
        print(etree.tostring(identify_response.xml, pretty_print=True, encoding="unicode"))


def list_metadata_formats(im_endpoint, identifier=None):
    """Harvest available metadata formats."""
    metadata_formats = fetch_data_from_scythe(im_endpoint, lambda scythe: scythe.list_metadata_formats(identifier))
    if metadata_formats:
        print("\nMetadata formats:")
        for metadata_format in metadata_formats:
            print(etree.tostring(metadata_format.xml, pretty_print=True, encoding="unicode"))


def list_identifiers(im_endpoint, metadata_prefix, from_date=None, until=None, set_name=None):
    """Harvest available identifiers."""
    identifiers = fetch_data_from_scythe(
        im_endpoint,
        lambda scythe: scythe.list_identifiers(
            metadata_prefix=metadata_prefix,
            from_=from_date,
            until=until,
            set_=set_name
        )
    )
    if identifiers:
        print("\nIdentifiers:")
        for identifier in identifiers:
            print(etree.tostring(identifier.xml, pretty_print=True, encoding="unicode"))


def list_sets(im_endpoint):
    """Harvest available sets."""
    sets = fetch_data_from_scythe(im_endpoint, lambda scythe: scythe.list_sets())
    if sets:
        print("List sets:")
        for set_item in sets:
            print(etree.tostring(set_item.xml, pretty_print=True, encoding="unicode"))


def get_record(im_endpoint, identifier, metadata_prefix):
    """Harvest a specific record."""
    record = fetch_data_from_scythe(
        im_endpoint,
        lambda scythe: scythe.get_record(identifier=identifier, metadata_prefix=metadata_prefix)
    )
    if record:
        print("Get record:")
        print(etree.tostring(record.xml, pretty_print=True, encoding="unicode"))


def list_records(im_endpoint, metadata_prefix, from_date=None, until=None, set_name=None):
    """Harvest all records."""
    records = fetch_data_from_scythe(
        im_endpoint,
        lambda scythe: scythe.list_records(
            from_=from_date,
            until=until,
            metadata_prefix=metadata_prefix,
            set_=set_name
        )
    )
    if records:
        print("List records:")
        for record in records:
            print(etree.tostring(record.xml, pretty_print=True, encoding="unicode"))


def get_arg_parser():
    parser = argparse.ArgumentParser(description='OAI-PMH client for Infrastructure Manager (https://im.egi.eu/im-dashboard/)')
    parser.add_argument("--im-endpoint", required=True, help="Infrastructure Manager OAI-PMH endpoint")
    subparsers = parser.add_subparsers(dest='command')

    subparsers.add_parser('identify', help='Retrieve repository information')

    # List Identifiers arguments
    list_identifiers_parser = subparsers.add_parser('list_identifiers', help='Retrieve all available identifiers of the records in the repository')
    list_identifiers_parser.add_argument("metadata_prefix", help="Required. Metadata prefix (e.g., oai_dc) of the identifiers to retrieve")
    list_identifiers_parser.add_argument("--from", dest="from_date", help="Optional. Lower bound datestamps of the records to retrieve in YYYY-MM-DD format")
    list_identifiers_parser.add_argument("--until", help="Optional. Upper bound datestamps of the records to retrieve in YYYY-MM-DD format")
    list_identifiers_parser.add_argument("--set", dest="set_name", help="Optional. Set of the records to retrieve")

    # List Metadata Formats arguments
    list_metadata_formats_parser = subparsers.add_parser("list_metadata_formats", help="Retrieve all available metadata formats in the repository")
    list_metadata_formats_parser.add_argument("identifier", nargs="?", help="Optional record identifier")

    # Get Record arguments
    get_record_parser = subparsers.add_parser("get_record", help="Retrieve a specific record from the repository")
    get_record_parser.add_argument("identifier", help="Required. Identifier of the record to retrieve")
    get_record_parser.add_argument("metadata_prefix", help="Required. Metadata prefix (e.g., oai_dc)")

    # List Sets arguments
    subparsers.add_parser('list_sets', help='Retrieve the set structure of the repository')

    # List Records arguments
    list_records_parser = subparsers.add_parser("list_records", help="Retrieve all records available in the repository")
    list_records_parser.add_argument("metadata_prefix", help="Required. Metadata prefix (e.g., oai_dc) of the records to retrieve")
    list_records_parser.add_argument("--from", dest="from_date", help="Optional. Lower bound datestamps of the records to retrieve in YYYY-MM-DD format")
    list_records_parser.add_argument("--until", help="Optional. Upper bound datestamps of the records to retrieve in YYYY-MM-DD format")
    list_records_parser.add_argument("--set", dest="set_name", help="Optional. Set of the records to retrieve")

    return parser


if __name__ == '__main__':
    parser = get_arg_parser()
    args = parser.parse_args()

    im_endpoint = args.im_endpoint

    if args.command == 'identify':
        identify(im_endpoint)
    elif args.command == 'list_metadata_formats':
        list_metadata_formats(im_endpoint, identifier=args.identifier)
    elif args.command == 'list_identifiers':
        list_identifiers(im_endpoint, metadata_prefix=args.metadata_prefix, from_date=args.from_date, until=args.until, set_name=args.set_name)
    elif args.command == 'list_sets':
        list_sets(im_endpoint)
    elif args.command == 'get_record':
        get_record(im_endpoint, identifier=args.identifier, metadata_prefix=args.metadata_prefix)
    elif args.command == 'list_records':
        list_records(im_endpoint, metadata_prefix=args.metadata_prefix, from_date=args.from_date, until=args.until, set_name=args.set_name)
    else:
        parser.print_help()