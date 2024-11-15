import numpy as np
import trimesh
from stl import mesh

def load_3d_object(file_path):
    # Load the 3D object using trimesh
    model = trimesh.load(file_path)
    return model

def find_overhangs(mesh, overhang_angle=45):
    # Identify vertices and faces that are likely to need support
    # Convert angle to radians
    angle_threshold = np.radians(overhang_angle)
    
    # Calculate the normal of each face
    face_normals = mesh.face_normals
    z_axis = np.array([0, 0, 1])
    
    # Calculate the angle between face normals and the z-axis
    angles = np.arccos(np.clip(np.dot(face_normals, z_axis), -1.0, 1.0))
    
    # Find overhanging faces based on angle threshold
    overhang_faces = np.where(angles > angle_threshold)[0]
    return overhang_faces

def generate_supports(mesh, overhang_faces, max_supports=1000, batch_size=100):
    # Limit the number of overhang faces processed to max_supports
    limited_faces = overhang_faces[:max_supports] if len(overhang_faces) > max_supports else overhang_faces
    supports = []

    # Process supports in batches to avoid memory issues
    for i in range(0, len(limited_faces), batch_size):
        batch = []
        for face_index in limited_faces[i:i + batch_size]:
            face_center = mesh.triangles_center[face_index]
            support_height = face_center[2]  # From bottom to overhang point
            support_radius = 0.5  # Adjustable support radius

            # Create cylindrical support geometry
            cylinder = trimesh.creation.cylinder(radius=support_radius, height=support_height)
            cylinder.apply_translation([face_center[0], face_center[1], support_height / 2])

            batch.append(cylinder)
        
        # Concatenate the current batch and add to the supports list
        batch_mesh = trimesh.util.concatenate(batch)
        supports.append(batch_mesh)
    
    # Final concatenation of all batched supports
    all_supports = trimesh.util.concatenate(supports)
    return all_supports

def save_supports(support_mesh, output_file):
    # Save the support structures as an STL file
    support_mesh.export(output_file)

# Main function
def main(input_file, output_file):
    # Load the model
    model = load_3d_object(input_file)
    
    # Identify overhangs that need support
    overhang_faces = find_overhangs(model, overhang_angle=45)
    
    # Generate support structures for overhangs
    supports = generate_supports(model, overhang_faces, max_supports=1000, batch_size=100)
    
    # Save the generated supports to an STL file
    save_supports(supports, output_file)

# Example usage
input_file = "cone.obj"  # Path to your 3D model
output_file = "cone_support.obj"  # Path to save the support structures
main(input_file, output_file)
