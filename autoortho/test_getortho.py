#!/usr/bin/env python3

import gc
import os
import time
import pytest
import psutil
import getortho

from aostats import STATS

#getortho.ISPC = False

@pytest.fixture
def chunk():
    return getortho.Chunk(2176, 3232, 'EOX', 13)

def test_chunk_get(chunk):
    ret = chunk.get()
    assert ret == True
    
    print(STATS)
    assert True == False


def test_null_chunk():
    c = getortho.Chunk(2176, 3232, 'Null', 13)
    ret = c.get()
    assert ret

def test_chunk_getter():
    c = getortho.Chunk(2176, 3232, 'EOX', 13)
    getortho.chunk_getter.submit(c)
    ready = c.ready.wait(5)
    assert ready == True

@pytest.fixture
def tile(tmpdir):
    t = getortho.Tile(2176, 3232, 'EOX', 13, cache_dir=tmpdir)
    return t

def test_get_bytes(tmpdir):
    tile = getortho.Tile(2176, 3232, 'Null', 13, cache_dir=tmpdir)
    ret = tile.get_bytes(0, 131073)
    assert ret
    
    testfile = tile.write()
    with open(testfile, 'rb') as h:
        h.seek(128)
        data = h.read(8)

    assert data != b'\x00'*8
   

def test_get_bytes_mip1(tmpdir):
    tile = getortho.Tile(2176, 3232, 'Null', 13, cache_dir=tmpdir)
    #ret = tile.get_bytes(16777344, 4194304)
    ret = tile.get_bytes(16777344, 1024)
    assert ret
    
    testfile = tile.write()
    with open(testfile, 'rb') as h:
        h.seek(16777344)
        data = h.read(8)

    assert data != b'\x00'*8


def test_get_bytes_mip_end(tmpdir):
    tile = getortho.Tile(2176, 3232, 'Null', 13, cache_dir=tmpdir)
    #ret = tile.get_bytes(16777344, 4194304)
    ret = tile.get_bytes(20970000, 1024)
    assert ret
    
    testfile = tile.write()
    with open(testfile, 'rb') as h:
        #h.seek(20709504)
        h.seek(20971640)
        data = h.read(8)

    assert data != b'\x00'*8


def test_get_bytes_mip_span(tmpdir):
    tile = getortho.Tile(2176, 3232, 'Null', 13, cache_dir=tmpdir)
    #ret = tile.get_bytes(16777344, 4194304)
    ret = tile.get_bytes(20955264, 32768)
    assert ret
    
    testfile = tile.write()
    with open(testfile, 'rb') as h:
        #h.seek(20709504)

        h.seek(20955264)
        data0 = h.read(8)
        h.seek(20971648)
        data1 = h.read(8)

    assert data0 != b'\x00'*8
    assert data1 == b'\x00'*8


def test_get_bytes_row_span(tmpdir):
    tile = getortho.Tile(2176, 3232, 'Null', 13, cache_dir=tmpdir)
    #ret = tile.get_bytes(16777344, 4194304)
    ret = tile.get_bytes(17825792, 4096)
    assert ret
    
    testfile = tile.write()
    with open(testfile, 'rb') as h:
        h.seek(17825792)
        data = h.read(8)

    assert data != b'\x00'*8


def test_find_mipmap_pos():
    tile = getortho.Tile(2176, 3232, 'Null', 13)

    m = tile.find_mipmap_pos(129)
    assert m == 0

    m = tile.find_mipmap_pos(16777344)
    assert m == 1

    m = tile.find_mipmap_pos(20971650)
    assert m == 2


def test_read_bytes(tmpdir):
    tile = getortho.Tile(2176, 3232, 'Null', 13, cache_dir=tmpdir)
    data0 = tile.read_dds_bytes(0, 131073)
    assert data0[128:136] != b'\x00'*8
    data1 = tile.read_dds_bytes(131073,100000)
    assert data1[0:7] != b'\x00*8'
   
    print(len(data0))
    with open(f"{tmpdir}/readtest.dds", 'wb') as h:
        h.write(data0)
        #h.write(data1)

    testfile = tile.write()
    with open(testfile, 'rb') as h:
        h.seek(131073)
        filedata = h.read(8)

    assert data1[0:8] == filedata    


def test_get_mipmap(tmpdir):
    tile = getortho.Tile(2176, 3232, 'Null', 13, cache_dir=tmpdir)
    tile.min_zoom = 5
    ret = tile.get_mipmap(6)
    testfile = tile.write()
    assert ret

