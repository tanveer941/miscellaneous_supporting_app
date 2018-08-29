"""
signal_loader.py
----------------

Used to load and convert signals or block of signals.
Arguments to class initialization look like this::

  vdy={'prefix': 'SIM VFB ALL.DataProcCycle.ObjSyncEgoDynamic',
       'signals': [{'name': '.Lateral.Curve.Curve', 'port': 'Curve'},
                   {'name': '.Longitudinal.MotVar.Velocity', 'port': 'VehicleSpeed'},
                   {'name': '.Longitudinal.MotVar.Accel', 'port': 'VehicleAccelXObjSync'},
                   {'name': '.Lateral.YawRate.YawRate', 'port': 'VehicleYawRateObjSync'}
                  ]
      }

whereas prefix will prepend all names from list of signals (default: ''),
and `conv` is intended to be the conversation function.
This function is called with list of extracted signals, default function passes through all signals
and returns them.
Once you use `$` marker inside first signalname, all signals are treated like a block. Iteration will
then go along all found indices found. If you want to use less, you need to keep track outside, e.g.
with your own counter.

**example 1**
-------------

read out simple list of signals::

  sl = SignalLoader(r'D:\tmp\Continuous_2015.04.22_at_12.15.53.bsig',
                    fixed={'prefix': 'MTS.Package.',
                           'signals': ['TimeStamp', 'CycleCount'],
                           'conv': lambda s: s},  # default
                    ars={'signals': ['ARS4xx Device.AlgoVehCycle.VehDyn.Longitudinal.MotVar.Velocity',
                                     'MTS.Package.TimeStamp']})
  for i in sl('fixed'):
      print(i)

  print("do we have 'var': %s" % ('var' in sl))  # prints: .... False as only `fixed` and `ars` was defined

**example 2**
-------------

block readout::

  def sum_up(sigs):
      res = sigs[0]
      for i in xrange(1, len(sigs)):
          res += sigs[i]
      return res

  sl = SignalLoader(r'D:\tmp\Snapshot_2014.10.15_at_19.40.34.bsig',
                    fct={'prefix': 'SIM VFB.FCTSensor.',
                         'signals': ['CDInternalObjInfo.Obj[$].TTC',
                                     'CDInternalObjInfo.Obj[$].TTC2',
                                     'CDInternalObjInfo.Obj[$].TTC3'],
                         'conv': sum_up})

    cnt = 0
    for sig in sl('fct'):
        print("%d: %s" % (cnt, sig))
        if cnt >= 2:  # just stop reading / converting as we only need 2 of those blocks
            break
        cnt += 1


"""
# - STK imports -------------------------------------------------------------------------------------------------------
from signalreader import SignalReader

# - defines -----------------------------------------------------------------------------------------------------------
PREFIX = "prefix"
SIGNALS = "signals"
CONV = "conv"
ITER = "iter"
IARGS = "iargs"


# - classes -----------------------------------------------------------------------------------------------------------
class SignalLoader(object):
    """loads signals / objects from given binary file (bsig)
    """
    def __init__(self, bsig, **kwargs):
        """loader / converter for signals out of a bsig / csv (SignalReader class is used).
        be aware that putting down block size to 4kb inside MTS signal exporter could speed up SignalReader...

        :param bsig: path / to / bsig or csv file
        :type bsig: file | str
        :param kwargs: list of arguments described here, all others are saved to xargs

        :keyword prefix: signal prefix name to be prepended to all signal names
        :type prefix: str
        :keyword signals: list of signal names
        :type signals: list[str]
        :keyword conv: conversation function taking one argument being the signal (numpy array)
        """
        self._bsig = SignalReader(bsig)

        self._idx = 0
        self._imx = 0
        self._obj_mode = False
        self._idem = None

        self._args = kwargs
        for arg, val in self._args.iteritems():
            if CONV not in val:
                val[CONV] = lambda s: s
            # will be called when iterator inits with self, returning if going via block mode and iter amount
            if ITER not in val:
                val[ITER] = {'func': self._dummy_iter, 'args': None}

            pref = val.get(PREFIX, '')
            # for sig in val[SIGNALS]:
            #     print ">> ", sig
            #     if sig['name'].startswith('.'):
            #         sig['name'] = pref + sig['name']

    def __enter__(self):
        """with statement usage start"""
        return self

    def _dummy_iter(self, *_):
        """dummy iterator init, used by default to just load single signals
        """
        return False, len(self._idem[SIGNALS])

    def __len__(self):
        """get length of objects / signals"""
        if self._imx == 0:
            try:
                self._obj_mode, self._imx = self._idem[ITER]['func'](self, self._idem[ITER]['args'])
            except:
                self._obj_mode, self._imx = False, 0

        return self._imx

    def __iter__(self):
        """start iterating through signal processing"""
        self._idx, self._imx = 0, 0
        len(self)
        return self

    def next(self):
        """next item to catch and return"""
        if self._idem is None or self._idx >= self._imx:
            raise StopIteration

        if self._obj_mode:
            obj = self._idem[CONV](self._idx, self._idem[SIGNALS])
        else:
            print "{{{{ ", self._idem[CONV](self._bsig[self._idem[SIGNALS][self._idx]])
            obj = self._idem[CONV](self._bsig[self._idem[SIGNALS][self._idx]])
            # obj = self._idem[CONV](self._bsig[self._idem[SIGNALS][self._idx]['name']])
        self._idx += 1

        return obj

    def __call__(self, item):
        """making a lookalike function call, to take over item of what we want to iterate through actually,
        the iterator for itself is quiet useless as no args can be given.

        ::

          mp = MyProcessor()
          for sig in sigldr('my_signal'):
              mp.proc(sig)
          print(mp.result())

        :param item: named item to iterate over and extract that data
        :returns: self to be able to iterate
        """
        if item not in self._args:
            raise KeyError
        self._idem = self._args[item]
        return self

    def __getitem__(self, item):
        """let's take out that item from bsig as we have it actually...

        :param item: named signal from SignalReader
        :returns: raw / unconverted signal
        """
        return self._bsig[item]

    def __contains__(self, item):
        """do we have some item inside us?

        :param item: the one to check
        """
        return item in self._args

    def __exit__(self, *_):
        """close down file (with support)"""
        self.close()

    def __del__(self):
        """in case someone forgot to call close"""
        self.close()

    def close(self):
        """close sig reader"""
        if self._bsig is not None:
            self._bsig.close()
            self._bsig = None
