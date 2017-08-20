from pathlib import Path
import generator

if __name__ == '__main__':
    # Generate all projects
    path = Path('build/')
    projects = [
        generator.JavaProject('java', 2, 10),
        generator.KotlinProject('kotlin', 3, 15),
        generator.KotlinAndroidProject('kotlin_android', 4, 20, library=False),
        generator.AndroidProject('android_lib', 3, 15, library=True),
        generator.AndroidProject('android_app', 3, 15, library=False, dependencies=[
            'java', 'kotlin', 'kotlin_android', 'android_lib',
        ]),
    ]

    # Generate root project
    root_project = generator.GradleRootProject('multi', projects=[p.project_id for p in projects])
    multi_project_path = root_project.generate(path)

    # And sub projects
    for project in projects:
        project.generate(multi_project_path / 'projects/')
