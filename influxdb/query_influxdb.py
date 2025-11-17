#!/usr/bin/env python3
"""
Query InfluxDB v2 to retrieve all different fields in a specified bucket.

This script connects to an InfluxDB v2 instance and retrieves all unique field names
from the specified bucket. Optionally, it can also retrieve all distinct topics/tags.

Usage:
    python query_influxdb.py <bucket_name> <influx_token> <fqdn> <port> [--org <org_name>] [--topics] [--json]
    
Example:
    python query_influxdb.py my_bucket my_secret_token fqdn.de 18086
    python query_influxdb.py my_bucket my_secret_token fqdn.de 18086 --org my_org
    python query_influxdb.py my_bucket my_secret_token fqdn.de 18086 --topics
    python query_influxdb.py my_bucket my_secret_token fqdn.de 18086 --topics --json
"""

import argparse
import sys
from typing import Set, List
from influxdb_client import InfluxDBClient
from influxdb_client.client.flux_table import FluxTable


def get_all_fields(
    bucket_name: str,
    influx_token: str,
    org: str = "my-org",
    url: str = "https://fqdn.de:18086",
    verify_ssl: bool = False
) -> Set[str]:
    """
    Query InfluxDB v2 to get all unique field names in a bucket.
    
    Args:
        bucket_name: Name of the InfluxDB bucket to query
        influx_token: Authentication token for InfluxDB
        org: Organization name (default: "my-org")
        url: InfluxDB URL (default: "https://fqdn.de:18086")
        verify_ssl: Whether to verify SSL certificates (default: False)
        
    Returns:
        Set of unique field names found in the bucket
        
    Raises:
        Exception: If connection or query fails
    """
    
    # Create InfluxDB client
    client = InfluxDBClient(
        url=url,
        token=influx_token,
        org=org,
        verify_ssl=verify_ssl
    )
    
    try:
        # Query to get all unique field names using Flux
        query = f'''
from(bucket: "{bucket_name}")
  |> range(start: -30d)
  |> keys(except: ["_start", "_stop", "_time"])
  |> filter(fn: (x) => x._value == "string" or x._value == "boolean" or x._value == "long" or x._value == "double" or x._value == "int" or x._value == "uint")
  |> group(columns: ["_value"])
  |> distinct(column: "_value")
  |> keep(columns: ["_value"])
'''
        
        # Alternative simpler query - get all fields
        query = f'''
import "influxdata/influxdb/v1" as v1

v1.tagValues(bucket: "{bucket_name}", tag: "_field")
'''
        
        # Use the query method with Flux query
        query_api = client.query_api()
        
        tables = query_api.query(query)
        
        fields: Set[str] = set()
        
        # Extract field names from the query results
        for table in tables:
            for record in table.records:
                field_name = record.values.get("_value")
                if field_name:
                    fields.add(field_name)
        
        return fields
        
    finally:
        client.close()


def get_all_fields_v2(
    bucket_name: str,
    influx_token: str,
    org: str = "my-org",
    url: str = "https://fqdn.de:18086",
    verify_ssl: bool = False
) -> List[str]:
    """
    Alternative method to get all fields using bucket schema API.
    
    Args:
        bucket_name: Name of the InfluxDB bucket to query
        influx_token: Authentication token for InfluxDB
        org: Organization name (default: "my-org")
        url: InfluxDB URL (default: "https://fqdn.de:18086")
        verify_ssl: Whether to verify SSL certificates (default: False)
        
    Returns:
        List of unique field names found in the bucket
    """
    
    from influxdb_client.client.write_api import SYNCHRONOUS
    
    client = InfluxDBClient(
        url=url,
        token=influx_token,
        org=org,
        verify_ssl=verify_ssl
    )
    
    try:
        query_api = client.query_api()
        
        # Query to get all measurement + field combinations
        flux_query = f'''
from(bucket: "{bucket_name}")
  |> range(start: -7d)
  |> group(columns: ["_field"])
  |> distinct(column: "_field")
  |> keep(columns: ["_field"])
  |> sort(columns: ["_field"])
'''
        
        tables = query_api.query(flux_query)
        
        fields: List[str] = []
        seen: Set[str] = set()
        
        for table in tables:
            for record in table.records:
                field = record["_field"]
                if field and field not in seen:
                    fields.append(field)
                    seen.add(field)
        
        return sorted(fields)
        
    finally:
        client.close()


