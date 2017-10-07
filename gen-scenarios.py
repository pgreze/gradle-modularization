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

# Projects number benchs

def multi(name, inc_targets):
    write(name, ("""\
build {%(common)s
}
inc_app {%(common)s
    apply-abi-change-to = "projects/app/src/main/java/lib/app/Cls0.java"
}
""" % globals()) + "".join(
"""\
inc_lib%(tgt)s {%(common)s
    apply-abi-change-to = "projects/lib%(tgt)s/src/main/java/lib/lib%(tgt)s/Cls0.java"
}
""" % {'tgt': tgt, 'common': common} for tgt in inc_targets))

multi("single_app", [])
multi("multi_3", [1])
multi("multi_5", [1, 3])
multi("multi_8", [1, 3, 7])
multi("multi_10", [1, 3, 7, 9])
multi("multi_30", [7, 9, 19])
multi("multi_50", [7, 9, 19, 39])
multi("multi_80", [9, 19, 39, 79])
multi("multi_100", [9, 19, 39, 79, 99])
