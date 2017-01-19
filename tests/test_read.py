import os, sys; sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import fnmatch

import numpy
import pytest
import datetime

from lasio import read

test_dir = os.path.dirname(__file__)

egfn = lambda fn: os.path.join(os.path.dirname(__file__), "examples", fn)
stegfn = lambda vers, fn: os.path.join(
    os.path.dirname(__file__), "examples", vers, fn)

def test_read_v12_sample():
    l = read(stegfn("1.2", "sample.las"))


def test_read_v12_sample_big():
    l = read(stegfn("1.2", "sample_big.las"))


def test_read_v12_sample_curve_api():
    l = read(stegfn("1.2", "sample_curve_api.las"))


def test_read_v12_sample_minimal():
    l = read(stegfn("1.2", "sample_minimal.las"))


def test_read_v12_sample_wrapped():
    l = read(stegfn("1.2", "sample_wrapped.las"))


def test_read_v2_sample():
    l = read(stegfn("2.0", "sample_2.0.las"))


def test_read_v2_sample_based():
    l = read(stegfn("2.0", "sample_2.0_based.las"))


def test_read_v2_sample_minimal():
    l = read(stegfn("2.0", "sample_2.0_minimal.las"))


def test_read_v2_sample_wrapped():
    l = read(stegfn("2.0", "sample_2.0_wrapped.las"))

import lasio.reader
def test_parameter_pattern_with_format():
    d = lasio.reader.read_line(
        r"ROP5            .m/h                                       :(RT)    (DRILLING_SURFACE)                              Rate of penetration averaged over the last 5 ft (1.5 m){F13.4}")
    correct_d = {'valueformat': 'F13.4',
                 'value': None,
                 'name': 'ROP5',
                 'associations': '',
                 'descr': '(RT)    (DRILLING_SURFACE)                              Rate of penetration averaged over the last 5 ft (1.5 m)',
                 'unit': 'm/h'}
    assert d == correct_d, d

def test_parameter_pattern_with_datestring():
    d = lasio.reader.read_line(
        r"DATE            .                    01/22/2016            :LOG DATE(Composite Date for Composite LAP) {MM/DD/YYYY}")
    assert d == \
           {'associations': '',
            'value': datetime.datetime(2016, 1, 22, 0, 0),
            'descr': 'LOG DATE(Composite Date for Composite LAP)',
            'unit': '',
            'name': 'DATE',
            'valueformat': 'MM/DD/YYYY'}, d

def test_parameter_with_unit():
    ''' The line in this test case is not conforming to the standard
    '''
    d = lasio.reader.read_line(
        r"HKLA            .1000 kgf                                  :(RT)    (DRILLING_SURFACE)                              Average Hookload{F13.4}")
    print(d)
    assert False, "Not implemented"

def test_value_parsing():
    v = lasio.reader.parse_value("01/10/2016","MM/DD/YYYY")
    assert v == datetime.datetime(2016,1,10), '"01/10/2016","MM/DD/YYYY" parsed as %s' % v
    v = lasio.reader.parse_value("01/10/2016","DD/MM/YYYY")
    assert v == datetime.datetime(2016,10,1), '"01/10/2016","DD/MM/YYYY" parsed as %s' % v
    v = lasio.reader.parse_value("DEC-3-2017","MMM-DD-YYYY")
    assert v == datetime.datetime(2017,12,3)


def test_read_v3_sample():
    l = read(stegfn("3.0", "sample_3.0.las"))


def test_read_v3_sample2():
    l = read(stegfn("3.0", "memory_data_shortened_3.0.las"))

def test_read_v3_sample2_depthdtype():
    l = read(stegfn("3.0", "memory_data_shortened_3.0.las"))
    assert l["DEPTH"].dtype is numpy.dtype('float'), "Depth dtype should be float, was %s" % l["DEPTH"].dtype

