import os
import argparse
import hashlib
from PIL import Image
import imagehash
from collections import defaultdict

def find_duplicates(dataset_path, hash_method='phash', threshold=95, action='move'):
    """
    Find and handle duplicate images in dataset directory
    hash_method: 'phash' (perceptual), 'ahash' (average), 'md5' (exact)
    threshold: Similarity percentage (1-100)
    action: 'delete' or 'move' duplicates
    """
    # Create duplicates directory if needed
    dup_dir = os.path.join(dataset_path, 'duplicates')
    if action == 'move' and not os.path.exists(dup_dir):
        os.makedirs(dup_dir)

    # Initialize hashing parameters
    hash_size = 8
    threshold_distance = int((100 - threshold) * hash_size * hash_size / 100)

    hashes = defaultdict(list)
    total_duplicates = 0

    print(f"Scanning {dataset_path} for duplicates...")
    
    for root, _, files in os.walk(dataset_path):
        if root == dup_dir:
            continue
        
        for filename in sorted(files):
            if not filename.lower().endswith(('png', 'jpg', 'jpeg')):
                continue

            filepath = os.path.join(root, filename)
            
            try:
                with Image.open(filepath) as img:
                    # Calculate appropriate hash
                    if hash_method == 'md5':
                        file_hash = hashlib.md5(img.tobytes()).hexdigest()
                    else:
                        if hash_method == 'phash':
                            file_hash = imagehash.phash(img, hash_size=hash_size)
                        else:  # ahash
                            file_hash = imagehash.average_hash(img, hash_size=hash_size)
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")
                continue

            # Check for duplicates
            is_duplicate = False
            for existing_hash, existing_files in hashes.items():
                if hash_method == 'md5':
                    similarity = 100 if file_hash == existing_hash else 0
                else:
                    distance = file_hash - existing_hash
                    similarity = 100 - (distance / (hash_size * hash_size) * 100)
                
                if similarity >= threshold:
                    print(f"Duplicate found: {filename} matches {existing_files[0]} ({similarity:.1f}%)")
                    is_duplicate = True
                    break

            if is_duplicate:
                total_duplicates += 1
                handle_duplicate(filepath, dup_dir, action)
            else:
                hashes[file_hash].append(filename)

    print(f"\nFound {total_duplicates} duplicates. Action taken: {action}")

def handle_duplicate(filepath, dup_dir, action):
    """Handle duplicate file based on specified action"""
    try:
        if action == 'delete':
            os.remove(filepath)
        elif action == 'move':
            new_path = os.path.join(dup_dir, os.path.basename(filepath))
            os.rename(filepath, new_path)
    except Exception as e:
        print(f"Error handling duplicate {filepath}: {str(e)}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Dataset Deduplicator')
    parser.add_argument('dataset_path', help='Path to dataset directory')
    parser.add_argument('--method', choices=['phash', 'ahash', 'md5'], 
                       default='phash', help='Hashing method (default: phash)')
    parser.add_argument('--threshold', type=int, default=95,
                       help='Similarity threshold percentage (1-100)')
    parser.add_argument('--action', choices=['delete', 'move'], 
                       default='move', help='Action for duplicates (default: move)')
    
    args = parser.parse_args()
    
    find_duplicates(
        dataset_path=args.dataset_path,
        hash_method=args.method,
        threshold=args.threshold,
        action=args.action
    )
