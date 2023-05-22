import re


def get_coverage_line(lines):
    n = 0
    for line in lines:
        if line.startswith('---------- coverage: platform '):
            return n
        n += 1
    return None


def get_coverage_table(filename: str):

    final_coverage = []
    total_coverage = ""

    with open(filename) as f:
        lines = f.read().splitlines()
        n_coverage_line = get_coverage_line(lines)
        coverage_lines = lines[n_coverage_line:]
        for line in coverage_lines[1:-1]:
            if re.match(r"^-+$", line) or len(line) == 0:
                continue
            line = re.sub(r"-{2,}", '', line)
            line = re.sub(r"\s{1,}", ' ', line)
            line = re.sub(r"\b\s", '|', line)
            line = line.replace('% ', '%|')
            line = line.replace('__', r'\_\_')
            final_coverage.append(line.strip())
            if "TOTAL" in line:
                total_coverage = line.split('|')[3].replace('%', '')

        final_coverage.insert(1, '| - | - | - | - | - |')

    return final_coverage, total_coverage


def save_file(file_body, filename):
    with open(filename, 'w') as f:
        [f.write(f"\n{line}") for line in file_body]


if __name__ == '__main__':
    final_coverage, total_coverage = get_coverage_table('coverage.txt')
    save_file(final_coverage, 'coverage_table.txt')
    save_file([total_coverage], 'total_coverage')
