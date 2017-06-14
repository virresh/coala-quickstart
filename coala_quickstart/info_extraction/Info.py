class Info:
    description = 'Some information'

    # tuple of allowed types for the information value.
    value_type = (object,)

    def __init__(self,
                 source,
                 value,
                 extractor=None,
                 **kwargs):
        """
        :param source:    Source from where the information is discovered.
        :param value:     Value of the infomation to be represented.
        :param extractor: ``InfoExtractor`` instance used to extract the
                          information.
        """
        if not self.value_type:
            self.value_type = (object,)

        if not isinstance(value, self.value_type):
            raise TypeError("The value {} does not match the allowed "
                            "value types {}".format(value, self.value_type))
        self.source = source
        self._value = value
        self.extractor = extractor
        for key, val in kwargs.items():
            setattr(self, key, val)

    @property
    def value(self):
        return self._value

    @property
    def name(self):
        return self.__class__.__name__
