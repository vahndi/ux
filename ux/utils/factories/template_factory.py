from pandas import DataFrame, notnull


def add_meta(template: dict, key: str, value: str):

    if 'meta' not in template.keys():
        template['meta'] = {}
    template['meta'][key] = value
    return template


def generate_generic_template(specifics: dict, placeholders: dict, meta: dict = None):
    """
    Generate an example template from a dictionary of keys and values.

    :param specifics: Keys and values specific to this template.
    :param placeholders: Keys and values for all templates.
    :param meta: Additional values for meta, other than those already in `specifics`.
    :rtype: dict
    """
    template = placeholders.copy()
    for key, value in specifics.items():
        if notnull(value):
            if key in ('source', 'destination'):
                template[key] = value
            elif key == 'meta':
                if 'meta' not in template.keys():
                    template['meta'] = {}
                for line in value.split('\n'):
                    template['meta'][line.split(':')[0]] = line.split(':')[1]
                if meta is not None:
                    for k_meta, v_meta in meta.items():
                        template['meta'][k_meta] = v_meta
    return template


def generate_checkbox_check_template(specifics: dict, placeholders: dict,
                                     **kwargs):
    """
    Generate a template for the check event of a checkbox.

    :rtype: dict
    """
    template = generate_generic_template(
        specifics=specifics, placeholders=placeholders,
        meta={'value': '{{checkbox-value}}'}
    )
    template['action-type'] = 'check'
    return template


def generate_checkbox_uncheck_template(specifics: dict, placeholders: dict,
                                       **kwargs):
    """
    Generate a template for the uncheck event of a checkbox.

    :rtype: dict
    """
    template = generate_generic_template(
        specifics=specifics, placeholders=placeholders,
        meta={'value': '{{checkbox-value}}'}
    )
    template['action-type'] = 'uncheck'
    return template


def generate_dropdown_select_template(specifics: dict, placeholders: dict,
                                      **kwargs):
    """
    Generate a template for the select event of a dropdown.

    :rtype: dict
    """
    template = generate_generic_template(
        specifics=specifics, placeholders=placeholders,
        meta={'selected-item': '{{selected-item}}'}
    )
    template['action-type'] = 'select'
    return template


def generate_link_click_template(specifics: dict, placeholders: dict,
                                 **kwargs):
    """
    Generate a template for the click event of a link.

    :rtype: dict
    """
    template = generate_generic_template(
        specifics=specifics, placeholders=placeholders
    )
    template['action-type'] = 'click'
    return template


def generate_nav_button_click_template(specifics: dict, placeholders: dict,
                                       **kwargs):
    """
    Generate a template for the click event of a navigation button.

    :rtype: dict
    """
    template = generate_generic_template(
        specifics=specifics, placeholders=placeholders
    )
    template['action-type'] = 'click'
    return template


def generate_page_load_template(specifics: dict, placeholders: dict,
                                **kwargs):
    """
    Generate a template for the page load event of a page.

    :rtype: dict
    """
    template = generate_generic_template(
        specifics=specifics, placeholders=placeholders
    )
    template['action-type'] = 'load'
    return template


def generate_radio_buttons_check_template(specifics: dict, placeholders: dict,
                                          **kwargs):
    """
    Generate a template for the check event of a radio button.

    :rtype: dict
    """
    template = generate_generic_template(
        specifics=specifics, placeholders=placeholders
    )
    template['action-type'] = 'check'
    return template


def generate_submit_button_submit_template(specifics: dict, placeholders: dict,
                                           data: DataFrame, element_attrs: dict,
                                           **kwargs):
    """
    Generate a template for the submit event of a submit button.

    :rtype: dict
    """
    template = generate_generic_template(
        specifics=specifics, placeholders=placeholders
    )
    button_name = template['source']
    parent_name = '.'.join(button_name.split('.')[: -1])
    siblings = data.loc[
        (data['source'].str.startswith(parent_name)) &
        (data['source'].str.len() > len(parent_name)) &
        (data['source'] != button_name)
    ]
    for _, sibling in siblings.iterrows():
        element_path = sibling['source']
        element_name = element_path.split('.')[-1]
        element_type = sibling['ui-element']
        if element_type in element_attrs.keys():
            add_meta(template, element_name, '{{%s.%s}}' % (
                element_name,
                element_attrs[element_type]
            ))
    template['action-type'] = 'submit'
    return template


def generate_textbox_keystroke_template(specifics: dict, placeholders: dict,
                                        **kwargs):
    """
    Generate a template for the keystroke event of a textbox.

    :rtype: dict
    """
    template = generate_generic_template(
        specifics=specifics, placeholders=placeholders,
        meta={'key-id': '{{key-id}}'}
    )
    template['action-type'] = 'keystroke'
    return template
