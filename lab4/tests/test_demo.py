from demo import run_graph_demo, run_sort_demo


def test_demo_functions(capsys):
    run_sort_demo()
    run_graph_demo()
    output = capsys.readouterr().out
    assert "Comb sort" in output
    assert "Graph snapshot" in output
