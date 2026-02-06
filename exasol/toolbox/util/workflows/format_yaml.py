from ruamel.yaml import YAML


def get_standard_yaml() -> YAML:
    yaml = YAML()
    yaml.width = 200
    yaml.preserve_quotes = True
    yaml.sort_base_mapping_type_on_output = False  # type: ignore
    yaml.indent(mapping=2, sequence=4, offset=2)
    return yaml
