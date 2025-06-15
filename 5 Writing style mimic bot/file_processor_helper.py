
def process_text_file(file_path, output_path, transformer):
    """Transform entire text files"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split into paragraphs for better processing
    paragraphs = content.split('\n\n')
    transformed_paragraphs = []
    
    for para in paragraphs:
        if para.strip():
            transformed = transformer.transform_text(para)
            transformed_paragraphs.append(transformed)
        else:
            transformed_paragraphs.append('')
    
    # Save transformed content
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(transformed_paragraphs))
    
    print(f"Transformed file saved to: {output_path}")

# Usage
# process_text_file("input.txt", "output_academic.txt", transformer)