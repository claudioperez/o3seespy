import eqsig
import numpy as np

import o3seespy as o3
from o3seespy import extensions


def get_inelastic_response(mass, k_spring, f_yield, motion, dt, xi=0.05, r_post=0.0):
    osi = o3.OpenSeesInstance(ndm=2, state=3)

    # Establish nodes
    bot_node = o3.node.Node(osi, 0, 0)
    top_node = o3.node.Node(osi, 0, 0)

    # Fix bottom node
    o3.Fix3DOF(osi, top_node, o3.cc.FREE, o3.cc.FIXED, o3.cc.FIXED)
    o3.Fix3DOF(osi, bot_node, o3.cc.FIXED, o3.cc.FIXED, o3.cc.FIXED)
    # Set out-of-plane DOFs to be slaved
    o3.EqualDOF(osi, top_node, bot_node, [o3.cc.Y, o3.cc.ROTZ])

    # nodal mass (weight / g):
    o3.Mass(osi, top_node, mass, 0., 0.)

    # Define material
    bilinear_mat = o3.uniaxial_material.Steel01(osi, fy=f_yield, e0=k_spring, b=r_post)

    # Assign zero length element, # Note: pass actual node and material objects into element
    o3.element.ZeroLength(osi, [bot_node, top_node], mats=[bilinear_mat], dirs=[o3.cc.DOF2D_X], r_flag=1)

    # Define the dynamic analysis
    values = list(-1 * motion)  # should be negative
    acc_series = o3.time_series.Path(osi, dt, values)
    o3.pattern.UniformExcitation(osi, o3.cc.X, accel_series=acc_series)

    # set damping based on first eigen mode
    angular_freq2 = o3.get_eigen(osi, solver='fullGenLapack', n=1)
    if hasattr(angular_freq2, '__len__'):
        angular_freq2 = angular_freq2[0]
    angular_freq = angular_freq2 ** 0.5
    beta_k = 2 * xi / angular_freq
    o3.rayleigh.Rayleigh(osi, alpha_m=0.0, beta_k=beta_k, beta_k_init=0.0, beta_k_comm=0.0)

    # Run the dynamic analysis

    o3.wipe_analysis(osi)
    newmark_gamma = 0.5
    newmark_beta = 0.25

    o3.algorithm.Newton(osi)
    o3.constraints.Transformation(osi)
    o3.algorithm.Newton(osi)
    o3.numberer.RCM(osi)
    o3.system.SparseGeneral(osi)
    o3.integrator.Newmark(osi, newmark_gamma, newmark_beta)
    o3.analysis.Transient(osi)

    o3.test_check.EnergyIncr(osi, tol=1.0e-10, max_iter=10)
    analysis_time = (len(values) - 1) * dt
    analysis_dt = 0.001
    outputs = {
        "time": [],
        "rel_disp": [],
        "rel_accel": [],
        "force": []
    }
    o3.record(osi)
    curr_time = o3.get_time(osi)
    while curr_time < analysis_time:
        outputs["time"].append(curr_time)
        outputs["rel_disp"].append(o3.get_node_disp(osi, top_node, o3.cc.X))
        outputs["rel_accel"].append(o3.get_node_accel(osi, top_node, o3.cc.X))
        o3.gen_reactions(osi)
        outputs["force"].append(-o3.get_node_reaction(osi, bot_node, o3.cc.X))  # Negative since diff node
        o3.analyze(osi, 1, analysis_dt)
        curr_time = o3.get_time(osi)
    o3.wipe(osi)
    o3.extensions.to_cpy_file(osi)
    return outputs


def test_can_compress_py_file():

    mass = 1.0
    f_yield = 1.5  # Reduce this to make it nonlinear
    r_post = 0.0
    rec = 0.3 * np.sin(np.linspace(0, 2, 10))

    k_spring = 4 * np.pi ** 2
    outputs = get_inelastic_response(mass, k_spring, f_yield, rec, dt=0.01, xi=0.05, r_post=r_post)


def test_get_fn_name_and_args():
    line = 'node(0.0, 1.0)'
    fn1, args = o3.extensions._get_fn_name_and_args(line)
    assert fn1 == 'node'
    assert args[0] == '0.0'
    assert args[1] == '1.0'



if __name__ == '__main__':
    # test_get_fn_name_and_args()
    test_can_compress_py_file()
    # import re
    # s = "node(0.0, 1.0, a, 'ret')"
    # print(re.search(r'\((.*?)\)', s).group(1))
