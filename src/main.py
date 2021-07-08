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

def PoissonReconstrStrategy():
    # computing the mesh
    poisson_mesh = \
    o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd, depth=8, width=0, scale=1.1, linear_fit=False)[0]
    # cropping
    bbox = pcd.get_axis_aligned_bounding_box()
    p_mesh_crop = poisson_mesh.crop(bbox)

def ExpAndVisualize():
    # export
    o3d.io.write_triangle_mesh(output_path + "bpa_mesh.ply", dec_mesh)
    o3d.io.write_triangle_mesh(output_path + "p_mesh_c.ply", p_mesh_crop)

    # function creation
    def lod_mesh_export(mesh, lods, extension, path):
        mesh_lods = {}
        for i in lods:
            mesh_lod = mesh.simplify_quadric_decimation(i)
            o3d.io.write_triangle_mesh(path + "lod_" + str(i) + extension, mesh_lod)
            mesh_lods[i] = mesh_lod
        print("generation of " + str(i) + " LoD successful")
        return mesh_lods

    # execution of function
    my_lods = lod_mesh_export(bpa_mesh, [100000, 50000, 10000, 1000, 100], ".ply", output_path)
    # execution of function
    my_lods2 = lod_mesh_export(bpa_mesh, [8000, 800, 300], ".ply", output_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process a pointcloud file.')
    parser.add_argument("-i", "--input", dest="filename", required=True, type=validate_file, help="input file", metavar="FILE")
    args = parser.parse_args()
    input_path = args.filename
    output_path = "/data"
    dataname = "sample_w_normals.xyz"
    point_cloud = np.loadtxt(input_path + dataname, skiprows=1)

    # Format to open3d usable objects
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(point_cloud[:, :3])
    pcd.colors = o3d.utility.Vector3dVector(point_cloud[:, 3:6] / 255)
    pcd.normals = o3d.utility.Vector3dVector(point_cloud[:, 6:9])