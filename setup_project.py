import os

def create_project_structure():
    base_path = "."
    template = """# Day {day}: [Tip Title]

## Description
[Description of the tip]

## Code Snippet
```csharp
// Code here
```

## Resources
- [Link to documentation]
"""

    for i in range(1, 101):
        # Format folder name with leading zeros, e.g., Day_001, Day_099, Day_100
        folder_name = f"Day_{i:03d}"
        folder_path = os.path.join(base_path, folder_name)
        
        # Create directory
        os.makedirs(folder_path, exist_ok=True)
        
        # Create README.md
        readme_path = os.path.join(folder_path, "README.md")
        with open(readme_path, "w") as f:
            f.write(template.format(day=i))
            
    print("Successfully created folders Day_001 to Day_100 with README.md files.")

if __name__ == "__main__":
    create_project_structure()
