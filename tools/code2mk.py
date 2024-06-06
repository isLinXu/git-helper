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

    def generate_markdown(self):
        with open(self.output_file, 'w', encoding='utf-8') as md_file:
            for root, dirs, files in os.walk(self.repo_path):
                dirs[:] = [d for d in dirs if d not in self.ignored]
                for file in files:
                    if file in self.ignored or file.endswith('.md') or file.endswith('.markdown'):
                        continue

                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, self.repo_path)
                    indent_level = relative_path.count(os.path.sep)
                    indent = '  ' * indent_level
                    title_indent = '#' * (indent_level + 1)

                    md_file.write(f'{title_indent} {relative_path}\n\n')

                    try:
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

if __name__ == '__main__':
    # repo_path = '/Users/gatilin/PycharmProjects/yolo-lab/yolox'
    # output_file = 'output7.md'

    # repo_path = '/Users/gatilin/PycharmProjects/yolo-lab/yolov9'
    # output_file = 'yolov9.md'
    # repo_path = '/Users/gatilin/PycharmProjects/yolo-lab/ultralytics'
    # output_file = 'ultralytics.md'
    # repo_path = '/Users/gatilin/PycharmProjects/yolo-lab/yolov7'
    # output_file = 'yolov7.md'
    # repo_path = '/Users/gatilin/PycharmProjects/yolo-lab/yolov6'
    # output_file = 'yolov6.md'
    # repo_path = '/Users/gatilin/PycharmProjects/yolo-lab/yolov5'
    # output_file = 'yolov5.md'
    repo_path = '/Users/gatilin/PycharmProjects/yolo-lab/yolov4'
    output_file = 'yolov4.md'

    code_to_md = CodeToMarkdown(repo_path, output_file)
    code_to_md.generate_markdown()