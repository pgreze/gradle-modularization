from .java import JavaProject
from .android import AndroidProject

__all__ = ('KotlinProject', 'KotlinAndroidProject',)

class KotlinMixin:

    def build_gradle_content(self):
        return _android_gradle if self.android else _gradle

    def source_content(self, class_idx, methods_per_class):
        class_name = 'Cls%s' % class_idx
        methods = ''.join([
            _function % {
                'method_idx': "%sByCls%s" % (method_idx, class_idx),
                'body': self.resolve_body(method_idx, class_idx)
            } for method_idx in range(methods_per_class)
        ])
        return (
            _file_content % {
                'package': self.package,
                'class_name': class_name,
                'methods': methods,
            },
            class_name + '.kt',
        )

    def resolve_body(self, method_idx, class_idx):
        if method_idx == 0:
            return '' if class_idx == 0 else 'fct0ByCls%s()' % str(class_idx - 1)
        else:
            return 'fct%sByCls%s()' % (method_idx - 1, class_idx)

class KotlinProject(KotlinMixin, JavaProject):
    android = False

class KotlinAndroidProject(KotlinMixin, AndroidProject):
    android = True

_gradle = """\
apply plugin: 'kotlin'

sourceCompatibility = "1.7"
targetCompatibility = "1.7"

dependencies {
    compile "org.jetbrains.kotlin:kotlin-stdlib:$kotlin_version"
}
"""

_android_gradle = """\
apply plugin: 'com.android.library'
apply plugin: 'kotlin-android'

android {
    compileSdkVersion compile_sdk_version
    buildToolsVersion build_tools_version

    defaultConfig {
        minSdkVersion min_sdk_version
        targetSdkVersion target_sdk_version
        versionCode 1
        versionName "1.0"
    }
}
dependencies {
    compile "com.android.support:appcompat-v7:$support_library_version"
    compile "org.jetbrains.kotlin:kotlin-stdlib-jre7:$kotlin_version"
    testCompile 'junit:junit:4.12'
}

"""

_file_content = """\
package %(package)s

%(methods)s
"""

_function = """
fun fct%(method_idx)s() {
    %(body)s
}
"""