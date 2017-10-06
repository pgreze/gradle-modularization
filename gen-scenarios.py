#!/usr/bin/env python3

def write(filename, content):
    with open('build/' + filename + '.scenario', mode='w') as f:
        f.write(content)

gradle_version = '4.2.1'
common = """
    versions = ["%(gradle_version)s"]
    gradle-args = ["--parallel"]
    warm-ups = 1
    tasks = ["app:assembleDebug"]""" % locals()

# SAMPLE

write("sample", ''.join("""\
assemble_sample_%(suffix)s {%(common)s
    gradle-args = ["--parallel", "-Pandroid.gradle_plugin=%(agp)s"]
}
inc_sample_app_%(suffix)s {%(common)s
    gradle-args = ["--parallel", "-Pandroid.gradle_plugin=%(agp)s"]
    apply-abi-change-to = "projects/app/src/main/java/lib/app/Cls0.java"
}
inc_sample_lib_%(suffix)s {%(common)s
    gradle-args = ["--parallel", "-Pandroid.gradle_plugin=%(agp)s"]
    apply-abi-change-to = "projects/java/src/main/java/lib/java/Cls0.java"
}
""" % {
    'common': common,
    'suffix': suffix,
    'agp': agp
} for suffix, agp in [('233', '2.3.3'), ('agp_beta', '3.0.0-beta4')]))

# SINGLE_APP

write("single_app", """\
build {%(common)s
}
inc {%(common)s
    apply-abi-change-to = "projects/app/src/main/java/lib/app/Cls9000.java"
}
""" % locals())

# MULTI_3

write("multi_3", """\
build {%(common)s
}
inc_app {%(common)s
    apply-abi-change-to = "projects/app/src/main/java/lib/app/Cls0.java"
}
inc_lib {%(common)s
    apply-abi-change-to = "projects/lib1/src/main/java/lib/lib1/Cls0.java"
}
""" % locals())

# MULTI_10

write("multi_10", """\
build {%(common)s
}
inc_app {%(common)s
    apply-abi-change-to = "projects/app/src/main/java/lib/app/Cls0.java"
}
inc_lib1 {%(common)s
    apply-abi-change-to = "projects/lib1/src/main/java/lib/lib1/Cls0.java"
}
inc_lib3 {%(common)s
    apply-abi-change-to = "projects/lib3/src/main/java/lib/lib3/Cls0.java"
}
inc_lib7 {%(common)s
    apply-abi-change-to = "projects/lib7/src/main/java/lib/lib7/Cls0.java"
}
inc_lib9 {%(common)s
    apply-abi-change-to = "projects/lib9/src/main/java/lib/lib9/Cls0.java"
}
""" % locals())

# MULTI_100

write("multi_100", """\
build {%(common)s
}
inc_app {%(common)s
    apply-abi-change-to = "projects/app/src/main/java/lib/app/Cls0.java"
}
inc_lib19 {%(common)s
    apply-abi-change-to = "projects/lib19/src/main/java/lib/lib19/Cls0.java"
}
inc_lib39 {%(common)s
    apply-abi-change-to = "projects/lib39/src/main/java/lib/lib39/Cls0.java"
}
inc_lib79 {%(common)s
    apply-abi-change-to = "projects/lib79/src/main/java/lib/lib79/Cls0.java"
}
inc_lib99 {%(common)s
    apply-abi-change-to = "projects/lib99/src/main/java/lib/lib99/Cls0.java"
}
""" % locals())
