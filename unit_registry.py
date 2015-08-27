"""
A registry for units that can be added to and modified.


"""

#-----------------------------------------------------------------------------
# Copyright (c) 2013, yt Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

from yt.units.unit_lookup_table import \
    default_unit_symbol_lut

class SymbolNotFoundError(Exception):
    pass

class UnitParseError(Exception):
    pass

class UnitRegistry:
    """A registry for unit symbols"""
    def __init__(self, add_default_symbols=True, lut=None):
        if lut:
            self.lut = lut
        else:
            self.lut = {}
        self.unit_objs = {}

        if add_default_symbols:
            self.lut.update(default_unit_symbol_lut)

    def __getitem__(self, key):
        return self.lut[key]

    def __contains__(self, item):
        return item in self.lut

    def add(self, symbol, base_value, dimensions, tex_repr=None, offset=None):
        """
        Add a symbol to this registry.

        """
        from yt.units.unit_object import validate_dimensions

        # Validate
        if not isinstance(base_value, float):
            raise UnitParseError("base_value (%s) must be a float, got a %s."
                                 % (base_value, type(base_value)))

        if offset is not None:
            if not isinstance(offset, float):
                raise UnitParseError(
                    "offset value (%s) must be a float, got a %s."
                    % (offset, type(offset)))
        else:
            offset = 0.0

        validate_dimensions(dimensions)

        if tex_repr is None:
            # make educated guess that will look nice in most cases
            tex_repr = r"\rm{" + symbol + "}"

        # Add to lut
        self.lut.update({symbol: (base_value, dimensions, offset, tex_repr)})

    def remove(self, symbol):
        """
        Remove the entry for the unit matching `symbol`.

        """
        if symbol not in self.lut:
            raise SymbolNotFoundError(
                "Tried to remove the symbol '%s', but it does not exist" \
                "in this registry." % symbol)

        del self.lut[symbol]

    def modify(self, symbol, base_value):
        """
        Change the base value of a dimension.  Useful for adjusting code units
        after parsing parameters."

        """
        if symbol not in self.lut:
            raise SymbolNotFoundError(
                "Tried to modify the symbol '%s', but it does not exist" \
                "in this registry." % symbol)

        if hasattr(base_value, "in_base"):
            base_value = float(base_value.in_base().value)

        self.lut[symbol] = (base_value, ) + self.lut[symbol][1:]

    def keys(self):
        """
        Print out the units contained in the lookup table.

        """
        return self.lut.keys()
