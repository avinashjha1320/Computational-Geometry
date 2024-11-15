import numpy as np
import trimesh

def load_model(filepath):
    """
    Load the 3D model from an OBJ or STL file.
    """
    model = trimesh.load(filepath)
    print(f"Model loaded: {filepath}")
    print(f"Vertices: {len(model.vertices)}, Faces: {len(model.faces)}")
    return model

def calculate_escape_paths(model):
    """
    Placeholder for calculating escape paths within the model volume.
    These paths guide the placement of parting surfaces and membranes.
    """
    print("Calculating escape paths (placeholder)...")
    escape_paths = None  # This should be replaced with real escape path calculations.
    return escape_paths

def create_parting_surface(model, escape_paths):
    """
    Generates parting surfaces based on escape paths.
    These surfaces allow the mold to split for easy object removal.
    """
    print("Creating parting surfaces (placeholder)...")
    
    # Instead of using `model.section`, generate a proper plane or mesh for parting surface
    # We can create a simple plane at the centroid, oriented along the Z-axis.
    centroid = model.centroid
    parting_surface = trimesh.creation.box(extents=[model.extents[0], model.extents[1], 0.1])  # Thin box as placeholder
    
    # Position the parting surface near the model centroid
    parting_surface.apply_translation([centroid[0], centroid[1], centroid[2] - 0.05])
    
    return parting_surface

def create_hard_shell(model, parting_surface):
    """
    Create a hard shell mold based on the parting surface.
    """
    print("Creating hard shell...")
    
    # Ensure the parting surface is a proper mesh before performing difference operation
    if isinstance(parting_surface, trimesh.Trimesh):  # Check if parting surface is a mesh
        if not parting_surface.is_volume:
            print("Error: parting surface is not a valid volume!")
            return None
    else:
        print("Error: parting surface is not a valid trimesh object!")
        return None
    
    # Perform the difference operation between the model and parting surface
    hard_shell = model.copy()
    if hard_shell.is_volume and parting_surface.is_volume:
        hard_shell = hard_shell.difference(parting_surface)
    else:
        print("Error: Both objects must be volumes for the difference operation.")
    
    print("Hard shell mold created.")
    return hard_shell

def create_flexible_mold(model, parting_surface):
    """
    Create a flexible silicone mold that will fit within the hard shell.
    """
    print("Creating flexible silicone mold...")
    
    # Ensure the parting surface is a proper mesh
    if isinstance(parting_surface, trimesh.Trimesh):  # Check if parting surface is a mesh
        if not parting_surface.is_volume:
            print("Error: parting surface is not a valid volume!")
            return None
    else:
        print("Error: parting surface is not a valid trimesh object!")
        return None
    
    # Create the flexible mold by slightly expanding the original model
    silicone_mold = model.copy()
    silicone_mold = silicone_mold.difference(parting_surface)
    silicone_mold.apply_scale(1.02)  # Offset slightly for fit
    print("Flexible silicone mold created.")
    return silicone_mold

def export_mold_parts(hard_shell, silicone_mold):
    """
    Exports the hard shell and silicone mold parts as separate STL files.
    """
    hard_shell_filename = "hard_shell_mold.stl"
    silicone_mold_filename = "silicone_mold.stl"
    
    hard_shell.export(hard_shell_filename)
    silicone_mold.export(silicone_mold_filename)
    
    print(f"Hard shell saved as {hard_shell_filename}")
    print(f"Silicone mold saved as {silicone_mold_filename}")

# Main function to orchestrate the mold generation process
def main(filepath):
    """
    Full pipeline for mold generation from a 3D model file.
    """
    # Step 1: Load model
    model = load_model(filepath)
    
    # Step 2: Calculate escape paths (for mold parting)
    escape_paths = calculate_escape_paths(model)
    
    # Step 3: Generate parting surfaces
    parting_surface = create_parting_surface(model, escape_paths)
    
    # Step 4: Create the composite mold (rigid shell + flexible inner part)
    hard_shell = create_hard_shell(model, parting_surface)
    if hard_shell is None:
        print("Error: Could not create hard shell.")
        return
    
    silicone_mold = create_flexible_mold(model, parting_surface)
    if silicone_mold is None:
        print("Error: Could not create flexible mold.")
        return
    
    # Step 5: Export the mold parts
    export_mold_parts(hard_shell, silicone_mold)

# Run the pipeline on a provided 3D model file (example .obj file)
input_file = "cone.obj"
main(input_file)
