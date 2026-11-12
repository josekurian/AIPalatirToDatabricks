#!/usr/bin/env python3
"""
Automated Foundry-to-Databricks Code Converter
Parses Palantir Foundry PySpark transforms (@transform, @transform_df, Input, Output)
and converts them into native Databricks Delta Live Tables (DLT) or standard PySpark jobs.
"""

import re
import sys
import os

def convert_foundry_to_dlt(foundry_code: str) -> str:
    """
    Translates Foundry PySpark transforms to Databricks Delta Live Tables (DLT).
    """
    lines = foundry_code.splitlines()
    output_lines = []
    
    output_lines.append("# Auto-converted from Palantir Foundry Code Repositories to Databricks DLT")
    output_lines.append("import dlt")
    output_lines.append("from pyspark.sql import functions as F")
    output_lines.append("from pyspark.sql.types import *")
    output_lines.append("")
    
    in_transform = False
    table_name = "target_table"
    inputs = []
    
    for line in lines:
        # Strip transform imports
        if "from transforms.api import" in line:
            continue
        if "@configure" in line:
            continue
            
        # Match Output locator
        out_match = re.search(r'Output\(["\'](.+?)["\']\)', line)
        if out_match:
            raw_path = out_match.group(1)
            table_name = raw_path.strip("/").split("/")[-1].lower()
            
        # Match Input locators
        in_match = re.search(r'(\w+)\s*=\s*Input\(["\'](.+?)["\']\)', line)
        if in_match:
            var_name = in_match.group(1)
            in_path = in_match.group(2).strip("/").split("/")[-1].lower()
            inputs.append((var_name, in_path))
            
        # Function definition
        func_match = re.search(r'def\s+(\w+)\s*\((.*?)\):', line)
        if func_match:
            in_transform = True
            output_lines.append(f'@dlt.table(')
            output_lines.append(f'    name="{table_name}",')
            output_lines.append(f'    comment="Migrated from Palantir Foundry transform: {table_name}",')
            output_lines.append(f'    table_properties={{"quality": "gold"}}')
            output_lines.append(f')')
            output_lines.append(f'def {table_name}():')
            
            # Inject dlt.read for inputs
            for var_name, in_path in inputs:
                output_lines.append(f'    {var_name} = dlt.read("{in_path}")')
            inputs = []
            continue
            
        if in_transform:
            output_lines.append(line)
            
    return "\n".join(output_lines)

if __name__ == "__main__":
    sample_foundry_file = "/Users/josekurian/GoogleAutomation/AIPalatirToDatabricks/Palantir/code_repositories/customer_supply_chain_transforms.py"
    if os.path.exists(sample_foundry_file):
        with open(sample_foundry_file, "r") as f:
            code = f.read()
        converted = convert_foundry_to_dlt(code)
        
        target_path = "/Users/josekurian/GoogleAutomation/AIPalatirToDatabricks/Migrations/code_converters/converted_dlt_sample.py"
        with open(target_path, "w") as out:
            out.write(converted)
        print(f"Successfully converted Foundry transform to DLT: {target_path}")
