# IM - Infrastructure Manager
# Copyright (C) 2025 - GRyCAP - Universitat Politecnica de Valencia
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import argparse
from lxml import etree
from oaipmh_scythe import Scythe


class OAIPMHClient:

    @staticmethod
    def fetch_data_from_scythe(im_endpoint, func, *args, **kwargs):
        """Fetch data from Scythe."""
        with Scythe(im_endpoint) as scythe:
            return func(scythe, *args, **kwargs)

    @staticmethod
    def identify(im_endpoint):
        """Harvest repository identity information."""
        try:
            identify_response = OAIPMHClient.fetch_data_from_scythe(
                im_endpoint, lambda scythe: scythe.identify()
            )
            if identify_response:
                print("Identify response:")
                print(
                    etree.tostring(
                        identify_response.xml,
                        pretty_print=True,
                        encoding="unicode"
                    )
                )
        except Exception as e:
            print(f"{type(e).__name__}: {e}")

    @staticmethod
    def list_metadata_formats(im_endpoint, identifier=None):
        """Harvest available metadata formats."""
        try:
            metadata_formats = OAIPMHClient.fetch_data_from_scythe(
                im_endpoint,
                lambda scythe: scythe.list_metadata_formats(identifier)
            )
            if metadata_formats:
                print("\nMetadata formats:")
                for metadata_format in metadata_formats:
                    print(
                        etree.tostring(
                            metadata_format.xml,
                            pretty_print=True,
                            encoding="unicode"
                        )
                    )
        except Exception as e:
            print(f"{type(e).__name__}: {e}")

    @staticmethod
    def list_identifiers(
        im_endpoint, metadata_prefix, from_date=None, until=None, set_name=None
    ):
        """Harvest available identifiers."""
        try:
            identifiers = OAIPMHClient.fetch_data_from_scythe(
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
                    print(
                        etree.tostring(
                            identifier.xml,
                            pretty_print=True,
                            encoding="unicode"
                        )
                    )
        except Exception as e:
            print(f"{type(e).__name__}: {e}")

    @staticmethod
    def list_sets(im_endpoint):
        """Harvest available sets."""
        try:
            sets = OAIPMHClient.fetch_data_from_scythe(
                im_endpoint, lambda scythe: scythe.list_sets()
            )
            if sets:
                print("List sets:")
                for set_item in sets:
                    print(
                        etree.tostring(
                            set_item.xml,
                            pretty_print=True,
                            encoding="unicode"
                        )
                    )
        except Exception as e:
            print(f"{type(e).__name__}: {e}")

    @staticmethod
    def get_record(im_endpoint, identifier, metadata_prefix):
        """Harvest a specific record."""
        try:
            record = OAIPMHClient.fetch_data_from_scythe(
                im_endpoint,
                lambda scythe: scythe.get_record(
                    identifier=identifier,
                    metadata_prefix=metadata_prefix
                )
            )
            if record:
                print("Get record:")
                print(
                    etree.tostring(
                        record.xml,
                        pretty_print=True,
                        encoding="unicode"
                    )
                )
        except Exception as e:
            print(f"{type(e).__name__}: {e}")

    @staticmethod
    def list_records(
        im_endpoint, metadata_prefix, from_date=None, until=None, set_name=None
    ):
        """Harvest all records."""
        try:
            records = OAIPMHClient.fetch_data_from_scythe(
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
                    print(
                        etree.tostring(
                            record.xml,
                            pretty_print=True,
                            encoding="unicode"
                        )
                    )
        except Exception as e:
            print(f"{type(e).__name__}: {e}")


def get_arg_parser():
    parser = argparse.ArgumentParser(
        description=(
            'OAI-PMH client for Infrastructure Manager '
            '(https://im.egi.eu/im-dashboard/)'
        )
    )
    parser.add_argument(
        "--im-endpoint",
        required=True,
        help="Infrastructure Manager OAI-PMH endpoint"
    )
    subparsers = parser.add_subparsers(dest='command')

    subparsers.add_parser(
        'identify',
        help='Retrieve repository information'
    )

    # List Identifiers arguments
    list_identifiers_parser = subparsers.add_parser(
        'list_identifiers',
        help=(
            'Retrieve all available identifiers of the records in the '
            'repository'
        )
    )
    list_identifiers_parser.add_argument(
        "metadata_prefix",
        help=(
            "Required. Metadata prefix (e.g., oai_dc) of the identifiers "
            "to retrieve"
        )
    )
    list_identifiers_parser.add_argument(
        "--from",
        dest="from_date",
        help=(
            "Optional. Lower bound datestamps of the records to retrieve "
            "in YYYY-MM-DD format"
        )
    )
    list_identifiers_parser.add_argument(
        "--until",
        help=(
            "Optional. Upper bound datestamps of the records to retrieve "
            "in YYYY-MM-DD format"
        )
    )
    list_identifiers_parser.add_argument(
        "--set",
        dest="set_name",
        help="Optional. Set of the records to retrieve"
    )

    # List Metadata Formats arguments
    list_metadata_formats_parser = subparsers.add_parser(
        "list_metadata_formats",
        help="Retrieve all available metadata formats in the repository"
    )
    list_metadata_formats_parser.add_argument(
        "identifier",
        nargs="?",
        help="Optional record identifier"
    )

    # Get Record arguments
    get_record_parser = subparsers.add_parser(
        "get_record",
        help="Retrieve a specific record from the repository"
    )
    get_record_parser.add_argument(
        "identifier",
        help="Required. Identifier of the record to retrieve"
    )
    get_record_parser.add_argument(
        "metadata_prefix",
        help="Required. Metadata prefix (e.g., oai_dc)"
    )

    # List Sets arguments
    subparsers.add_parser(
        'list_sets',
        help='Retrieve the set structure of the repository'
    )

    # List Records arguments
    list_records_parser = subparsers.add_parser(
        "list_records",
        help="Retrieve all records available in the repository"
    )
    list_records_parser.add_argument(
        "metadata_prefix",
        help=(
            "Required. Metadata prefix (e.g., oai_dc) of the records "
            "to retrieve"
        )
    )
    list_records_parser.add_argument(
        "--from",
        dest="from_date",
        help=(
            "Optional. Lower bound datestamps of the records to retrieve "
            "in YYYY-MM-DD format"
        )
    )
    list_records_parser.add_argument(
        "--until",
        help=(
            "Optional. Upper bound datestamps of the records to retrieve "
            "in YYYY-MM-DD format"
        )
    )
    list_records_parser.add_argument(
        "--set",
        dest="set_name",
        help="Optional. Set of the records to retrieve"
    )

    return parser


def main():
    parser = get_arg_parser()
    args = parser.parse_args()

    if args.command == 'identify':
        OAIPMHClient.identify(args.im_endpoint)
    elif args.command == 'list_metadata_formats':
        OAIPMHClient.list_metadata_formats(args.im_endpoint,
                                           identifier=args.identifier)
    elif args.command == 'list_identifiers':
        OAIPMHClient.list_identifiers(
            args.im_endpoint,
            metadata_prefix=args.metadata_prefix,
            from_date=args.from_date,
            until=args.until,
            set_name=args.set_name
        )
    elif args.command == 'list_sets':
        OAIPMHClient.list_sets(args.im_endpoint)
    elif args.command == 'get_record':
        OAIPMHClient.get_record(
            args.im_endpoint,
            identifier=args.identifier,
            metadata_prefix=args.metadata_prefix
        )
    elif args.command == 'list_records':
        OAIPMHClient.list_records(
            args.im_endpoint,
            metadata_prefix=args.metadata_prefix,
            from_date=args.from_date,
            until=args.until,
            set_name=args.set_name
        )
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
