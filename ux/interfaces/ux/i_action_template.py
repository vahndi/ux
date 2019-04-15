class IActionTemplate(object):

    @property
    def action_type(self):
        raise NotImplementedError

    @property
    def source_id(self):
        raise NotImplementedError

    @property
    def target_id(self):
        raise NotImplementedError

