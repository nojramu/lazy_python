import os
import re

# list of file extensions considered as text files modify as needed
textfileextensions = ('txt', 'py', 'md', 'html', 'css', 'js', 'csv')

# function to sanitize file names by converting to lowercase and removing special characters
def sanitize_filename(filename, word_to_remove=None):
    # keep the period intact while removing other special characters and converting to lowercase
    sanitized_filename = re.sub(r'[^\w\s.-]', '', filename).lower().replace('-', ' ').replace('_', ' ')
    
    # remove a choosen word if specified
    if word_to_remove:
        sanitized_filename = re.sub(r'\b' + re.escape(word_to_remove) + r'\b', '', sanitized_filename)
    
    return sanitized_filename

# function to sanitize file content by converting to lowercase and removing special characters
def sanitize_file_content(content):
    # convert content to lowercase and remove special characters
    return re.sub(r'[^\w\s.-]', '', content).lower()

# function to process all files in the current directory
def process_files_in_current_directory(word_to_remove=None):
    # get the current directory where the script is located
    current_directory = os.getcwd()
    
    for root, dirs, files in os.walk(current_directory):
        for filename in files:
            old_filepath = os.path.join(root, filename)
            # sanitize the filename
            new_filename = sanitize_filename(filename, word_to_remove)
            new_filepath = os.path.join(root, new_filename)

            # rename the file if necessary
            if old_filepath != new_filepath:
                os.rename(old_filepath, new_filepath)

            # get the file extension
            file_extension = os.path.splitext(new_filename)[1]

            # only process content for text-based files
            if file_extension in textfileextensions:
                try:
                    # try reading the file with utf8 encoding if it fails use latin1
                    with open(new_filepath, 'r', encoding='utf-8') as file:
                        content = file.read()
                except UnicodeDecodeError:
                    try:
                        with open(new_filepath, 'r', encoding='latin1') as file:
                            content = file.read()
                    except Exception as e:
                        print(f"Could not read file {new_filename}: {e}")
                        continue

                # sanitize the file content
                sanitized_content = sanitize_file_content(content)

                # overwrite the file with sanitized content
                with open(new_filepath, 'w', encoding='utf-8') as file:
                    file.write(sanitized_content)

# main function
if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Sanitize file names and content in the current directory.')
    parser.add_argument('--remove', '-r', type=str, help='Remove a choosen word when renaming files.')
    args = parser.parse_args()

    process_files_in_current_directory(args.remove)
    print("Files and content sanitized successfully in the current directory.")

