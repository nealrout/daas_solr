from lxml import etree
import re

sql_script_dir = rf"D:\src\github\daas_db\sql\table"
sql_table_input = rf"{sql_script_dir}\table_account.sql"
solr_scheme_out_dir = rf"D:\src\github\daas_solr\stage"
solr_schema_template = rf"{solr_scheme_out_dir}\TEMPLATE_managed-schema.xml"
solr_schema_output = rf"{solr_scheme_out_dir}\managed-schema.xml"


def read_xml_with_comments(file_path):
    """Reads an XML file while preserving comments."""
    parser = etree.XMLParser(remove_blank_text=True, recover=True)
    tree = etree.parse(file_path, parser)
    root = tree.getroot()
    return tree, root

def add_or_update_field(root, field_name, field_type, indexed, stored, required, multi_valued, insert_after=None, insert_before=None):
    """Adds or updates a field element in the XML while preserving comments."""
    existing_field = root.find(f".//field[@name='{field_name}']")
    if existing_field is not None:
        # Update existing field
        existing_field.set("type", field_type)
        existing_field.set("indexed", indexed)
        existing_field.set("stored", stored)
        existing_field.set("required", required)
        existing_field.set("multiValued", multi_valued)
    else:
        # Add new field before the last closing tag
        new_field = etree.Element("field")
        new_field.set("name", field_name)
        new_field.set("type", field_type)
        new_field.set("indexed", indexed)
        new_field.set("stored", stored)
        new_field.set("required", required)
        new_field.set("multiValued", multi_valued)
        root.append(new_field)

        if insert_after:
            ref_field = root.find(f".//field[@name='{insert_after}']")
            if ref_field is not None and ref_field.getparent() is not None:
                ref_field.addnext(new_field)
                return

        if insert_before:
            ref_field = root.find(f".//field[@name='{insert_before}']")
            if ref_field is not None and ref_field.getparent() is not None:
                ref_field.addprevious(new_field)
                return

def remove_field(root, field_name):
    """Removes a field element from the XML while preserving comments."""
    for field in root.findall(".//field"):
        if field.get("name") == field_name:
            field.getparent().remove(field)

def save_xml(tree, output_file):
    """Saves the modified XML file while preserving comments."""
    tree.write(output_file, encoding="utf-8", xml_declaration=True, pretty_print=True)


def extract_table_definitions(sql_file):
    """Extracts table definitions from a .sql file."""
    with open(sql_file, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Regular expression to capture CREATE TABLE statements
    pattern = re.compile(r'create table.*?\(.*?\);', re.DOTALL | re.IGNORECASE)
    matches = pattern.findall(content)
    
    return matches

if __name__ == "__main__":
    table_def = extract_table_definitions(sql_table_input)

    tree, root = read_xml_with_comments(file_path=solr_schema_template)


    asdf = table_def[0].split("\n")
    reversed_list = list(reversed(asdf))

    # default field required
    add_or_update_field(root, field_name="solr_dt", field_type="pdate", indexed="true", stored="true", required="false", multi_valued="false", insert_after="_text_")

    for col in reversed_list:
        if "create table" not in col and ";" not in col:
            field_name = col.strip().split(" ")[0]
            deff = col.strip().split(" ")[1]

            if "not null" in col.lower():
                solr_required = "true"
            else:
                solr_required = "false"

            if deff.lower() == "bigint":
                solr_field_type = "pint"
            elif "varchar" in deff.lower() or "text" in deff.lower() or "citext" in deff.lower():
                solr_field_type = "string"
            elif "timestamp" in deff.lower():
                solr_field_type = "pdate"

            print(f"field_name: {field_name}, solr_field_type: {solr_field_type}, solr_required: {solr_required}")
            add_or_update_field(root, field_name=field_name, field_type=solr_field_type, indexed="true", stored="true", required=solr_required, multi_valued="false", insert_after="_text_")

    save_xml(tree, solr_schema_output)


