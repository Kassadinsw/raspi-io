# -*- coding: utf-8 -*-
import base64
from .client import RaspiWsClient
from .setting import get_server_port
from .core import RaspiBaseMsg, RaspiAckMsg
__all__ = ['SerialInit', 'SerialClose', 'SerialRead', 'SerialWrite', 'SerialFlush', 'Serial']


class SerialInit(RaspiBaseMsg):
    _handle = 'init'
    _properties = {'port', 'baudrate', 'bytesize', 'parity', 'stopbits', 'timeout'}

    def __init__(self, **kwargs):
        super(SerialInit, self).__init__(**kwargs)


class SerialClose(RaspiAckMsg):
    _handle = 'close'
    _properties = {'port'}

    def __init__(self, **kwargs):
        super(SerialClose, self).__init__(**kwargs)


class SerialRead(RaspiBaseMsg):
    _handle = 'read'
    _properties = {'size'}

    def __init__(self, **kwargs):
        super(SerialRead, self).__init__(**kwargs)


class SerialWrite(RaspiBaseMsg):
    _handle = 'write'
    _properties = {'data'}

    def __init__(self, **kwargs):
        super(SerialWrite, self).__init__(**kwargs)


class SerialFlush(RaspiBaseMsg):
    IN = 1
    OUT = 2
    BOTH = 3
    _handle = 'flush'
    _properties = {'where'}

    def __init__(self, **kwargs):
        super(SerialFlush, self).__init__(**kwargs)


class Serial(RaspiWsClient):
    PATH = __name__.split(".")[-1]

    def __init__(self, host, port, baudrate, bytesize=8, parity='N', stopbits=1, timeout=1, verbose=1):
        """Raspi Ws Serial

        :param host: raspi io server address
        :param port: serial port name, such as /dev/ttyUSB0
        :param baudrate: serial port baudrate
        :param bytesize: serial port bytesize
        :param parity: serial port parity
        :param stopbits:serial port stopbits
        :param timeout: serial port read timeout
        """
        super(Serial, self).__init__((host, get_server_port(host, self.PATH, port)), timeout * 2, verbose)
        self.__port = port
        self.__opened = False
        ret = self._transfer(SerialInit(
            port=port, baudrate=baudrate, bytesize=bytesize, parity=parity, stopbits=stopbits, timeout=timeout))
        self.__opened = ret.ack if isinstance(ret, RaspiAckMsg) else False
        if not self.is_open():
            raise RuntimeError(ret.data)

    def __del__(self):
        self.close()

    def is_open(self):
        return self.__opened

    def close(self):
        if self.is_open():
            ret = self._transfer(SerialClose(port=self.__port))
            self.__opened = False if isinstance(ret, RaspiAckMsg) and ret.ack else self.__opened

    def read(self, size=1):
        """Read data from serial port

        :param size: read size
        :return: result, data or error
        """
        ret = self._transfer(SerialRead(size=size))
        return self._decode(ret.data) if isinstance(ret, RaspiAckMsg) and ret.ack else ""

    def write(self, data):
        """Write data to serial port

        :param data: write data
        :return: result, error or write length
        """
        ret = self._transfer(SerialWrite(data=self._encode(data)))
        return ret.data if isinstance(ret, RaspiAckMsg) and ret.ack else -1

    def flush(self):
        self._transfer(SerialFlush(where=SerialFlush.BOTH))

    def flushInput(self):
        self._transfer(SerialFlush(where=SerialFlush.IN))

    def flushOutput(self):
        self._transfer(SerialFlush(where=SerialFlush.OUT))
