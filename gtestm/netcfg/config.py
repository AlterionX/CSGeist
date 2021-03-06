#!/usr/bin/env python3
import getpass


def ainp(store, key, out, secure=True):
    if key not in store or store[key] is None or not store[key]:
        if secure:
            store[key] = getpass.getpass("Enter" + out + ":\n")
        else:
            store[key] = input("Enter" + out + ":\n")
    if not store[key]:
        store[key] = None


class Config:
    # Where everything IS
    DEF_CFG_FILE = "./config"
    SIMULT = 10

    # region Data key strings
    # Remote access data
    GDC_USER_KEY = "remote_user"
    GDC_PASS_KEY = "remote_pass"
    GDC_HOSTNAME_KEY = "remote_host"  # should be accessed dynamically
    # Local access data
    LCL_USER_KEY = "local_user"
    LCL_PASS_KEY = "local_pass"
    LCL_HOSTNAME_KEY = "local_host"  # should be detected
    # Test IO data
    TEST_DIR_KEY = "test_dir"
    PROJ_LOC_KEY = "proj_loc"
    PROJ_DIR_KEY = "proj_dir"
    OUTP_LOC_KEY = "outp_loc"
    OUTP_DIR_KEY = "outp_dir"
    # Assignment
    CURR_PROJ_SEM_KEY = "curr_proj_sem"
    CURR_PROJ_CLS_KEY = "curr_proj_cls"
    CURR_PROJ_NUM_KEY = "curr_proj_num"
    # Timing
    TIME_YR_KEY = "yr"
    TIME_MN_KEY = "mn"
    TIME_DY_KEY = "dy"
    TIME_HR_KEY = "hr"
    TIME_MI_KEY = "mi"
    TIME_SC_KEY = "sc"
    # endregion

    # region Default information
    # GDC_USER_DEF
    # GDC_PASS_DEF
    GDC_HOSTNAME_DEF = "linux.cs.utexas.edu"
    # LCL_USER_DEF
    # LCL_PASS_DEF
    LCL_HOSTNAME_DEF = "linux.cs.utexas.edu"
    # PROJ_LOC_DEF
    # PROJ_DIR_DEF
    OUTP_LOC_DEF = GDC_HOSTNAME_DEF
    OUTP_DIR_DEF = "~/gtestm_cp_dir"
    # CURR_PROJ_SEM_DEF
    # CURR_PROJ_CLS_DEF
    # CURR_PROJ_NUM_DEF
    # TIME_YR_DEF = "year"
    # TIME_MN_DEF = "month"
    # TIME_DY_DEF = "day"
    # TIME_HR_DEF = "hour"
    # TIME_MI_DEF = "minute"
    # TIME_SC_DEF = "second"
    # endregion

    # region Environmental data dictionary
    ENV_VARS = {
        GDC_USER_KEY: None,
        GDC_PASS_KEY: None,
        GDC_HOSTNAME_KEY: GDC_HOSTNAME_DEF,
        LCL_USER_KEY: None,
        LCL_PASS_KEY: None,
        LCL_HOSTNAME_KEY: LCL_HOSTNAME_DEF,
        TEST_DIR_KEY: None,
        PROJ_LOC_KEY: None,
        PROJ_DIR_KEY: None,
        OUTP_LOC_KEY: OUTP_LOC_DEF,
        OUTP_DIR_KEY: OUTP_DIR_DEF,
        CURR_PROJ_SEM_KEY: None,
        CURR_PROJ_CLS_KEY: None,
        CURR_PROJ_NUM_KEY: None,
        TIME_YR_KEY: None,
        TIME_MN_KEY: None,
        TIME_DY_KEY: None,
        TIME_HR_KEY: None,
        TIME_MI_KEY: None,
        TIME_SC_KEY: None
    }
    # endregion

    # region Required data
    REQ_ELEM = [
        (GDC_USER_KEY, " username", False),
        (GDC_PASS_KEY, " password", True),
        (TEST_DIR_KEY, " the parent directory of the source of all the tests", False),
        (PROJ_DIR_KEY, " the parent directory of where your projects are located", False),
        (OUTP_DIR_KEY, " a directory that can be completely scrapped", False),
        (CURR_PROJ_CLS_KEY, " class(cs<code>)", False),
        (CURR_PROJ_SEM_KEY, " semester(<semester letter><year>)", False),
        (CURR_PROJ_NUM_KEY, " project number(p<number>)", False)
    ]

    # endregion

    def __init__(self, cfg_file=DEF_CFG_FILE, delay_login=False):
        self.delay_login = delay_login
        self.store = self._pull(cfg_file)
        self._init(**self.store)

    def check_req(self):
        for key, prompt, _ in Config.REQ_ELEM:
            if key not in self.store or self.store[key] is None or not self.store[key]:
                return True
        return False

    def _pull(self, cfg_file):
        cfg_dict = {}
        # A tuple of all lines not a comment and not empty, assuming proper formatting
        setting_data = list(
            map(
                lambda san_line: tuple(san_line.strip().split(':')),
                filter(
                    lambda line: line and line[0:2] != "//",
                    map(
                        lambda line: line.strip(),
                        open(cfg_file).readlines()
                    )
                )
            )
        )

        for cat, val in setting_data:
            cfg_dict[cat.strip()] = val.strip()

        if self.delay_login:
            return cfg_dict

        for req_key, prompt, hide in Config.REQ_ELEM:
            ainp(cfg_dict, req_key, prompt, secure=hide)

        return cfg_dict

    def _init(
            self,

            remote_user=ENV_VARS[GDC_USER_KEY],
            remote_pass=ENV_VARS[GDC_PASS_KEY],
            remote_host=ENV_VARS[GDC_HOSTNAME_KEY],

            remote_port=22,

            local_user=ENV_VARS[LCL_USER_KEY],
            local_pass=ENV_VARS[LCL_PASS_KEY],
            local_host=ENV_VARS[LCL_HOSTNAME_KEY],

            local_port=22,

            test_dir=ENV_VARS[TEST_DIR_KEY],

            proj_loc=ENV_VARS[PROJ_LOC_KEY],
            proj_dir=ENV_VARS[PROJ_DIR_KEY],

            outp_loc=ENV_VARS[OUTP_LOC_KEY],
            outp_dir=ENV_VARS[OUTP_DIR_KEY],

            curr_proj_cls=ENV_VARS[CURR_PROJ_CLS_KEY],
            curr_proj_sem=ENV_VARS[CURR_PROJ_SEM_KEY],
            curr_proj_num=ENV_VARS[CURR_PROJ_NUM_KEY],

            yr=ENV_VARS[TIME_YR_KEY],
            mn=ENV_VARS[TIME_MN_KEY],
            dy=ENV_VARS[TIME_DY_KEY],
            hr=ENV_VARS[TIME_HR_KEY],
            mi=ENV_VARS[TIME_MI_KEY],
            sc=ENV_VARS[TIME_SC_KEY]
    ):
        self.test_dir = test_dir

        self.remote_host = remote_host
        self.remote_user = remote_user
        self.remote_pass = remote_pass

        self.remote_port = remote_port

        self.proj_dir = proj_dir
        self.outp_dir = outp_dir

        self.curr_proj_cls = curr_proj_cls
        self.curr_proj_sem = curr_proj_sem
        self.curr_proj_num = curr_proj_num
