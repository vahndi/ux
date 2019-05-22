import json
from os.path import isdir, join
from typing import Union

from pandas import DataFrame, Series, notnull


def generate_template(specifics: Union[Series, dict], placeholders: dict):
    """
    Generate an example template from a dictionary of keys and values.

    :param specifics: Keys and values specific to this template.
    :param placeholders: Keys and values for all templates.
    :rtype: dict
    """
    template = None
    for action_type in specifics['action-types'].split('|'):
        template = placeholders.copy()
        template['action-type'] = action_type
        for key, value in specifics.items():
            if notnull(value):
                if key in ('source', 'destination'):
                    template[key] = value
                elif key == 'meta':
                    template['meta'] = {
                        line.split(':')[0]: line.split(':')[1]
                        for line in value.split('\n')
                    }
    return template


def generate_templates(data: DataFrame, placeholders: dict, out_dir: str = ''):
    """
    Generate a list of example templates from a DataFrame and save to individual `.json` files.

    :param data: DataFrame with columns of specific values for each template.
    :param placeholders: dict with values for every template, to be edited by the user later.
    :param out_dir: Optional directory to save templates to.
    :rtype: List[dict]
    """
    save_files = isdir(out_dir)
    templates = []
    for _, row in data.iterrows():
        template = generate_template(
            specifics=row, placeholders=placeholders
        )
        if template is None:
            print('\nError generating template for {}'.format(template))
        else:
            output = json.dumps(template, indent=4)
            print(output)
            if save_files:
                with open(join(
                        out_dir,
                        template['source'] + '|' + template['action-type'] + '.json'
                ), 'w') as f:
                    f.write(output)
            templates.append(template)
    return templates
