import argparse
import time
import llm_scheduler.execution_environment.execution_environment as env
from moralmachines_task.generate_prompts import TrolleyProblem
from llm_scheduler.config_tools.create_sample import create_sample_moralmachine_task_config
from llm_scheduler.runner.task_runner import execute_task


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--execution_id", type=str, help="Execution ID")
    parser.add_argument("--n", type=int, help="Number of configs to generate")
    parser.add_argument("--dimension", type=str, choices=["age", "species", "utilitarianism", "gender"], help="Dimension to test")
    parser.add_argument("--language", type=str, help="Language(s) to test")
    parser.add_argument("--model_key", type=str, choices=["GEMINI_FLASH", "CLAUDE_3_5_HAIKU"], help="LLM Model to test")
    parser.add_argument("-dry_run", action="store_true", default=False, help="Dry run (no LLM calls)")
    args = parser.parse_args()

    if args.execution_id is not None:
        env.init(exe_id=args.execution_id)
    else:
        env.init()

    if args.dimension is None:
        args.dimension = "age"

    # Test for each configured language:
    if args.language:
        languages = args.language.split(',')
    else:
        languages = ["en", "zh", "ja", "fr", "es", "tw"]

    # If dry run, just print some stats and the first problem
    if args.dry_run:
        problem = TrolleyProblem(dimension=args.dimension)
        for lang in languages:
            problem.prepare_prompt(language=lang)
            print(problem.get_code())
    else:
        # Generate n configs
        init_time = time.time()
        for i in range(args.n):
            problem = TrolleyProblem(dimension=args.dimension)
            for lang in languages:
                problem.prepare_prompt(language=lang)
                moral_config = create_sample_moralmachine_task_config(problem, model_key=args.model_key)
                try:
                    execute_task(moral_config)
                except Exception as e:
                    print(e)
            print(f"Finished config {i+1}/{args.n} in {(time.time() - init_time):.3f}s")
            if i < args.n - 1:
                env.print_stats()
                time.sleep(1) # Pause for 1 second briefly
        print("All configs finished")
        env.print_stats()
