"""

Binary Signal Read Class

**User-API Interfaces**

  - `SignalReader` (signal file class)
  - `SignalReaderException`

"""

# __all__ = ['SignalReader', 'SignalReaderException']

# - import Python modules ---------------------------------------------------------------------------------------------
from numpy import inf, array
from os import path as opath, SEEK_END, SEEK_CUR
from struct import unpack
from zlib import decompress
from csv import Error, reader
from re import match
from sys import _getframe

# - import STK modules ------------------------------------------------------------------------------------------------
# from error import StkError
# from helper import deprecation

ERR_OK = 0
"""Code for No Error"""
ERR_UNSPECIFIED = 1
"""Code for an unknown Error"""

# - defines -----------------------------------------------------------------------------------------------------------
SIG_NAME = 'SignalName'
SIG_TYPE = 'SignalType'
SIG_ARRAYLEN = 'ArrayLength'
SIG_OFFSET = 'Offsets'
SIG_SAMPLES = 'SampleCount'


# - classes -----------------------------------------------------------------------------------------------------------

class StkError(Exception):
    """
    **Base STK exception class**,

    where all other Exceptions from the stk sub-packages must be derived from.

    Frame number is set to 2 thereof.

    - Code for No Error: ERR_OK
    - Code for an unknown / unspecified Error: ERR_UNSPECIFIED
    """

    ERR_OK = ERR_OK
    """Code for No Error"""
    ERR_UNSPECIFIED = ERR_UNSPECIFIED
    """Code for an unknown Error"""

    def __init__(self, msg, errno=ERR_UNSPECIFIED, dpth=2):
        """
        retrieve some additional information

        :param msg:   message to announce
        :type msg:    str
        :param errno: related error number
        :type errno:  int
        :param dpth:  starting frame depth for error trace, increase by 1 for each subclass level of StkError
        :type dpth:   int
        """
        Exception.__init__(self, msg)
        frame = _getframe(dpth)
        self._errno = errno
        self._error = "'%s' (%d): %s (line %d) attr: %s" \
                      % (msg, errno, opath.basename(frame.f_code.co_filename), frame.f_lineno, frame.f_code.co_name)

    def __str__(self):
        """
        :return: our own string representation
        :rtype: str
        """
        return self._error

    @property
    def error(self):
        """
        :return: error number of exception
        :rtype: int
        """
        return self._errno


class SignalReaderException(StkError):
    """general exception for SignalReader class"""
    def __init__(self, msg):
        """derived from std error"""
        delim = "=" * (len(msg) + 7) + "\n"
        StkError.__init__(self, "\n%sERROR: %s\n%s" % (delim, msg, delim))


