import pygrf

class TestAct():

    def test_read_act_file(self):
        act = pygrf.open_act("bin/frus.act")
        assert len(act.animations) == 40
