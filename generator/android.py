from pathlib import Path
from .java import JavaProject

_all_ = ('AndroidProject',)

class AndroidProject(JavaProject):

    def __init__(self, project_id: str, class_count: int, method_count: int, library=True, dependencies=[]):
        super().__init__(project_id, class_count, method_count)
        self.library = library
        self.dependencies = dependencies

    def generate(self, parent: Path) -> str:
        project_path = super().generate(parent)
        self.manifest(project_path)

    def build_gradle_content(self):
        return _gradle % {
            'type': 'library' if self.library else "application",
            'applicationId': '' if self.library else "        applicationId 'com.example.app'\n",
            'dependencies': '\n'.join(
                '    compile project(":%s")' % project for project in self.dependencies
            ),
        }

    def manifest(self, project_path: Path):
        with open(project_path / 'src/main/AndroidManifest.xml', mode='w') as f:
            manifest = _manifest_lib if self.library else _manifest_app
            f.write(manifest % {'package_name': self.package})

_gradle = """\
apply plugin: 'com.android.%(type)s'

android {
    compileSdkVersion compile_sdk_version
    buildToolsVersion build_tools_version

    defaultConfig {
%(applicationId)s        minSdkVersion min_sdk_version
        targetSdkVersion target_sdk_version
        versionCode 1
        versionName "1.0"
        multiDexEnabled true
    }
    compileOptions {
        sourceCompatibility JavaVersion.VERSION_1_7
        targetCompatibility JavaVersion.VERSION_1_7
    }
}

dependencies {
    compile "com.android.support:appcompat-v7:$support_library_version"
    compile "com.android.support:recyclerview-v7:$support_library_version"
    compile "com.android.support:support-annotations:$support_library_version"
    compile 'com.android.support:multidex:1.0.1'
%(dependencies)s
}
"""

_manifest_lib = """\
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="%(package_name)s">
</manifest>
"""

_manifest_app = """\
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="%(package_name)s">
    <application
        android:allowBackup="true"
        android:label="Application"
        android:supportsRtl="true">
    </application>
</manifest>
"""
