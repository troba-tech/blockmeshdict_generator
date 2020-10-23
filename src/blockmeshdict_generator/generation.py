import numpy as np


from .classes.block import Block
from .classes.mesh import Mesh


def generate_block(origin, size, n_cells):

    origin_x = origin[0]
    origin_y = origin[1]
    origin_z = origin[2]

    size_x = size[0]
    size_y = size[1]
    size_z = size[2]

    block_points = [
        [origin_x, origin_y, origin_z],
        [origin_x + size_x, origin_y, origin_z],
        [origin_x + size_x, origin_y + size_y, origin_z],
        [origin_x, origin_y + size_y, origin_z],

        [origin_x, origin_y, origin_z + size_z],
        [origin_x + size_x, origin_y, origin_z + size_z],
        [origin_x + size_x, origin_y + size_y, origin_z + size_z],
        [origin_x, origin_y + size_y, origin_z + size_z],
    ]

    block = Block.create_from_points(block_points)

    block.n_cells = n_cells

    return block

def generate_mesh(
    size_blocks,
    n_cells,
    bottom_boundaries,
    top_boundaries,
    left_boundaries,
    right_boundaries,
    mode_2D=True,
    mode_2_z_size=0.1,
    front_boundaries=None,
    back_boundaries=None,
    boundaries_type = {},
    removed_blocks=[]
):

    size_blocks_x = size_blocks[0]
    size_blocks_y = size_blocks[1]

    if not mode_2D:
        size_blocks_z = size_blocks[2]

    n_cells_x = n_cells[0]
    n_cells_y = n_cells[1]
    if not mode_2D:
        n_cells_z = n_cells[2]


    mesh = Mesh()

    # Create all blocks
    
    for k in range(1 if mode_2D else len(size_blocks_z)):
        for j in range(len(size_blocks_y)):
            for i in range(len(size_blocks_x)):

                # Do not include removed wall
                if (i,j,k) in [block['coord'] for block in removed_blocks]:    
                    continue

                

                block = generate_block(
                    origin=[
                        np.sum(size_blocks_x[0:i]),
                        np.sum(size_blocks_y[0:j]),
                        0 if mode_2D else np.sum(size_blocks_z[0:k]),
                    ],
                    size=[
                        size_blocks_x[i],
                        size_blocks_y[j],
                        mode_2_z_size if mode_2D else size_blocks_z[k],
                    ],
                    n_cells=[
                        int(np.ceil(n_cells_x*size_blocks_x[i]/np.sum(size_blocks_x))),
                        int(np.ceil(n_cells_y*size_blocks_y[j]/np.sum(size_blocks_y))),
                        1 if mode_2D else int(np.ceil(n_cells_z*size_blocks_z[k]/np.sum(size_blocks_z))),
                    ]
                )

                #Take into account internal boundaries due to removed blocks

                if i < len(size_blocks_x)-1 and (i+1,j,k) in [block['coord'] for block in removed_blocks]:  
                    boundary_name = [ block for block in removed_blocks if block["coord"] == (i+1,j,k) ][0]["boundaries"]["left"]
                    block.set_boundary('right', boundary_name)

                if i > 0 and (i-1,j,k) in [block['coord'] for block in removed_blocks]:    
                    boundary_name = [ block for block in removed_blocks if block["coord"] == (i-1,j,k) ][0]["boundaries"]["right"]
                    block.set_boundary('left', boundary_name)

                if j < len(size_blocks_y)-1 and (i,j+1,k) in [block['coord'] for block in removed_blocks]:
                    boundary_name = [ block for block in removed_blocks if block["coord"] == (i,j+1,k) ][0]["boundaries"]["bottom"]    
                    block.set_boundary('back', boundary_name)

                if j > 0 and (i,j-1,k) in [block['coord'] for block in removed_blocks]:  
                    boundary_name = [ block for block in removed_blocks if block["coord"] == (i,j-1,k) ][0]["boundaries"]["top"]  
                    block.set_boundary('front', boundary_name)

                if not mode_2D:
                    if k < len(size_blocks_z)-1 and (i,j,k+1) in [block['coord'] for block in removed_blocks]:
                        boundary_name = [ block for block in removed_blocks if block["coord"] == (i,j,k+1) ][0]["boundaries"]["back"]    
                        block.set_boundary('bottom', boundary_name)

                    if k > 0 and (i,j,k-1) in [block['coord'] for block in removed_blocks]:  
                        boundary_name = [ block for block in removed_blocks if block["coord"] == (i,j,k-1) ][0]["boundaries"]["front"]  
                        block.set_boundary('top', boundary_name)


                # Add external boundaries

                if j == 0:
                    block.set_boundary('front', bottom_boundaries[i][k])
                if j == len(size_blocks_y)-1:
                    block.set_boundary('back', top_boundaries[i][k])

                if i == 0:
                    block.set_boundary('left', left_boundaries[j][k])
                if i == len(size_blocks_x)-1:
                    block.set_boundary('right', right_boundaries[j][k])

                
                if k == 0:
                    if mode_2D:
                        block.set_boundary('top', "FrontAndBack")
                    else: 
                        block.set_boundary('top', front_boundaries[i][j])
                if k == 1 if mode_2D else len(size_blocks_z)-1:
                    if mode_2D:
                        block.set_boundary('bottom', "FrontAndBack")
                    else:
                        block.set_boundary('bottom', back_boundaries[i][j])
                
                mesh.add_block(block)


    # Set boundary types
    for boundaries_name, boundary_type in boundaries_type.items():
        mesh.set_boundary_type(boundaries_name, boundary_type)

        if mode_2D:
            mesh.set_boundary_type("FrontAndBack", "empty")

    return mesh


