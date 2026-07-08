import os
import shutil
import tempfile
import timeit
import importlib.util

spec = importlib.util.spec_from_file_location("f_dotfiles", "f-dotfiles.py")
f_dotfiles = importlib.util.module_from_spec(spec)
spec.loader.exec_module(f_dotfiles)

def setup_dummy_files(base_dir, num_dirs=50, files_per_dir=200):
    """Sets up 10,000 files for benchmarking."""
    for i in range(num_dirs):
        dir_path = os.path.join(base_dir, f"dir_{i}")
        os.makedirs(dir_path)
        for j in range(files_per_dir):
            file_path = os.path.join(dir_path, f"file_{j}.txt")
            with open(file_path, "w") as f:
                if j % 2 == 0:
                    f.write(f"# file_{j}.txt: This is a description\n")
                f.write("Line 1\nLine 2\nLine 3\nLine 4\nLine 5\nLine 6\nLine 7\nLine 8\nLine 9\nLine 10\n")

def run_benchmark():
    base_dir = tempfile.mkdtemp()
    print(f"Setting up dummy files in {base_dir}...")
    setup_dummy_files(base_dir)

    try:
        def test_func():
            f_dotfiles.extract_descriptions(base_dir)

        print("Warming up...")
        test_func()

        number = 5
        print(f"Running benchmark ({number} iterations)...")
        time_taken = timeit.timeit(test_func, number=number)
        print(f"Time taken for {number} runs: {time_taken:.4f} seconds")
        print(f"Average time per run: {time_taken/number:.4f} seconds")
    finally:
        shutil.rmtree(base_dir)

if __name__ == "__main__":
    run_benchmark()