def test_read_v3_sample2_timedtype():
    l = read(stegfn("3.0", "memory_data_shortened_3.0.las"))
    assert l["TIME"].dtype == numpy.dtype('datetime64[ns]'), "Time dtype should be datetime64[ns], was %s" % l["TIME"].dtype

def test_read_v3_pandas_column():
    l = read(stegfn("3.0", "memory_data_shortened_3.0.las"))
    col = l["DEPTH"]
    assert col.size >= 3

def test_read_v3_sample_spec():
    l = read(stegfn("3.0", "sample_las3.0_spec.las"))


def test_dodgy_param_sect():
    l = read(egfn("dodgy_param_sect.las"))


def test_mnemonic_good():
    l = read(egfn("mnemonic_good.las"))
    assert [c.mnemonic for c in l.curves] == [
        "DEPT", "DT", "RHOB", "NPHI", "SFLU", "SFLA", "ILM", "ILD"]


def test_mnemonic_duplicate():
    l = read(egfn("mnemonic_duplicate.las"))
    assert [c.mnemonic for c in l.curves] == [
        "DEPT", "DT", "RHOB", "NPHI", "SFLU:1", "SFLU:2", "ILM", "ILD"]


def test_mnemonic_leading_period():
    l = read(egfn("mnemonic_leading_period.las"))
    assert [c.mnemonic for c in l.curves] == [
        "DEPT", "DT", "RHOB", "NPHI", "SFLU", "SFLA", "ILM", "ILD"]

def test_mnemonic_missing():
    l = read(egfn("mnemonic_missing.las"))
    assert [c.mnemonic for c in l.curves] == [
        "DEPT", "DT", "RHOB", "NPHI", "UNKNOWN", "SFLA", "ILM", "ILD"]

def test_mnemonic_missing_multiple():
    l = read(egfn("mnemonic_missing_multiple.las"))
    assert [c.mnemonic for c in l.curves] == [
        "DEPT", "DT", "RHOB", "NPHI", "UNKNOWN:1", "UNKNOWN:2", "ILM", "ILD"]

def test_null_subs_default():
    l = read(egfn("null_subs.las"))
    assert numpy.isnan(l['DT'][0])

def test_null_subs_True():
    l = read(egfn("null_subs.las"), null_subs=True)
    assert numpy.isnan(l['DT'][0])

def test_null_subs_False():
    l = read(egfn("null_subs.las"), null_subs=False)
    assert l['DT'][0] == -999.25

def test_multi_curve_mnemonics():
    l = read(egfn('sample_issue105_a.las'))
    assert l.keys() == [c.mnemonic for c in l.curves] == ['DEPT', 'RHO:1', 'RHO:2', 'RHO:3', 'PHI']


def test_multi_missing_curve_mnemonics():
    l = read(egfn('sample_issue105_b.las'))
    assert l.keys() == [c.mnemonic for c in l.curves] == ['DEPT', 'UNKNOWN:1', 'UNKNOWN:2', 'UNKNOWN:3', 'PHI']


def test_multi_curve_mnemonics_gr():
    l = read(egfn('sample_issue105_c.las'))
    assert l.keys() == [c.mnemonic for c in l.curves] == ['DEPT', 'GR:1', 'GR:2', 'GR[0]', 'GR[1]', 'GR[2]', 'GR[3]', 'GR[4]', 'GR[5]']

#  DEPT.M                      :  1  DEPTH
# GR.gAPI: mean gamma ray value
# GR.gAPI: corrected gamma ray value
# GR[0].gAPI: gamma ray image at angle 0 dega
# GR[1].gAPI: gamma ray image at angle 60 dega
# GR[2].gAPI: gamma ray image at angle 120 dega
# GR[3].gAPI: gamma ray image at angle 180 dega
# GR[4].gAPI: gamma ray image at angle 240 dega
# GR[5].gAPI: gamma ray image at angle 300 dega

def test_inf_uwi():
    l = read(stegfn('2.0', 'sample_2.0_inf_uwi.las'))
    assert l.well['UWI'].value == '300E074350061450'

