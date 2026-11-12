#!/usr/bin/env python3
"""
Palantir Ontology to Databricks Unity Catalog DDL & Semantic Layer Converter
Parses Palantir Ontology JSON definitions and generates:
1. Databricks Unity Catalog SQL DDL
2. Primary & Foreign Key constraint relationships
3. ABAC Tagging and Masking statements
"""

import json
import sys
import os

def convert_ontology_to_databricks_sql(ontology_json_path: str) -> str:
    with open(ontology_json_path, "r") as f:
        data = json.load(f)

    ontology = data.get("ontology", {})
    ddl_statements = []
    
    ddl_statements.append("-- ========================================================================")
    ddl_statements.append(f"-- Automated Translation of Foundry Ontology: {ontology.get('apiName')}")
    ddl_statements.append("-- Target: Databricks Unity Catalog (Gold Layer)")
    ddl_statements.append("-- ========================================================================\n")
    
    type_mapping = {
        "string": "STRING",
        "double": "DOUBLE",
        "integer": "INT",
        "boolean": "BOOLEAN",
        "timestamp": "TIMESTAMP",
        "date": "DATE"
    }

    # 1. Object Types -> Delta Tables
    for obj in ontology.get("objectTypes", []):
        table_name = f"gold_{obj['apiName'].lower()}"
        primary_key = obj.get("primaryKey")
        ddl_statements.append(f"CREATE TABLE IF NOT EXISTS enterprise_operations.gold.{table_name} (")
        
        col_defs = []
        for prop_name, prop_spec in obj.get("properties", {}).items():
            spark_type = type_mapping.get(prop_spec.get("type"), "STRING")
            col_line = f"    {prop_name} {spark_type}"
            if prop_name == primary_key:
                col_line += " NOT NULL"
            col_defs.append(col_line)
            
        if primary_key:
            col_defs.append(f"    CONSTRAINT pk_{table_name} PRIMARY KEY ({primary_key})")
            
        ddl_statements.append(",\n".join(col_defs))
        ddl_statements.append(")")
        ddl_statements.append("USING DELTA")
        ddl_statements.append(f"COMMENT '{obj.get('displayName')} - Migrated from Palantir Ontology';\n")

    # 2. Link Types -> Foreign Keys
    for link in ontology.get("linkTypes", []):
        src_table = f"gold_{link['sourceObjectType'].lower()}"
        tgt_table = f"gold_{link['targetObjectType'].lower()}"
        fk_col = link.get("foreignKey")
        link_name = link.get("apiName")
        
        ddl_statements.append(
            f"ALTER TABLE enterprise_operations.gold.{src_table} "
            f"ADD CONSTRAINT fk_{link_name} FOREIGN KEY ({fk_col}) "
            f"REFERENCES enterprise_operations.gold.{tgt_table}({fk_col});"
        )
        
    return "\n".join(ddl_statements)

if __name__ == "__main__":
    spec_path = "/Users/josekurian/GoogleAutomation/AIPalatirToDatabricks/Palantir/ontology_definitions/enterprise_ontology_spec.json"
    if os.path.exists(spec_path):
        sql_out = convert_ontology_to_databricks_sql(spec_path)
        target_path = "/Users/josekurian/GoogleAutomation/AIPalatirToDatabricks/Migrations/code_converters/generated_unity_catalog_from_ontology.sql"
        with open(target_path, "w") as out:
            out.write(sql_out)
        print(f"Successfully converted Ontology to Unity Catalog SQL: {target_path}")
