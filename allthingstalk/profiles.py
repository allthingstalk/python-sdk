class Profile(dict):
    _type = None
    extras = []

    def __init__(self, **kwargs):
        self.type = self.__class__._type
        profile = {'type': self.type}
        for key, val in kwargs.items():
            if key in self.__class__.extras:
                profile[key] = val
        dict.__init__(self, **profile)


class NumberProfile(Profile):
    _type = 'number'
    extras = ['minimum', 'maximum', 'unit']


class IntegerProfile(Profile):
    _type = 'integer'
    extras = ['minimum', 'maximum', 'unit']


class BooleanProfile(Profile):
    _type = 'boolean'
    extras = []


class StringProfile(Profile):
    _type = 'string'
    extras = ['enum']


class ObjectProfile(Profile):
    _type = 'object'
    extras = ['properties']


class GeoProfile(ObjectProfile):

    def __init__(self, **kwargs):
        super().__init__(properties={
            'latitude': NumberProfile(),
            'longitude': NumberProfile()
        })
