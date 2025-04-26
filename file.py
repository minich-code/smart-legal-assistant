# import os

# def print_folder_structure(start_path='.'):
#     for root, dirs, files in os.walk(start_path):
#         level = root.replace(start_path, '').count(os.sep)
#         indent = ' ' * 4 * level
#         print(f"{indent}{os.path.basename(root)}/")
#         sub_indent = ' ' * 4 * (level + 1)
#         for f in files:
#             print(f"{sub_indent}{f}")

# # Example usage
# print_folder_structure('.')
import os

def print_folder_structure(start_path='src'):
    if not os.path.exists(start_path):
        print(f"Folder '{start_path}' does not exist.")
        return

    for root, dirs, files in os.walk(start_path):
        level = root.replace(start_path, '').count(os.sep)
        indent = ' ' * 4 * level
        print(f"{indent}{os.path.basename(root)}/")
        sub_indent = ' ' * 4 * (level + 1)
        for f in files:
            print(f"{sub_indent}{f}")

# Example usage
print_folder_structure('src')
