#!/usr/bin/env python3

def write(filename, content):
    with open('build/' + filename + '.scenario', mode='w') as f:
        f.write(content)

gradle_version = '4.2.1'
common = """
    versions = ["%(gradle_version)s"]
    gradle-args = ["--parallel"]
    warm-ups = 1
    cleanup-tasks = ["clean"]
    tasks = ["app:assembleDebug"]""" % locals()

write("single_app", """\
assemble_single_app {%(common)s
}
incremental_single_app {%(common)s
    apply-abi-change-to = "projects/app/src/main/java/lib/app/Cls9000.java"
}
""" % locals())

write("app_lib", """\
assemble_app_lib {%(common)s
}
incremental_app {%(common)s
    apply-abi-change-to = "projects/app/src/main/java/lib/app/Cls0.java"
}
incremental_lib {%(common)s
    apply-abi-change-to = "projects/lib0/src/main/java/lib/lib0/Cls0.java"
}
""" % locals())

write("sample", ''.join("""\
assemble_sample_%(suffix)s {%(common)s
    gradle-args = ["--parallel", "-Pandroid.gradle_plugin=%(agp)s"]
}
incremental_sample_app_%(suffix)s {%(common)s
    gradle-args = ["--parallel", "-Pandroid.gradle_plugin=%(agp)s"]
    apply-abi-change-to = "projects/app/src/main/java/lib/app/Cls0.java"
}
incremental_sample_lib_%(suffix)s {%(common)s
    gradle-args = ["--parallel", "-Pandroid.gradle_plugin=%(agp)s"]
    apply-abi-change-to = "projects/java/src/main/java/lib/java/Cls0.java"
}
""" % {
    'common': common,
    'suffix': suffix,
    'agp': agp
} for suffix, agp in [('233', '2.3.3'), ('agp_beta', '3.0.0-beta4')]))
