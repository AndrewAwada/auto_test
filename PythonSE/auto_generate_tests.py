def generate_pytest_from_auto_tests(
    tests,
    package,
    module_name,
    function_name,
    timeout=5,
    output_file="test_generated.py",
):
    """
    Generate pytest/expecttest tests using only the output of auto_generate_tests.

    If "real return" is not None:
        generate a normal assert.

    If "real return" is None:
        generate an expect test that snapshots the actual runtime result.
    """

    lines = []

    lines.append("import expecttest")
    lines.append("import pytest")
    lines.append(f"from {package}.{module_name} import {function_name}")
    lines.append("")
    lines.append(f"TIMEOUT = {timeout}")
    lines.append("")
    lines.append("class TestGeneratedSymbolicTests(expecttest.TestCase):")
    lines.append("")

    generated_count = 0

    for i, test in enumerate(tests):
        inputs = test.get("inputs")

        # Skip unsat paths or paths where no concrete input was generated.
        if inputs is None:
            continue

        expected_return = test.get("real return")
        pc = test.get("pc")

        # Preserve argument order using dict insertion order.
        # This assumes auto_generate_tests builds inputs in function-argument order.
        args = list(inputs.values())
        args_str = ", ".join(repr(arg) for arg in args)

        test_name = f"test_{function_name}_generated_{i}"

        lines.append( "    @pytest.mark.timeout(TIMEOUT)")
        lines.append(f"    def {test_name}(self):")
        lines.append(f"        # path constraint: {pc}")
        lines.append(f"        result = {function_name}({args_str})")

        if expected_return is not None:
            lines.append(f"        assert result == {repr(expected_return)}")
        else:
            lines.append("        self.assertExpectedInline(")
            lines.append("            str(result),")
            lines.append('            """\\')
            lines.append("<expect output not recorded yet>")
            lines.append('""",')
            lines.append("        )")

        lines.append("")
        generated_count += 1

    if generated_count == 0:
        lines.append("    def test_no_generated_tests(self):")
        lines.append('        raise AssertionError("No satisfiable generated tests found")')
        lines.append("")

    generated_code = "\n".join(lines)

    with open(output_file, "w") as f:
        f.write(generated_code)

    return generated_code
