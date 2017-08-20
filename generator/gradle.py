import os
from pathlib import Path

__all__ = ('GradleProject', 'GradleRootProject',)

class GradleProject:

    def __init__(self, project_id: str, class_count: int, method_count: int):
        self.project_id = project_id
        self.class_count = class_count
        self.method_count = method_count

    def generate(self, parent: Path) -> str:
        project_path = parent / self.project_id

        # Create project folder
        os.makedirs(parent / self.project_id, exist_ok=False)

        # Write gradle file
        with open(project_path / 'build.gradle', mode='w') as f:
            f.write(self.build_gradle_content())

        # Write sources
        self.write_sources(project_path)

        return project_path

    def build_gradle_content(self):
        raise NotImplementedError()

    def write_sources(self, project_path: Path):
        pass


class GradleRootProject(GradleProject):

    def __init__(self, project_id: str, projects=[]):
        super().__init__(project_id, 0, 0)
        self.projects = projects

    def generate(self, parent: Path) -> str:
        project_path = super().generate(parent)

        with open(project_path / 'settings.gradle', mode='w') as f:
            f.write(self.settings())

        return project_path

    def build_gradle_content(self):
        return _build

    def settings(self):
        return _settings % {
            'project_id': self.project_id,
            'includes': '\n'.join("include ':%s'" % project for project in self.projects)
        }

_settings = """\
%(includes)s

rootProject.name = '%(project_id)s'
// See https://github.com/gradle/gradle/blob/master/settings.gradle
rootProject.children.each {project ->
    String fileBaseName = project.name
    String projectDirName = "projects/$fileBaseName"
    project.projectDir = new File(settingsDir, projectDirName)
    //project.buildFileName = "${fileBaseName}.gradle"
    assert project.projectDir.isDirectory()
    assert project.buildFile.isFile()
}
"""

_build = """\
buildscript {
    ext.kotlin_version = '1.1.4'
    repositories {
        google()
        jcenter()
    }
    dependencies {
        classpath 'com.android.tools.build:gradle:2.3.3'
        classpath "org.jetbrains.kotlin:kotlin-gradle-plugin:$kotlin_version"
    }
}
allprojects {
    repositories {
        google()
        jcenter()
    }
}
ext {
    compile_sdk_version = 26
    build_tools_version = '26.0.1'
    min_sdk_version = 21
    target_sdk_version = compile_sdk_version
    support_library_version = '26.0.1'
}
"""