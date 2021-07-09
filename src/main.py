import numpy as np
import open3d as o3d
import argparse



def validate_file(f):
    if not os.path.exists(f):
        # Argparse uses the ArgumentTypeError to give a rejection message like:
        # error: argument input: x does not exist
        raise argparse.ArgumentTypeError("{0} does not exist".format(f))
    return f

def BPAstrategy():
    # radius determination
    distances = pcd.compute_nearest_neighbor_distance()
    avg_dist = np.mean(distances)
    radius = 3 * avg_dist
    # computing the mehs
    bpa_mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(pcd, o3d.utility.DoubleVector(
        [radius, radius * 2]))
    # decimating the mesh
    dec_mesh = mesh.simplify_quadric_decimation(100000)
    # optional below:
    dec_mesh.remove_degenerate_triangles()
    dec_mesh.remove_duplicated_triangles()
    dec_mesh.remove_duplicated_vertices()
    dec_mesh.remove_non_manifold_edges()
    return dec_mesh

def PoissonReconstrStrategy():
    # computing the mesh
    poisson_mesh = \
    o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd, depth=8, width=0, scale=1.1, linear_fit=False)[0]
    # cropping
    bbox = pcd.get_axis_aligned_bounding_box()
    p_mesh_crop = poisson_mesh.crop(bbox)
    return p_mesh_crop

def ExpAndVisualize(mesh):
    # export
    o3d.io.write_triangle_mesh(output_path + "mesh.ply", mesh)

    # function creation
    def lod_mesh_export(lmesh, lods, extension, path):
        mesh_lods = {}
        for i in lods:
            mesh_lod = lmesh.simplify_quadric_decimation(i)
            o3d.io.write_triangle_mesh(path + "lod_" + str(i) + extension, mesh_lod)
            mesh_lods[i] = mesh_lod
        print("generation of " + str(i) + " LoD successful")
        return mesh_lods

    # execution of function
    my_lods = lod_mesh_export(mesh, [100000, 50000, 10000, 1000, 100], ".ply", output_path)
    # execution of function
    my_lods2 = lod_mesh_export(mesh, [8000, 800, 300], ".ply", output_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process a pointcloud file.')
    parser.add_argument("-i", "--input", dest="filename", required=True, type=validate_file, help="input file", metavar="FILE")
    args = parser.parse_args()
    input_path = args.filename
    output_path = "/data"
    dataname = "sample_w_normals.xyz"
    #point_cloud = np.loadtxt(input_path + dataname, skiprows=1)

    # Format to open3d usable objects
    #pcd = o3d.geometry.PointCloud()
    # new
    pcd = o3d.io.read_point_cloud(input_path)

    msh1 = ExpAndVisualize(BPAstrategy(pcd))
    msh2 = ExpAndVisualize(PoissonReconstrStrategy(pcd))
    #pcd.points = o3d.utility.Vector3dVector(point_cloud[:, :3])
    #pcd.colors = o3d.utility.Vector3dVector(point_cloud[:, 3:6] / 255)
    #pcd.normals = o3d.utility.Vector3dVector(point_cloud[:, 6:9])