def get_all_topics(
    bucket_name: str,
    influx_token: str,
    org: str = "my-org",
    url: str = "https://fqdn.de:18086",
    verify_ssl: bool = False
) -> List[str]:
    """
    Get all distinct topics/tags in a bucket.
    
    Args:
        bucket_name: Name of the InfluxDB bucket to query
        influx_token: Authentication token for InfluxDB
        org: Organization name (default: "my-org")
        url: InfluxDB URL (default: "https://fqdn.de:18086")
        verify_ssl: Whether to verify SSL certificates (default: False)
        
    Returns:
        List of unique topic/tag keys found in the bucket
    """
    
    client = InfluxDBClient(
        url=url,
        token=influx_token,
        org=org,
        verify_ssl=verify_ssl
    )
    
    try:
        query_api = client.query_api()
        
        # Query to get all distinct tag keys (excluding system columns)
        flux_query = f'''
from(bucket: "{bucket_name}")
  |> range(start: -7d)
  |> group(columns:["topic", "_field"])
  |> keys()
  |> filter(fn: (r) => r._value != "_time" and r._value != "_value" and r._value != "_field" and r._value != "_measurement" and r._value != "_start" and r._value != "_stop")
  |> unique(column: "_value")
'''
        
        tables = query_api.query(flux_query)
        
        topics: List[str] = []
        seen: Set[str] = set()
        
        for table in tables:
            for record in table.records:
                topic = record.values.get("_value")
                if topic and topic not in seen:
                    topics.append(topic)
                    seen.add(topic)
        
        return sorted(topics)
        
    finally:
        client.close()


def main():
    """Main entry point for the script."""
    
    parser = argparse.ArgumentParser(
        description="Query InfluxDB v2 to retrieve all fields in a bucket",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Query fields (default)
  python query_influxdb.py my_bucket my_token_here fqdn.de 18086
  
  # Query fields with specific organization
  python query_influxdb.py my_bucket my_token_here fqdn.de 18086 --org my_organization
  
  # Query topics/tags instead of fields
  python query_influxdb.py my_bucket my_token_here fqdn.de 18086 --topics
  
  # Query with JSON output
  python query_influxdb.py my_bucket my_token_here fqdn.de 18086 --json
  
  # Query topics with JSON output
  python query_influxdb.py my_bucket my_token_here fqdn.de 18086 --topics --json
  
  # Query with SSL verification
  python query_influxdb.py my_bucket my_token_here fqdn.de 18086 --verify-ssl
        """
    )
    
    parser.add_argument(
        "bucket",
        help="InfluxDB bucket name"
    )
    
    parser.add_argument(
        "token",
        help="InfluxDB authentication token"
    )
    
    parser.add_argument(
        "fqdn",
        help="InfluxDB server FQDN (e.g., fqdn.de or influxdb.example.com)"
    )
    
    parser.add_argument(
        "port",
        type=int,
        help="InfluxDB server port (e.g., 18086)"
    )
    
    parser.add_argument(
        "--org",
        default="my-org",
        help="InfluxDB organization name (default: my-org)"
    )
    
    parser.add_argument(
        "--verify-ssl",
        action="store_true",
        help="Verify SSL certificates (default: False)"
    )
    
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON array"
    )
    
    parser.add_argument(
        "--topics",
        action="store_true",
        help="Query distinct topics/tags instead of fields"
    )
    
    args = parser.parse_args()
    
    try:
        # Construct the URL from fqdn and port
        url = f"https://{args.fqdn}:{args.port}"
        
        print(f"Connecting to InfluxDB at {url}...", file=sys.stderr)
        
        if args.topics:
            print(f"Querying topics in bucket: {args.bucket}", file=sys.stderr)
            
            topics = get_all_topics(
                bucket_name=args.bucket,
                influx_token=args.token,
                org=args.org,
                url=url,
                verify_ssl=args.verify_ssl
            )
            
            if not topics:
                print("No topics found in the bucket.", file=sys.stderr)
                return 1
            
            print(f"\nFound {len(topics)} unique topics:\n", file=sys.stderr)
            
            if args.json:
                import json
                print(json.dumps(topics))
            else:
                for topic in topics:
                    print(topic)
        else:
            print(f"Querying bucket: {args.bucket}", file=sys.stderr)
            
            fields = get_all_fields_v2(
                bucket_name=args.bucket,
                influx_token=args.token,
                org=args.org,
                url=url,
                verify_ssl=args.verify_ssl
            )
            
            if not fields:
                print("No fields found in the bucket.", file=sys.stderr)
                return 1
            
            print(f"\nFound {len(fields)} unique fields:\n", file=sys.stderr)
            
            if args.json:
                import json
                print(json.dumps(fields))
            else:
                for field in fields:
                    print(field)
        
        return 0
        
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
