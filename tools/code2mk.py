import argparse
import os


class CodeToMarkdown:
    def __init__(self, repo_path, output_file):
        self.repo_path = repo_path
        self.output_file = output_file
        self.languages = {
            '.py': 'python',
            '.js': 'javascript',
            '.java': 'java',
            '.cpp': 'cpp',
            '.c': 'c',
            '.go': 'go',
            '.rb': 'ruby',
            '.php': 'php',
            '.rs': 'rust',
            '.sh': 'bash',
            '.css': 'css',
            '.html': 'html',
        }
        # self.ignored = {'.git', '__pycache__', '.DS_Store'}
        self.ignored = {
            '.ipynb', '.ipynb_checkpoints', '.ipynb_checkpoints',
            '.git', '__pycache__', '.DS_Store',
            '.vscode', '.idea', '.settings', 'node_modules',
            'dist', 'build', 'output', 'bin', 'obj',
            '.classpath', '.project', '.gradle',
            'venv', '.virtualenv', 'composer.lock', 'package-lock.json',
            'yarn.lock', 'Gemfile.lock', 'Cargo.lock', 'Gopkg.lock',
            'Pipfile.lock', 'poetry.lock', 'requirements.txt',
            '.gitignore', '.gitattributes', '.gitmodules', 'README.md',
            'LICENSE', '.travis.yml', '.circleci', 'appveyor.yml',
            'Dockerfile', 'docker-compose.yml', 'Vagrantfile', 'Makefile',
            'CMakeLists.txt', 'setup.py', 'MANIFEST.in',
        }

    def generate_tree(self, path, indent=''):
        tree = ''
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path) and item not in self.ignored:
                tree += f'{indent}- {item}\n'
                tree += self.generate_tree(item_path, indent + '  ')
            elif os.path.isfile(item_path) and item not in self.ignored:
                tree += f'{indent}- {item}\n'
        return tree

    def generate_markdown(self):
        with open(self.output_file, 'w', encoding='utf-8') as md_file:

            # Get repo_name from repo_path
            repo_name = os.path.basename(self.repo_path)

            # Write repo_name as title
            md_file.write(f'# {repo_name}\n\n')

            # Write directory tree
            md_file.write("Directory tree" + '\n')
            tree = self.generate_tree(self.repo_path)
            md_file.write(tree + '\n')
            md_file.write("---" + '\n')
            md_file.write("<!-- TOC -->" + '\n')
            # Write code snippets
            for root, dirs, files in os.walk(self.repo_path):
                dirs[:] = [d for d in dirs if d not in self.ignored]
                for file in files:
                    if file in self.ignored or file.endswith('.md') or file.endswith('.markdown') \
                            or file.endswith('.ipynb') or file.endswith('.json') \
                            or file.endswith('.jpg') or file.endswith('.png') or file.endswith('.jpeg')\
                            or file.endswith('.mp4') or file.endswith('.pdf') or file.endswith('.ttf')\
                            or file.endswith('.bin') or file.endswith('.jar') \
                            or file.endswith('.gz') or file.endswith('.zip') or file.endswith('.gif') \
                            or file.endswith('.ico') or file.endswith('.lib') or file.endswith('.a') or file.endswith('.so'):
                        continue

                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, self.repo_path)
                    indent_level = relative_path.count(os.path.sep)
                    indent = '  ' * indent_level
                    title_indent = '#' * (indent_level + 1)

                    md_file.write(f'{title_indent} {relative_path}\n\n')

                    try:
                        if os.path.exists(file_path):
                            with open(file_path, 'r', encoding='utf-8') as code_file:
                                file_ext = os.path.splitext(file)[1]
                                lang = self.languages.get(file_ext, '')
                                code_block = f'```{lang}\n'
                                for line in code_file:
                                    code_block += line
                                code_block += '```\n\n'
                                md_file.write(code_block)
                    except UnicodeDecodeError:
                        print(f"Unable to read file due to encoding issues: {file_path}")

def main(repo_path, output_file):
    code_to_md = CodeToMarkdown(repo_path, output_file)
    code_to_md.generate_markdown()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert code repository to Markdown')
    parser.add_argument('repo_path', help='Path to the code repository')
    parser.add_argument('output_file', help='Output Markdown file')
    args = parser.parse_args()

    main(args.repo_path, args.output_file)