def test_get_mipmap_hash(tmpdir):
    #tile = getortho.Tile(27568, 17984, 'NAIP', 16, cache_dir=tmpdir)
    tile = getortho.Tile(2176, 3232, 'NAIP', 13, cache_dir=tmpdir)
    #27568_17984_NAIP16.jpg
    tile.min_zoom = 5
    ret = tile.get_mipmap(0)
    testfile = tile.write()
    assert ret
    assert True == False

def test_create_chunks(tmpdir):
    tile = getortho.Tile(2176, 3232, 'Null', 13, cache_dir=tmpdir)
    tile._create_chunks()
    print(tile.chunks)
    assert len(tile.chunks[13]) == 256

def test_get_bytes_all(tmpdir):
    tile = getortho.Tile(2176, 3232, 'Null', 13, cache_dir=tmpdir)
    ret = tile.get_bytes(0, 131072)
    #ret = tile.get()
    testfile = tile.write()
    assert ret

def test_get_header(tmpdir):
    tile = getortho.Tile(2176, 3232, 'Null', 13, cache_dir=tmpdir)
    ret = tile.get_header()
    assert ret

def _test_get_null_tile(tmpdir):
    tile = getortho.Tile(2176, 3232, 'Null', 13, cache_dir=tmpdir)
    ret = tile.get()
    assert ret

def test_tile_fetch(tmpdir):
    tile = getortho.Tile(2176, 3232, 'EOX', 13, cache_dir=tmpdir)
    ret = tile.fetch()
    assert ret == True
    assert len(tile.chunks[13]) == (tile.width * tile.height)
    #getortho.chunk_getter.stop() 
    #time.sleep(10)

def _test_tile_fetch_many(tmpdir):
    start_col = 2176
    start_row = 3232

    #for c in range(2176, 2432, 16):
    #    for r in range(3232, 3488, 16):
    for c in range(2176, 2200, 16):
        for r in range(3232, 3264, 16):
            t = getortho.Tile(c, r, 'BI', 13, cache_dir=tmpdir)
            t.get()
            #t.fetch()
            #print(len(t.chunks))

    #assert True == False


def _test_tile_quick_zoom(tmpdir):
    t = getortho.Tile(2176, 3232, 'EOX', 13, cache_dir=tmpdir)
    t.get(quick_zoom=10)
    t.get(quick_zoom=11)
    t.get(quick_zoom=12)
    t.get()
    #assert True == False

def _test_tile_get(tile):
    ret = tile.get()
    assert ret


def _test_tile_mem(tmpdir):
    process = psutil.Process(os.getpid())
    start_mem = process.memory_info().rss
    t = getortho.Tile(2176, 3232, 'EOX', 13, cache_dir=tmpdir)
    t.get_mipmap(0)
    time.sleep(2)
    mip0_mem = process.memory_info().rss
    print(f"{start_mem} {mip0_mem}  used:  {(mip0_mem - start_mem)/pow(2,20)} MB")
    assert True == False


def _test_tile_close(tmpdir):
    process = psutil.Process(os.getpid())
    start_mem = process.memory_info().rss
    t = getortho.Tile(2176, 3232, 'EOX', 13, cache_dir=tmpdir)
    t.get()
    get_mem = process.memory_info().rss
    t.close()
    del(t)
    gc.collect()
    time.sleep(5)
    close_mem = process.memory_info().rss
    print(f"S: {start_mem} G: {get_mem} C: {close_mem}.  Diff {close_mem-start_mem}")
    t = getortho.Tile(2176, 3232, 'EOX', 13, cache_dir=tmpdir)
    t.get()
    get_mem = process.memory_info().rss
    t.close()
    del(t)
    gc.collect()
    time.sleep(5)
    close_mem = process.memory_info().rss
    print(f"S: {start_mem} G: {get_mem} C: {close_mem}.  Diff {close_mem-start_mem}")

#def test_map(tmpdir):
#    m = getortho.Map(cache_dir=tmpdir)
#    ret = m.get_tiles(2176, 3232, 'EOX', 13)
#    assert ret

# def test_map_background(tmpdir):
#     m = getortho.Map(cache_dir=tmpdir)
#     start_c = 2176
#     start_r = 3232
#     num_c = 2
#     num_r = 1
#     for c in range(start_c, (start_c + num_c*16), 16):
#         for r in range(start_r, (start_r + num_r*16), 16):
#             ret = m.get_tiles(c, r, 'EOX', 13, background=True)
#     
#     for t in m.tiles:
#         print(f"Waiting on {t}")
#         ret = t.ready.wait(600)
#         assert ret == True
#         assert len(t.chunks[13]) == 256
# 
#     files = os.listdir(tmpdir)
#     assert len(m.tiles) == len(files)
