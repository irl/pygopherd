import unittest
from io import BytesIO
from pygopherd.protocols import ProtocolMultiplexer
from pygopherd import testutil
import pygopherd.protocols

class ProtocolMultiplexerTestCase(unittest.TestCase):
    def setUp(self):
        self.config = testutil.getconfig()

    # Just a bunch of test cases for each different protocol -- make
    # sure we find the right one.

    def getproto(self, request):
        rfile = BytesIO(request)
        wfile = BytesIO()
        handler = testutil.gettestinghandler(rfile, wfile,
                                             self.config)
        return ProtocolMultiplexer.getProtocol(file.readline(),
                                               handler.server,
                                               handler,
                                               handler.rfile,
                                               handler.wfile,
                                               self.config)

    def testGoToGopher(self):
        assert isinstance(testutil.gettestingprotocol(b"/gopher0-request.txt\n"), pygopherd.protocols.rfc1436.GopherProtocol)

    def testGoToHTTP(self):
        assert isinstance(testutil.gettestingprotocol(b"GET /http-request.txt HTTP/1.0\n\n"),
                          pygopherd.protocols.http.HTTPProtocol)

    def testGoToGopherPlus(self):
        assert isinstance(testutil.gettestingprotocol(b"/gopher+-request.txt\t+\n"),
                          pygopherd.protocols.gopherp.GopherPlusProtocol)
    
