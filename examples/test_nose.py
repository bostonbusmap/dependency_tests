from dependency_tests.plugin import requires

@requires("test_b")
def test_a():
    print("a")

def test_b():
    print("b")

@requires("test_d", "test_h")
def test_e():
    print("e")

@requires("test_e")
def test_f():
    print("f")
    
@requires("test_h")
def test_g():
    print("g")

@requires()
def test_h():
    print("h")

@requires(["test_d", "test_b"])
def test_c():
    print("c")

@requires
def test_d():
    print("d")

