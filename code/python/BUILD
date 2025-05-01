package(default_visibility = ["//visibility:public"])

py_binary(
    name = "run_experiment",
    srcs = ["run_experiment.py"],
    deps = [
        "//moralmachines_task",
        "//llm_scheduler/config_tools",
        "//llm_scheduler/execution_environment",
        "//llm_scheduler/runner",
    ],
    python_version = "PY3",
)
