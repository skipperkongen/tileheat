from datasource import CsvFileSource
from logplayer import *
from analysis import *

ds = CsvFileSource('../../../data/log2_2011_q4_rand_skrm.csv')

player = LogPlayer(ds)
player.add_analyzer( Echo() )
player.forward()

