# -*- coding: utf-8 -*-
# Copyright 2017-2020 The diffsims developers
#
# This file is part of diffsims.
#
# diffsims is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# diffsims is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with diffsims.  If not, see <http://www.gnu.org/licenses/>.

import diffsims as ds
from diffsims.generators.rotation_list_generators import get_grid_streographic


class StructureLibrary():
    """
    A dictionary containing all the structures and their associated rotations
    in the .struct_lib attribute.

    Attributes
    ----------
    identifiers : list of strings/ints
        A list of phase identifiers referring to different atomic structures.
    structures : list of diffpy.structure.Structure objects.
        A list of diffpy.structure.Structure objects describing the atomic
        structure associated with each phase in the library.
    orientations : list
        A list over identifiers of lists of euler angles (as tuples) in the rzxz
        convention and in degrees.
    """

    def __init__(self,
                 identifiers,
                 structures,
                 orientations):
        if len(identifiers) != len(structures):
            raise ValueError('Number of identifiers ({}) and structures ({}) must be the same.'.format(
                len(identifiers), len(structures)))
        if len(identifiers) != len(orientations):
            raise ValueError('Number of identifiers ({}) and orientations ({}) must be the same.'.format(
                len(identifiers), len(orientations)))

        self.identifiers = identifiers
        self.structures = structures
        self.orientations = orientations
        # Create the actual dictionary
        self.struct_lib = dict()
        for ident, struct, ori in zip(identifiers, structures, orientations):
            self.struct_lib[ident] = (struct, ori)

    def get_library_size(self, to_print = False):
        """
        Returns the the total number of orientations in the
        current StructureLibrary object. Will also print the number of orientations
        for each identifier in the library if the parameter to_print is set to
        True. Works with both self.orientations on the form [1,2]
        and [[1,2], [2,3]](rotation lists).

        Parameters
        ----------
        to_print : bool
            Default is 'False'
            Returns
            -------
        size_library : int
            Total number of entries in the current StructureLibrary object.
        """
        size_library = 0
        for i in range (len(self.orientations)):
            if len(self.orientations[i]) == 1:
                size_library += 1
            else:
                size_library += len(self.orientations[i])
            if to_print == True:
                print(self.identifiers[i], "has", \
                len(self.orientations[i]), "number of entries.")
        if to_print == True:
            print("\nIn total:", size_library, "number of entries")
        return size_library

    @classmethod
    def from_orientation_lists(cls, identifiers, structures, orientations):
        """
        Creates a structure library from "manual" orientation lists

        Parameters
        ----------
        identifiers : list of strings/ints
            A list of phase identifiers referring to different atomic structures.
        structures : list of diffpy.structure.Structure objects.
            A list of diffpy.structure.Structure objects describing the atomic
            structure associated with each phase in the library.
        orientations : list of lists of tuples
            A list over identifiers of lists of euler angles (as tuples) in the rzxz
            convention and in degrees.
        Returns
        -------
        StructureLibrary
        """
        return cls(identifiers, structures, orientations)

    @classmethod
    def from_crystal_systems(cls, identifiers, structures, systems, resolution, equal='angle'):
        """
        Creates a structure library from crystal system derived orientation lists

        Parameters
        ----------
        identifiers : list of strings/ints
            A list of phase identifiers referring to different atomic structures.
        structures : list of diffpy.structure.Structure objects.
            A list of diffpy.structure.Structure objects describing the atomic
            structure associated with each phase in the library.
        systems : list
            A list over indentifiers of crystal systems
        resolution : float
            resolution in degrees
        equal : str
            Default is 'angle'
        Returns
        -------
        StructureLibrary
        """
        orientations = []
        for system in systems:
            orientations.append(get_grid_streographic(system, resolution, equal))
        return cls(identifiers, structures, orientations)
