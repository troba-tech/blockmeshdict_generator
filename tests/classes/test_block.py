import unittest

import numpy as np
from blockmeshdict_generator.classes.primitives import Vertex, Edge
from blockmeshdict_generator.classes.mesh import Mesh

from blockmeshdict_generator.util import constants

from .fixtures import FixturedTestCase

class TestBlock(FixturedTestCase):
    ###
    ### Block tests
    ###
    def test_block_definition(self):
        """ the correct output for blockMeshDict """
        self.mesh.prepare_data()

        self.assertEqual(
            str(self.block_1),
            "hex  ( 0 1 2 3 4 5 6 7 )  (5 10 15)  simpleGrading (1 1 1) // 0 Test"
        )
    
    def test_face_format(self):
        """ the correct face format for blockMeshDict """
        self.mesh.prepare_data()

        self.assertEqual(
            self.block_1.format_face('bottom'),
            "(0 1 2 3)"
        )
    
    def test_boundaries(self):
        """ boundary naming/positions """
        self.mesh.prepare_data()

        self.assertListEqual(self.block_1.boundaries['inlet'], ['bottom'])
        self.assertListEqual(self.block_1.boundaries['outlet'], ['top'])
        self.assertListEqual(self.block_1.boundaries['walls'], ['left', 'right', 'front', 'back'])

    def test_faces(self):
        """ definitions of faces around the block """
        self.mesh.prepare_data()

        self.assertListEqual(
            self.block_1.get_faces('walls'),
            ['(4 0 3 7)', '(5 1 2 6)', '(4 5 1 0)', '(7 6 2 3)']
        )

    def test_straight_block_size(self):
        """ length of a straight block edge """
        self.mesh.prepare_data()

        self.assertEqual(self.block_1.get_size(2), 1)
    
    def test_arc_block_size(self):
        """ length of a curved block edge (two segments) """
        self.mesh.prepare_data()

        self.assertAlmostEqual(
            self.block_1.get_size(0), 1.118033988749895
        )

    def test_spline_block_size(self):
        """ length of a spline block edge (three or more segments) """
        self.mesh.prepare_data()

        self.assertAlmostEqual(self.block_1.get_size(1), 1.2299269360237004)

    def test_cell_size(self):
        """ grade_to_size must calculate the correct grading to match given cell size """
        axis = 2
        test_cell_size = 0.005
        n = self.block_1.n_cells[axis]

        # set the desired cell size
        self.block_1.grade_to_size(axis, test_cell_size)
        self.mesh.prepare_data() # runs all deferred functions

        # get block grading
        g = self.block_1.grading[axis]

        # check that the sum of all elements, graded, is block size
        cell_sizes = [test_cell_size]
        block_size = 0

        for _ in range(n):
            s = cell_sizes[-1]*(g**(1/n))
            cell_sizes.append(s)
            block_size += s

        self.assertAlmostEqual(block_size, self.block_1.get_size(axis))

        # also check that ratio of first to last cell size is what's calculated
        self.assertAlmostEqual(cell_sizes[-1]/cell_sizes[0], g, delta=constants.tol)

    def test_axis_from_pair(self):
        """ return the correct pairs of points along each axis """
        self.mesh.prepare_data()

        # this only works for the first block, where
        # index in block.vertices[] and vertex.mesh_index coincide;
        # later these numbers differ
        pairs = [
            [[0, 1], [3, 2], [4, 5], [7, 6]],
            [[0, 3], [1, 2], [5, 6], [4, 7]],
            [[0, 4], [1, 5], [2, 6], [3, 7]],
        ]

        for i, pair in enumerate(pairs):
            for j in range(4):
                v1 = self.block_1.vertices[pair[j][0]].mesh_index
                v2 = self.block_1.vertices[pair[j][1]].mesh_index

                self.assertEqual(
                    self.block_1.get_axis_from_pair((v1, v2)), i)

if __name__ == '__main__':
    unittest.main()