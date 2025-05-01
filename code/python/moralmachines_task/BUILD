package(default_visibility = ["//visibility:public"])

load("@moral_machines_pip_deps//:requirements.bzl", "requirement")

py_library(
    name = "moralmachines_task",
    srcs = [
        "generate_prompts.py",
        "prompt_templates.py",
        "generate_moral_machine_scenarios.py",
        "config.py",
    ],
    deps = [
        requirement("google_cloud_translate"),
    ],
)

py_binary(
    name = "generate_prompts",
    srcs = ["generate_prompts.py"],
    deps = [
        ":moralmachines_task",
    ],
    python_version = "PY3",
)

py_binary(
    name = "generate_moralmachines_task",
    srcs = ["generate_moral_machine_scenarios.py"],
    deps = [
        ":moralmachines_task",
    ],
    main = "generate_moral_machine_scenarios.py",
    python_version = "PY3",
)

py_binary(
    name = "parse_output",
    srcs = ["parse_output.py"],
    deps = [
        ":moralmachines_task",
        requirement("pandas"),
    ],
    python_version = "PY3",
)
