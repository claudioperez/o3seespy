import o3seespy as o3  # for testing only


def test_elastic_beam_column2d():
    osi = o3.OpenseesInstance(dimensions=2)
    transf = o3.transformation.Linear(osi, [])
    o3.element.ElasticBeamColumn2D(osi, ele_nodes=1, big_a=1.0, big_e=1.0, iz=1.0, transf=transf, mass=1.0, c_mass=1)

def test_elastic_beam_column3d():
    osi = o3.OpenseesInstance(dimensions=2)
    transf = o3.transformation.Linear(osi, [])
    o3.element.ElasticBeamColumn3D(osi, ele_nodes=1, big_a=1.0, big_e=1.0, big_g=1.0, big_j=1.0, iy=1.0, iz=1.0, transf=transf, mass=1.0, c_mass=1)


def test_mod_elastic_beam2dmass():
    osi = o3.OpenseesInstance(dimensions=2)
    transf = o3.transformation.Linear(osi, [])
    o3.element.ModElasticBeam2Dmass(osi, ele_nodes=1, big_a=1.0, big_e=1.0, iz=1.0, k11=1.0, k33=1.0, k44=1.0, transf=transf, mass_dens=1.0, c_mass=1)


def test_elastic_timoshenko_beam2d():
    osi = o3.OpenseesInstance(dimensions=2)
    transf = o3.transformation.Linear(osi, [])
    o3.element.ElasticTimoshenkoBeam2D(osi, ele_nodes=1, big_e=1.0, big_g=1.0, big_a=1.0, iz=1.0, avy=1.0, transf=transf, mass=1.0, c_mass=1)

def test_elastic_timoshenko_beam3d():
    osi = o3.OpenseesInstance(dimensions=2)
    transf = o3.transformation.Linear(osi, [])
    o3.element.ElasticTimoshenkoBeam3D(osi, ele_nodes=1, big_e=1.0, big_g=1.0, big_a=1.0, iz=1.0, jx=1.0, iy=1.0, iz_2=1, avy=1.0, avz=1.0, transf=transf, mass=1.0, c_mass=1)



def test_disp_beam_column():
    osi = o3.OpenseesInstance(dimensions=2)
    i_node = o3.node.Node(osi, 0.0, 0.0)
    j_node = o3.node.Node(osi, 0.0, 1.0)
    transf = o3.transformation.Linear(osi, [])
    sec = o3.section.Elastic(osi, 10.0, 1.0, 1.0)
    integration = o3.beam_integration.Lobatto(osi, sec, 5)
    o3.element.DispBeamColumn(osi, i_node=i_node, j_node=j_node, transf=transf, integration=integration, c_mass=1, mass=0.0)


def test_force_beam_column():
    osi = o3.OpenseesInstance(dimensions=2)
    i_node = o3.node.Node(osi, 0.0, 0.0)
    j_node = o3.node.Node(osi, 0.0, 1.0)
    transf = o3.transformation.Linear(osi, [])
    sec = o3.section.Elastic(osi, 10.0, 1.0, 1.0)
    integration = o3.beam_integration.Lobatto(osi, sec, 5)
    o3.element.ForceBeamColumn(osi, i_node=i_node, j_node=j_node, transf=transf, integration=integration, max_iter=10, tol=1e-12, mass=0.0)


def test_nonlinear_beam_column():
    osi = o3.OpenseesInstance(dimensions=2)
    i_node = o3.node.Node(osi, 0.0, 0.0)
    j_node = o3.node.Node(osi, 0.0, 1.0)
    sec = o3.section.Elastic(osi, 10.0, 1.0, 1.0)
    transf = o3.transformation.Linear(osi, [])
    o3.element.NonlinearBeamColumn(osi, i_node=i_node, j_node=j_node, num_intgr_pts=1, sec=sec, transf=transf, max_iter=10, tol=1e-12, mass=0.0, int_type=1)


def test_disp_beam_column_int():
    osi = o3.OpenseesInstance(dimensions=2)
    sec = o3.section.Elastic(osi, 10.0, 1.0, 1.0)
    transf = o3.transformation.Linear(osi, [])
    o3.element.DispBeamColumnInt(osi, ele_nodes=1, num_intgr_pts=1, sec=sec, transf=transf, c_rot=1.0, mass_dens=1.0)


def test_mvlem():
    osi = o3.OpenseesInstance(dimensions=2)
    o3.element.MVLEM(osi, dens=1.0, ele_nodes=1, m=1, c=1.0, thick=1, widths=1, rho=1, mat_concrete_tags=1, mat_steel_tags=1, mat_shear=mat_shear)


def test_sfimvlem():
    osi = o3.OpenseesInstance(dimensions=2)
    o3.element.SFIMVLEM(osi, ele_nodes=1, m=1, c=1.0, thick=1, widths=1, mat_tags=1)
