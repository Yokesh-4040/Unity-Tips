import os
import shutil

def rename_days_to_tips():
    base_path = "."
    for i in range(1, 101):
        old_name = f"Day_{i:03d}"
        new_name = f"Tip_{i:03d}"
        
        old_path = os.path.join(base_path, old_name)
        new_path = os.path.join(base_path, new_name)
        
        if os.path.exists(old_path):
            print(f"Renaming {old_name} to {new_name}")
            shutil.move(old_path, new_path)
            
            # Also update the title in the README if it hasn't been manually changed yet
            readme_path = os.path.join(new_path, "README.md")
            if os.path.exists(readme_path):
                with open(readme_path, "r") as f:
                    content = f.read()
                
                if "Day" in content:
                    # Simple replace for the header if it matches the template
                    # Be careful not to replace text in the content that should stay, 
                    # but the template used "Day {day}" so we can target that.
                    new_content = content.replace(f"Day {i}", f"Tip {i}")
                    if new_content != content:
                        with open(readme_path, "w") as f:
                            f.write(new_content)

if __name__ == "__main__":
    rename_days_to_tips()
