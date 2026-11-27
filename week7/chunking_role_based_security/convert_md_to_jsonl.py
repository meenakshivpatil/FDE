"""Convert Kubernetes .MD files to JSONL format for RAG ingestion."""
import json
import os
from pathlib import Path
from datetime import datetime

# Configuration
DATA_DIR = Path(r'C:\min\tech\FDE\week7\chunking_role_based_security\data')
OUTPUT_FILE = DATA_DIR / 'kube_documents.jsonl'
TENANT_ID = 'DEMO'

# Department mapping from folder names
DEPARTMENT_MAPPING = {
    'Application_Engineering': 'Application_Engineering',
    'Platform_Engineering': 'Platform_Engineering',
    'Security_Engineering': 'Security_Engineering',
    'shared': 'shared'
}

# Folder prefixes for document IDs
FOLDER_PREFIXES = {
    'Application_Engineering': 'APP-ENG',
    'Platform_Engineering': 'PLAT-ENG',
    'Security_Engineering': 'SEC-ENG',
    'shared': 'SHARED'
}

def sanitize_filename_to_id(filename):
    """Convert markdown filename to ID suffix (e.g., 'cron-jobs.md' -> '001')."""
    return filename.replace('.md', '').replace('-', '_').upper()

def extract_description_from_frontmatter(content, fallback_filename=''):
    """Extract description from YAML frontmatter in markdown content.
    Falls back to formatted filename if no description found."""
    lines = content.split('\n')
    
    # Check if file starts with frontmatter (---)
    if not lines[0].strip().startswith('---'):
        return format_filename_as_title(fallback_filename)
    
    in_frontmatter = False
    description_lines = []
    capturing_description = False
    
    for i, line in enumerate(lines):
        # Start of frontmatter
        if i == 0 and line.strip().startswith('---'):
            in_frontmatter = True
            continue
        
        # End of frontmatter
        if in_frontmatter and i > 0 and line.strip().startswith('---'):
            break
        
        # Look for description field
        if in_frontmatter and line.strip().startswith('description:'):
            capturing_description = True
            # Get the value after 'description:'
            desc_value = line.split('description:', 1)[1].strip()
            if desc_value.startswith('>'):
                # Multi-line description (>- or >)
                desc_value = ''
            if desc_value and not desc_value.startswith('>'):
                description_lines.append(desc_value)
            continue
        
        # Continue capturing multi-line description
        if capturing_description and in_frontmatter:
            # Stop if we hit another field (starts with key:)
            if line and not line.startswith(' ') and ':' in line:
                break
            # Continue capturing indented lines
            if line.startswith('  '):
                description_lines.append(line.strip())
    
    if description_lines:
        # Join and clean up
        description = ' '.join(description_lines)
        # Remove markdown links and extra formatting
        description = description.replace('{{< ', '').replace(' >}}', '')
        return description.strip()
    
    # No description found - use filename as fallback
    return format_filename_as_title(fallback_filename)

def format_filename_as_title(filename):
    """Convert filename to a readable title.
    E.g., 'cron-jobs.md' -> 'Cron Jobs', 'pod_security.md' -> 'Pod Security'"""
    if not filename:
        return "Untitled"
    
    # Remove .md extension
    name = filename.replace('.md', '')
    # Replace hyphens and underscores with spaces
    name = name.replace('-', ' ').replace('_', ' ')
    # Title case
    name = name.title()
    return name

def process_folder(folder_path, folder_name, doc_counter):
    """Process all .md files in a folder."""
    documents = []
    department = DEPARTMENT_MAPPING.get(folder_name, folder_name)
    prefix = FOLDER_PREFIXES.get(folder_name, 'DOC')
    
    # Get all .md files in this folder
    md_files = sorted(folder_path.glob('*.md'))
    
    print(f"\n📁 Processing folder: {folder_name}")
    print(f"   Found {len(md_files)} markdown files")
    
    for idx, md_file in enumerate(md_files, 1):
        try:
            # Read the markdown file
            content = md_file.read_text(encoding='utf-8')
            
            # Extract title from description in YAML frontmatter, or use filename as fallback
            title = extract_description_from_frontmatter(content, md_file.name)
            
            # Generate document ID
            document_id = f"{prefix}-{idx:03d}"
            
            # Create the JSON object
            doc = {
                "document_id": document_id,
                "tenant_id": TENANT_ID,
                "department": department,
                "title": title,
                "visibility": "department",
                "permitted_groups": [department] if department != 'shared' else ['shared'],
                "version": 1,
                "source_path": f"kubernetes/{folder_name}/{md_file.name}",
                "content": content
            }
            
            documents.append(doc)
            print(f"   ✓ {document_id}: {title[:60]}")
            
        except Exception as e:
            print(f"   ✗ Error processing {md_file.name}: {e}")
    
    return documents

def main():
    """Main conversion process."""
    print("=" * 70)
    print("KUBERNETES MARKDOWN TO JSONL CONVERTER")
    print("=" * 70)
    print(f"Source directory: {DATA_DIR}")
    print(f"Output file: {OUTPUT_FILE}")
    print(f"Tenant ID: {TENANT_ID}")
    
    if not DATA_DIR.exists():
        print(f"\n✗ Error: Directory not found: {DATA_DIR}")
        return False
    
    all_documents = []
    
    # Process each folder
    for folder_name in DEPARTMENT_MAPPING.keys():
        folder_path = DATA_DIR / folder_name
        
        if not folder_path.exists():
            print(f"\n⚠ Folder not found: {folder_name}")
            continue
        
        if not folder_path.is_dir():
            print(f"\n⚠ Not a directory: {folder_name}")
            continue
        
        # Process this folder
        docs = process_folder(folder_path, folder_name, len(all_documents))
        all_documents.extend(docs)
    
    # Write to JSONL file
    print(f"\n" + "=" * 70)
    print(f"Writing {len(all_documents)} documents to JSONL...")
    print("=" * 70)
    
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            for doc in all_documents:
                f.write(json.dumps(doc) + '\n')
        
        print(f"✓ Successfully wrote {len(all_documents)} documents")
        print(f"✓ Output file: {OUTPUT_FILE}")
        
        # Print summary
        print(f"\n📊 SUMMARY BY DEPARTMENT:")
        dept_summary = {}
        for doc in all_documents:
            dept = doc['department']
            dept_summary[dept] = dept_summary.get(dept, 0) + 1
        
        for dept, count in sorted(dept_summary.items()):
            print(f"   {dept}: {count} documents")
        
        print(f"\n✓ Conversion completed successfully!")
        return True
        
    except Exception as e:
        print(f"✗ Error writing to output file: {e}")
        return False

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)
