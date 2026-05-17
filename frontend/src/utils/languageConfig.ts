export type LanguageId = 'C++' | 'Python' | 'Java';

export interface CompilerOption {
  value: string;
  label: string;
}

export interface LanguageConfig {
  id: LanguageId;
  label: string;
  defaultCompiler: string;
  compilers: CompilerOption[];
  template: string;
}

const CPP_TEMPLATE = `#include <iostream>

using namespace std;

// Реализуйте алгоритм здесь
int solve() {
    // ваш код
    return 0;
}

//используйте эту функцию для тестирования вашего решения
int main() {
    solve();
    return 0;
}
`;

const PYTHON_TEMPLATE = `def solve():
    """Реализуйте алгоритм здесь."""
    return 0

""используйте эту функцию для тестирования вашего решения"
if __name__ == "__main__":
    solve()
`;

const JAVA_TEMPLATE = `public class Main {
    // Реализуйте алгоритм здесь
    static int solve() {
        return 0;
    }
    // используйте эту функцию для тестирования вашего решения
    public static void main(String[] args) {
        solve();
    }
}
`;

export const LANGUAGE_CONFIGS: LanguageConfig[] = [
  {
    id: 'C++',
    label: 'C/C++',
    defaultCompiler: 'g++',
    compilers: [
      { value: 'g++', label: 'g++ (GCC)' },
      { value: 'gcc', label: 'gcc (GCC)' },
      { value: 'clang++', label: 'clang++ (LLVM)' },
      { value: 'clang', label: 'clang (LLVM)' },
    ],
    template: CPP_TEMPLATE,
  },
  {
    id: 'Python',
    label: 'Python',
    defaultCompiler: 'python',
    compilers: [{ value: 'python', label: 'Python 3' }],
    template: PYTHON_TEMPLATE,
  },
  {
    id: 'Java',
    label: 'Java',
    defaultCompiler: 'javac',
    compilers: [{ value: 'javac', label: 'JDK (javac)' }],
    template: JAVA_TEMPLATE,
  },
];

export const DEFAULT_LANGUAGE: LanguageId = 'C++';

export function getLanguageConfig(language: string): LanguageConfig {
  return LANGUAGE_CONFIGS.find((item) => item.id === language) ?? LANGUAGE_CONFIGS[0];
}

export function getDefaultFormCode(language: string = DEFAULT_LANGUAGE): string {
  return getLanguageConfig(language).template;
}
