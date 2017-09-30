from gtestm.netcfg import config
from gtestm.run import general as gen
from gtestm.utils import testdata


def linear_run(cfg: config.Config, td: testdata.TestData, sd: testdata.StateData):
    """
    Run all tests within the remote servers in a serial fashion (not multi-threaded)
    :param sd:
    :param cfg: The configuration data for running the tests
    :param td: The TestData object for holding test information
    :return: None
    """
    remote_test_dir = gen.direc_setup(cfg)

    tests = gen.fetch_test_list(cfg, remote_test_dir)

    sd.set_q(len(tests))

    for test in tests:
        gen.single_run(test, cfg, td=td)
        sd.incre_p()

    return td