class CsvReader(object):  # pylint: disable=R0924,R0902
    """
    **Delimited reader class**

    internal class used by SignalReader in case of reading csv type files

    use class `SignalReader` to read csv files
    """
    def __init__(self, filepath, **kwargs):
        """open / init cvs file
        """
        self._signal_names = []
        self._signal_values = {}
        self._signal_type = {}

        self._all_types = {long: 0, float: 1, str: 2}

        self._delimiter = kwargs.pop('delim', ';')
        if self._delimiter not in (';', ',', '\t', ' '):
            self._delimiter = ';'

        self._skip_lines = kwargs.pop('skip_lines', 0)
        self._skip_data_lines = kwargs.pop('skip_data_lines', 0)
        self._scan_type = kwargs.pop('scan_type', 'no_prefetch').lower()
        if self._scan_type not in ('prefetch', 'no_prefetch'):
            self._scan_type = 'prefetch'
        self._scan_opt = kwargs.pop('scan_opt', 'scan_auto').lower()
        if self._scan_opt not in ('scan_auto', 'scan_raw'):
            # self._scan_opt = self._match_type(self._scan_opt)
            if self._scan_opt == 'long':
                self._scan_opt = type(long(0))
            elif self._scan_opt == 'float':
                self._scan_opt = type(float(0.0))

        # for opt in kwargs:
        #     deprecation('unused SignalReader option: ' + opt)

        self._selfopen = None

        if not hasattr(filepath, 'read'):
            self._fp = open(filepath, "r")
            self._selfopen = True
            self._file_path = filepath
        else:
            self._fp = filepath
            self._selfopen = False
            self._file_path = filepath.name

        # read file header
        try:
            self._csv = reader(self._fp, delimiter=self._delimiter)
            for _ in xrange(self._skip_lines):
                self._csv.next()

            # get all signals name
            self._signal_names = self._csv.next()

            if self._signal_names.count('') > 0:
                self._signal_names.remove('')
            for idx in xrange(len(self._signal_names)):
                self._signal_names[idx] = self._signal_names[idx].strip()
                self._signal_values[idx] = []

            if self._scan_type == 'prefetch':
                self._read_signals_values()
        except:
            self.close()
            raise

    def close(self):
        """close the file
        """
        if self._fp is not None:
            if self._selfopen:
                self._fp.close()
            self._fp = None

            self._signal_names = None
            self._signal_values = None

    def __len__(self):
        """Function returns the number of signals in the binary file.

        :return: The number of signals in the binary file.
        """
        return len(self._signal_names)

    def __str__(self):
        """returns file info"""
        return "<dlm: '%s', signals: %d>" % (self._fp.name, len(self))

    def siglen(self, _):
        """provides length of a signal, as csv's are of same length we do it the easy way

        :param: signal name (to be compatible to SignalReader method, not used here)
        :return: length of signal in file
        :rtype:  int
        """
        if len(self._signal_values[0]) == 0:
            self._read_signals_values(self._signal_names[0])
        return len(self._signal_values[0])

    @property
    def signal_names(self):
        """returns names of all signals

        :return: all signal names in file
        :rtype:  list
        """
        return self._signal_names

    def signal(self, signal, offset=0, count=0):
        """returns the values of a signal given as input.

        When signal_name doesn't exist it returns 'None'

        :param signal: the name of the signal
        :param offset: signal offset to start
        :param count: number of signal items to return
        :return: value of named signal or None
        """
        if type(signal) in (tuple, list):
            return [self.signal(s) for s in signal]

        self._read_signals_values(self._signal_names[signal] if type(signal) == int else signal)

        if type(signal) == str:
            signal = self._signal_names.index(signal)

        # todo: maybe we should convert already when reading...
        try:
            vals = array(self._signal_values[signal], dtype=[tt for tt, it in self._all_types.items()
                                                             if it == self._signal_type[signal]][0])
        except KeyError:
            vals = array(self._signal_values[signal], dtype=float)

        if offset + count == 0:
            return vals
        else:
            return vals[offset:offset + count]

    def _read_signals_values(self, signals_list=None):  # pylint: disable=R0912,R0915
        """
        Reads signal values from a simulation file - csv format.
        This function reads a list of signal given as input.
        When signals_list is 'None' all signal will be read

        :param signals_list:   the list of the signals
        :return: dictionary with extracted signals, empty {} in case of errors
        """
        if signals_list is None:
            signals_list = self._signal_names

        if type(signals_list) == str:
            signals_list = [signals_list]

        # prevent loading already loaded ones
        removes = [sig for sig in signals_list if len(self._signal_values[self._signal_names.index(sig)]) > 0]
        for rem in removes:
            signals_list.remove(rem)

        if len(signals_list) == 0:
            return

        for signal in signals_list:
            if signal not in self._signal_type:
                if self._scan_opt == 'scan_raw':
                    self._signal_type[self._signal_names.index(signal)] = 2
                else:
                    self._signal_type[self._signal_names.index(signal)] = 0

        self._fp.seek(0)
        # if skip_lines constructor parameter is not specified
        for _ in xrange(self._skip_lines + 1 + self._skip_data_lines):
            self._csv.next()

        if self._scan_opt == 'scan_raw':
            try:
                for row in self._csv:
                    for signal in signals_list:
                        try:
                            idx = self._signal_names.index(signal)
                            self._signal_values[idx].append(str(row[idx]))
                        except IndexError:
                            pass
                    # del row
            except Error as ex:
                raise SignalReaderException('file %s, line %d: %s' % (self._file_path, self._csv.line_num, ex))

        elif self._scan_opt == 'scan_auto':
            try:
                for row in self._csv:
                    for signal in signals_list:
                        idx = self._signal_names.index(signal)
                        try:
                            if match(r"^(\d+)$", row[idx].lstrip()) is not None:
                                val = long(row[idx])
                            elif(match(r"[-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?\s*\Z",
                                       row[idx].lstrip()) is not None):
                                val = float(row[idx])
                            else:
                                val = str(row[idx])

                            if type(val) == str:
                                if match(r"[+]?1(\.)[#][Ii][Nn]", val.lstrip()) is not None:
                                    val = inf
                                elif match(r"-1(\.)[#][Ii][Nn]", val.lstrip()) is not None:
                                    val = -inf
                            self._signal_values[idx].append(val)
                            self._signal_type[idx] = max(self._all_types[type(val)], self._signal_type[idx])
                        except:
                            self._signal_type[idx] = type(float)
                    # del row
            except Error as ex:
                raise SignalReaderException('file %s, line %d: %s' % (self._file_path, self._csv.line_num, ex))
        else:
            try:
                for row in self._csv:
                    for signal in signals_list:
                        idx = self._signal_names.index(signal)
                        self._signal_values[idx].append(self._scan_opt(row[idx]))
            except Error as ex:
                raise SignalReaderException('file %s, line %d: %s' % (self._file_path, self._csv.line_num, ex))


