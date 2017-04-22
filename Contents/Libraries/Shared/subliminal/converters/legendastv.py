# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from babelfish import LanguageReverseConverter, language_converters

class LegendasTVConverter(LanguageReverseConverter):
    def __init__(self):
        self.name_converter = language_converters['name']
        self.from_legendastv = {'Portugu�s-BR': ('por', 'BR'),
                                'Portugu�s-PT': ('por',),
                                'Espanhol': ('spa',),
								'Ingl�s': ('eng',),
                                'Alem�o': ('deu',),
                                '�rabe': ('ara',),
                                'B�lgaro': ('bul',),
                                'Checo': ('ces',),
                                'Chin�s': ('zho',),
                                'Coreano': ('kor',),
                                'Dinamarqu�s': ('dan',),
                                'Franc�s': ('fra',),
                                'Italiano': ('ita',),
                                'Japon�s': ('jpn',),
                                'Noruegu�s': ('nor',),
                                'Polon�s': ('pol',),
                                'Sueco': ('swe',)}
        self.to_legendastv = {('por', 'BR'): 'Portugu�s-BR',
                              ('por',): 'Portugu�s-PT',
                              ('spa',): 'Espanhol',
                              ('eng',): 'Ingl�s',
							  ('deu',): 'Alem�o',
                              ('ara',): '�rabe',
                              ('bul',): 'B�lgaro',
                              ('ces',): 'Checo',
                              ('zho',): 'Chin�s',
                              ('kor',): 'Coreano',
                              ('dan',): 'Dinamarqu�s',
                              ('fra',): 'Franc�s',
                              ('ita',): 'Italiano',
                              ('jpn',): 'Japon�s',
                              ('nor',): 'Noruegu�s',
                              ('pol',): 'Polon�s',
                              ('swe',): 'Sueco'}
        self.codes = self.name_converter.codes | set(self.from_legendastv.keys())

    def convert(self, alpha3, country=None, script=None):
        if (alpha3, country, script) in self.to_legendastv:
            return self.to_legendastv[(alpha3, country, script)]
        if (alpha3, country) in self.to_legendastv:
            return self.to_legendastv[(alpha3, country)]
        if (alpha3,) in self.to_legendastv:
            return self.to_legendastv[(alpha3,)]

        return self.name_converter.convert(alpha3, country, script)

    def reverse(self, legendastv):
        if legendastv in self.from_legendastv:
            return self.from_legendastv[legendastv]

        return self.name_converter.reverse(legendastv)