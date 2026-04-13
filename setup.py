
import os

# Create the monorepo structure
base_path = "/mnt/kimi/output/devsuite"

# Root structure
paths = [
    "packages/cli/src/commands",
    "packages/cli/src/utils",
    "packages/web/app",
    "packages/web/components",
    "packages/web/lib",
    "packages/api-directory/app",
    "packages/api-directory/components",
    "packages/api-directory/data"
]

for path in paths:
    os.makedirs(os.path.join(base_path, path), exist_ok=True)

print("✅ Directory structure created")
print(f"Base path: {base_path}")