class BsigReader(object):  # pylint: disable=R0902,R0924
    """bsig reader class

    internal class used by SignalReader to read binary signal files (type bsig2 and bsig3)

    use class `SignalReader` to read files
    """
    def __init__(self, fp, **kw):  # pylint: disable=R0912,R0915
        """set default values

        :param fp: file to use, can be a file pointer to an already open file or a name of file
        :keyword use_numpy: use numpy for signal values, default: True
        """
        self._arr_frmt = {0x0008: 'B', 0x8008: 'b', 0x0010: 'H', 0x8010: 'h', 0x0020: 'L', 0x8020: 'l', 0x0040: 'Q',
                          0x8040: 'q', 0x9010: 'f', 0x9020: 'd'}
        self._sig_frmt = {'c': 1, 'b': 1, 'B': 1, 'h': 2, 'H': 2, 'I': 4, 'l': 4, 'L': 4, 'q': 8, 'Q': 8,
                          'f': 4, 'd': 8}
        file_header = 24

        self._fp = fp
        self._npusage = kw.pop('use_numpy', True)
        self._name_sense = kw.pop('sensitive', True)
        self._selfopen = None

        try:
            if hasattr(self._fp, 'read'):
                self._fp.seek(0)
                self._selfopen = False
            else:
                # noinspection PyTypeChecker
                self._fp = open(self._fp, "rb")
                self._selfopen = True

            # read global header
            if self._read_sig('c' * 4) != ('B', 'S', 'I', 'G'):
                raise SignalReaderException("given file is not of type BSIG!")
            version = self._read_sig('B' * 3)
            if version[0] not in (2, 3):  # we support version 2 and 3 by now
                raise SignalReaderException("unsupported version: %d.%d.%d, supporting only V2 & V3!" % version)
            self._version = version[0]
            self._signal_data = []
            self._offstype = 'I' if self._version == 2 else 'Q'

            # get total size of file
            self._fp.seek(0, SEEK_END)
            self._file_size = self._fp.tell()
            self._fp.seek(-file_header, SEEK_CUR)

            # read file header
            signal_count, self._block_size, self._hdr_size, offset_size = self._read_sig('IIII')
            self._read_sig('B' * 3)  # internal version is unused, read over
            self._compression = self._read_sig('B')[0] == 1
            if self._read_sig('c' * 4) != ('B', 'I', 'N', '\x00'):  # bin signature
                raise SignalReaderException("BSIG signature wrong!")

            # read signal description
            self._fp.seek(self._file_size - file_header - self._hdr_size)  # = self._hdr_offset
            for _ in xrange(signal_count):
                sig_name_len = self._read_sig('H')[0]
                signal_name = "".join(self._read_sig('c' * sig_name_len))
                array_len, stype = self._read_sig('II')
                self._signal_data.append({SIG_NAME: signal_name, SIG_TYPE: stype, SIG_ARRAYLEN: array_len})

            # read offsets data
            self._fp.seek(self._file_size - file_header - self._hdr_size - offset_size)
            for sig in self._signal_data:
                offset_count, sig[SIG_SAMPLES] = self._read_sig('II')
                sig[SIG_OFFSET] = self._read_sig(self._offstype * offset_count)
        except SignalReaderException:
            self.close()
            raise
        except:
            self.close()
            raise SignalReaderException("Error while reading signal information, corruption of data?")

    def close(self):
        """close signal file
        """
        if self._fp is not None:
            try:
                if self._selfopen:
                    self._fp.close()
                self._fp = None

                self._signal_data = None
            except:
                raise SignalReaderException("An error occurred while closing the file.")

    def __len__(self):
        """Function returns the number of signals in the binary file.

        :return: number of signals in the binary file.
        """
        return len(self._signal_data)

    def __str__(self):
        """returns file info"""
        return "<bsig%d: '%s', signals: %d>" % (self._version, self._fp.name, len(self))

    def siglen(self, signal):
        """provides length of a signal, as csv's are of same length we do it the easy way

        :param signal: name of signal
        :return: length of signal
        :rtype:  int
        """
        if signal is None:
            return self._signal_data[0][SIG_SAMPLES]

        if self._name_sense:
            sigdet = next((s for s in self._signal_data if s[SIG_NAME] == signal), None)
        else:
            sigdet = next((s for s in self._signal_data if s[SIG_NAME].lower() == signal.lower()), None)
        if sigdet is None:
            raise SignalReaderException("no signal by that name found: %s" % str(signal))

        return sigdet[SIG_SAMPLES]

    def signal(self, signal, offset=None, count=None):  # pylint: disable=R0912
        """Function returns the data for the signal with the specified index.

        :param signal: index / name of signal or list of the signals
        :param offset: data offset of signal
        :param count: length of data
        :return: signal data as an array (default) or list as defined during reader initialisation
        :rtype: array or list
        """
        # check for input argument validity
        if type(signal) in (tuple, list):
            return [self.signal(s) for s in signal]
        elif type(signal) == int and 0 <= signal < len(self._signal_data):
            sigdet = self._signal_data[signal]
        else:
            if self._name_sense:
                sigdet = next((s for s in self._signal_data if s[SIG_NAME] == signal), None)
            else:
                sigdet = next((s for s in self._signal_data if s[SIG_NAME].lower() == signal.lower()), None)
            if sigdet is None:
                # raise SignalReaderException("signal not found: %s" % signal)
                print "signal not found: %s" % signal
                return []

        # align offset and count, count is initially the length, but we use it as stop point and offset as start point
        if offset is None:
            offset = 0
        elif offset < 0:
            offset = sigdet[SIG_SAMPLES] + offset
        if count is None:
            count = sigdet[SIG_SAMPLES]
        elif count < 0 or offset + count > sigdet[SIG_SAMPLES]:
            raise SignalReaderException("offset / count for signal %s is out of range: %s / %s" %
                                        (signal, str(offset), str(count)))
        else:
            count += offset

        frmt = self._arr_frmt[sigdet[SIG_TYPE]]  # data format
        dlen = self._sig_frmt[frmt]  # length of one data point
        blkl = self._block_size / dlen  # real block length
        alen = sigdet[SIG_ARRAYLEN]  # array length of signal
        sig = []  # extracted signal

        # increment with array length
        offset *= alen
        count *= alen

        # precalc reduced offsets
        sigoffs = list(sigdet[SIG_OFFSET])
        while count < (len(sigoffs) - 1) * blkl:  # cut last offsets
            sigoffs.pop(len(sigoffs) - 1)

        while offset >= blkl:  # cut first offsets
            sigoffs.pop(0)
            offset -= blkl  # reduce starting point
            count -= blkl  # reduce stop point

        # without compression we could even cut down more reading,
        # but I'll leave it for now as it makes more if then else

        # read data blocks
        for offs in sigoffs:
            self._fp.seek(offs)
            if self._compression:
                data = self._fp.read(self._read_sig('I')[0])
                data = decompress(data)
            else:
                data = self._fp.read(self._block_size)

            data = unpack(frmt * (len(data) / dlen), data)
            sig.extend(data)

        if self._npusage:
            if alen == 1:
                return array(sig[offset:count], dtype=frmt)
            return array(sig[offset:count], dtype=frmt).reshape(((count - offset) / alen, alen))
        else:
            if alen == 1:
                return sig[offset:count]
            return [sig[i:i + alen] for i in xrange(offset, count, alen)]

    @property
    def signal_names(self):
        """returns names of all signals with the specified index.

        :return: all signal names in file
        :rtype:  list
        """
        return [sig[SIG_NAME] for sig in self._signal_data]

    def _read_sig(self, stype):
        """read signal of given type
        """
        try:
            return unpack(stype, self._fp.read(self._sig_frmt[stype[0]] * len(stype)))
        except:
            raise SignalReaderException("An error occured while reading binary data.")


