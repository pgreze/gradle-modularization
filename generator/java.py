import os
from pathlib import Path
from .gradle import GradleProject

class JavaProject(GradleProject):

    def __init__(self, project_id: str, class_count: int, method_count: int):
        super().__init__(project_id, class_count, method_count)
        self.package = 'lib.%s' % self.project_id

    def build_gradle_content(self):
        return _gradle

    def write_sources(self, project_path: Path):
        src_output = project_path / ('src/main/java/lib/%s' % (self.project_id))
        os.makedirs(str(src_output))
        for class_idx in range(self.class_count):
            content, filename = self.source_content(class_idx, int(self.method_count / self.class_count))
            with open(str(src_output / filename), mode='w') as f:
                f.write(content)

    def source_content(self, class_idx, methods_per_class):
        class_name = 'Cls%s' % class_idx
        methods = ''.join([
            _function % {
                'method_idx': method_idx,
                'body': self.function_body(method_idx, class_idx),
            } for method_idx in range(methods_per_class)
        ])
        return (
            _file_content % {
                'package': self.package,
                'class_name': class_name,
                'methods': methods,
            },
            class_name + '.java',
        )

    def function_body(self, method_idx, class_idx):
        if method_idx == 0:
            return '' if class_idx == 0 else 'new Cls%s().fct0();' % (class_idx - 1)
        else:
            return 'fct%s();' % (method_idx - 1)

_gradle = """\
apply plugin: 'java'

repositories {
    jcenter()
}
dependencies {
    testCompile 'junit:junit:4.12'
}
"""

_file_content = """\
package %(package)s;

public class %(class_name)s {
%(methods)s
}
"""

_function = """
    public void fct%(method_idx)s() {
        %(body)s
    }
"""