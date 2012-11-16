from ctypes import *

class Timespec(Structure):
    _fields_ = [('tm_sec', c_int),
                ('tm_min', c_int),
                ('tm_hour', c_int),
                ('tm_mday', c_int),
                ('tm_mon', c_int),
                ('tm_year', c_int),
                ('tm_wday', c_int),
                ('tm_yday', c_int),
                ('tm_isdst', c_int),
                ('tm_zone', c_char_p),
                ('tm_gmtoff', c_long)]
class Stat(Structure):
    _fields_ = [('st_dev', c_uint32),
                ('st_mode', c_uint16),
                ('st_nlink', c_uint16),
                ('st_ino', c_uint64),
                ('st_uid', c_uint32),
                ('st_gid', c_uint32),
                ('st_rdev', c_uint32),
                ('st_atimespec', Timespec),
                ('st_mtimespec', Timespec),
                ('st_ctimespec', Timespec),
                ('st_birthtimespec', Timespec),
                ('st_size', c_uint64),
                ('st_blocks', c_uint64),
                ('st_blksize', c_uint32),
                ('st_flags', c_uint32),
                ('st_gen', c_uint32),
                ('st_lspare', c_uint32),
                ('st_qspare0', c_uint64),
                ('st_qspare1', c_uint64)]
class FTSENT(Structure):
    _fields_ = [('fts_cycle', c_void_p),
                ('fts_parent', c_void_p),
                ('fts_link', c_void_p),
                ('fts_number', c_long),
                ('fts_pointer', c_void_p),
                ('fts_accpath', c_char_p),
                ('fts_path', c_char_p),
                ('fts_errno', c_int),
                ('fts_symfd', c_int),
                ('fts_pathlen', c_ushort),
                ('fts_namelen', c_ushort), # @66
                ('fts_ino', c_uint64), # @72
                ('fts_dev', c_uint32), # @80
                ('fts_nlink', c_uint16), #@84
                ('fts_level', c_short), #@86
                ('fts_info', c_ushort), #@88
                ('fts_flags', c_ushort), #@90
                ('fts_instr', c_ushort), #@92
                ('fts_statp', POINTER(Stat)), #@96
                ('fts_name', c_char*1)]

libc = CDLL('/usr/lib/libc.dylib', use_errno=True)

libc.fts_open.argtypes=[POINTER(c_char_p), c_int, c_void_p]
libc.fts_open.restype=c_void_p
libc.fts_close.argtypes=[c_void_p]
libc.fts_close.restype=c_int
libc.fts_read.argtypes=[c_void_p]
libc.fts_read.restype=POINTER(FTSENT)

FTS_COMFOLLOW = 0x001 #          /* follow command line symlinks */
FTS_LOGICAL   = 0x002 #          /* logical walk */
FTS_NOCHDIR   = 0x004 #          /* don't change directories */
FTS_NOSTAT    = 0x008 #          /* don't get stat info */
FTS_PHYSICAL  = 0x010 #          /* physical walk */
FTS_SEEDOT    = 0x020 #          /* return dot and dot-dot */
FTS_XDEV      = 0x040 #          /* don't cross devices */
FTS_WHITEOUT  = 0x080 #          /* return whiteout information */
FTS_COMFOLLOWDIR=0x400#          /* (non-std) follow command line symlinks for directories only */
FTS_OPTIONMASK= 0x4ff #          /* valid user option mask */

FTS_NAMEONLY =  0x100 #          /* (private) child names only */
FTS_STOP     =  0x200 #   

class fts(object):
    def __init__(self, path, flags=FTS_PHYSICAL):
        self.path=path
        a = ARRAY(c_char_p, 2)(path.encode('utf8'), None)
        self.fts = libc.fts_open(a, flags, None)
    def close(self):
        if self.fts:
            libc.fts_close(self.fts)
            self.fts = None
    def __del__(self):
        self.close()
    def __next__(self):
        e = libc.fts_read(self.fts)
        if not e:
            raise StopIteration
        return e.contents
    def next(self):
        return self.__next__()
    def __iter__(self):
        return self

def test():
    f = fts('.')
    for e in f:
        print(e.fts_path)
    f.close()