class SignalReader(object):
    """
    **MAIN Class for Signal File Read.** (\\*.bsig (aka \\*.bin), \\*.csv)

    open, step through, read signals and close a signal file, provide list of signal names

    by default the **values are returned as numpy array**, see `__init__` how to configure for python lists

    for csv files several options (like delimiter) are supported, see `__init__` for more details

    even if the usage looks like calling a dict *a SignalReader instance is no dict:*

    - when getting a signal using ``sr['my_signal_name']`` just that signal is read from the file;
    - adding or deleting signals is not possible, it's just a reader;
    - there are no dict functions like d.keys(), d.values(), d.get() etc.

    supported functions (see also Examples below):

    -with              open and integrated close for a signal file
    -get               values of signal with name or index: ``sr['my_name'], sr[2]``
    -len               number of signals: ``len(sr)``
    -in                check if signal with name is available: ``if 'my_sig' in sr:``
    -for               loop over all signals with name and values: ``for n, v in sr:``
    -signal_names      list of all signal names (like dict.keys()): ``sr.signal_names``

    usage (example)
    ---------------

    .. python::
        # read csv files:
        reader = SignalReader(<file.csv>,
                              'delim'=<delimiter>,
                              'scan_type'=<'prefetch','no_prefetch'>,
                              'scan_opt'=<'scan_auto','scan_raw','float',...>,
                              'skip_lines'=<number_of_header_lines_to_skip>,
                              'skip_data_lines'=<number_of_data_lines_to_skip>)
        # read bsig files (version 2 or 3)
        reader = SignalReader(<file.bsig>)

        # check if signal with name is stored in file:
        if "MTS.Package.TimeStamp" not in reader:
            print("TimeStamp missing in signal file")

    Examples:

    .. python::
        import numpy as np
        from stk.io.signalreader import SignalReader, SignalReaderException

        # EXAMPLE 1
        sr = SignalReader('file_hla_xyz.txt', delim ='\t', scan_type='NO_PREFETCH')
        # get values
        read_values = sr['lux_R2G']
        sr.close()

        # EXAMPLE 2
        sr = SignalReader('file_sla_xyz.csv',delim =',',skip_lines=8)
        # read only signal 'timestamp'
        values = sr['timestamp'] # gets the timestamp signal
        values = sr[0] # gets the signal by index 0
        sr.close()

        # EXAMPLE 3
        with SignalReader('file_hla_xyz.bsig') as sr:
            signals = sr[['Time stamp','Cycle counter']] # retrieves a list of both signals --> [[<sig1>], [<sig2>]]

        # EXAMPLE 4
        with SignalReader('file_hla_xyz.bsig') as sr:
            signals = sr['Time stamp':50:250] # retrieves 200 samples of time stamp signal from offset 50 onwards

        # EXAMPLE 5
        with SignalReader('file_fct.bsig') as sr:
            for n, v in sr:  # iterate over names and signals
                print("%s: %d" % (n, v.size))

        with SignalReader('file_hla_xyz.bsig') as sr:
            signals = sr['Time stamp':50:250] # retrieves 200 samples of time stamp signal from offset 50 onwards

        # EXAMPLE 6
        instance_ARS = SignalReader('file_ars_xyz.csv', delim =';',scan_opt = 'float')
        ...
        instance_ARS.close()


        import numpy as np
        from stk.io.signalreader import SignalReader, SignalReaderException

        # EXAMPLE 1
        sr = SignalReader('file_hla_xyz.txt', delim ='\t', scan_type='NO_PREFETCH')
        # get values
        read_values = sr['lux_R2G']
        sr.close()

        # EXAMPLE 2
        sr = SignalReader('file_sla_xyz.csv',delim =',',skip_lines=8)
        # read only signal 'timestamp'
        values = sr['timestamp'] # gets the timestamp signal
        values = sr[0] # gets the signal by index 0
        sr.close()

        # EXAMPLE 3
        with SignalReader('file_hla_xyz.bsig') as sr:
            signals = sr[['Time stamp','Cycle counter']] # retrieves a list of both signals --> [[<sig1>], [<sig2>]]

        # EXAMPLE 4
        with SignalReader('file_hla_xyz.bsig') as sr:
            signals = sr['Time stamp':50:250] # retrieves 200 samples of time stamp signal from offset 50 onwards

        # EXAMPLE 5
        instance_ARS = SignalReader('file_ars_xyz.csv', delim =';',scan_opt = 'float')
        ...
        instance_ARS.close()

    """

    def __init__(self, filename, **kw):
        """open the binary file by its name, supported formats: bsig 2, 3, csv

        :param filename: path/to/file.name

        *following parameter can be used when intending to open e.g. a bsig file:*

        :keyword use_numpy: boolean value that indicates wether using numpy arrays for signal values, default: True
        :keyword sensitive: boolean value that indicates wether to treat signal names case sensitive, default: True

        *following parameter can be used when intending to open e.g. a csv file:*

        :keyword delim: delimiter char for columns
        :keyword scan_type: can be 'no_prefetch' or 'prefetch' to read in data at init
        :keyword scan_opt: 'can be 'scan_auto', 'scan_raw' or e.g. 'float', 'long' or 'str'
        :keyword scip_lines: how many lines should be scripped / ignored reading in at start of file
        :keyword scip_data_lines: how many lines of data should be scripped reading in at start
        :keyword type: type of file can set explicitly, set to 'bsig' will force it to be a bsig
        """
        self._fp = filename

        if opath.splitext(self._fp.name if hasattr(self._fp, 'read')
                          else filename)[1].lower() in ('.bsig', '.bin', '.tstp') or kw.pop('type', None) == 'bsig':
            self._reader = BsigReader(self._fp, **kw)
            self._type = "bsig"
        else:
            self._reader = CsvReader(self._fp, **kw)
            self._type = "dlm"

        self._signal_names = self._reader.signal_names
        self._iter_idx = 0

    def __enter__(self):
        """being able to use with statement"""
        return self

    def __exit__(self, *_):
        """close down file"""
        self.close()

    def close(self):
        """close file"""
        self._reader.close()

    def __str__(self):
        """returns the type and number of signals"""
        return str(self._reader)

    def __len__(self):
        """return number of signals from reader"""
        return len(self._reader)

    def signal_length(self, signal=None):
        """length of a signal

        :param signal: name of signal length should be returned
        :return: signal length
        :rtype: int
        """
        return self._reader.siglen(signal)

    def __iter__(self):
        """start iterating through signals"""
        self._iter_idx = 0
        return self

    def next(self):
        """next signal item to catch and return"""
        if self._iter_idx >= len(self._signal_names):
            raise StopIteration
        else:
            self._iter_idx += 1
            return self._signal_names[self._iter_idx - 1], self[self._iter_idx - 1]

    def __contains__(self, name):
        """checks if signal name is stored in SignalReader

        :param name: signal name to check
        :return: bool
        """
        return name in self._signal_names

    def __getitem__(self, signal):
        """provide signal by name or index,

        if index is a slice use start as index,
        stop as offset and step as count

        :param signal: signal name or index or sliced index
        :type  signal: str, int, tuple/list
        :return:  signal with type as defined in reader initiation
        :rtype:   array or list
        """
        # [Offset:Offset + SampleCount]
        try:
            if type(signal) in (int, str):
                return self._reader.signal(signal)
            elif type(signal) in (tuple, list):
                if set(signal).issubset(self._signal_names):
                    return self._reader.signal(signal)
                else:
                    return self._reader.signal(signal[0], signal[1], signal[2])
            elif type(signal) == slice:  # not nice, but no other strange construct needed
                return self._reader.signal(signal.start, signal.stop, signal.step)
            else:
                raise IndexError
        except (IndexError, SignalReaderException):
            raise
        except:
            raise SignalReaderException("Data corruption inside signal file, unable to read signal '{}'!"
                                        .format(signal))

    @property
    def signal_names(self):
        """list of all signal names

        :return: all signal names in file
        :rtype:  list
        """
        return self._signal_names
