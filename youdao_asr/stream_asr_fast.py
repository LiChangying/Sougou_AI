#!/usr/bin/python
import argparse
from ws4py.client.threadedclient import WebSocketClient
import time
import threading
import Queue
import json
import time
import hashlib
import uuid
import os
import sys, codecs
#sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

#app_key = 'zhudytest123'
#app_secret = 'youdaoapiv120171'
app_key = 'testKey1'
app_secret = 'youdaoapiv12017'


def rate_limited(maxPerSecond):
    minInterval = 1.0 / float(maxPerSecond)
    def decorate(func):
        lastTimeCalled = [0.0]
        def rate_limited_function(*args,**kargs):
            elapsed = time.clock() - lastTimeCalled[0]
            leftToWait = minInterval - elapsed
            if leftToWait>0:
                time.sleep(leftToWait)
            ret = func(*args,**kargs)
            lastTimeCalled[0] = time.clock()
            return ret
        return rate_limited_function
    return decorate


class MyClient(WebSocketClient):

    def __init__(self, audiofile, url, protocols=None, extensions=None, heartbeat_freq=None, byterate=32000,
                 save_adaptation_state_filename=None, send_adaptation_state_filename=None):
        super(MyClient, self).__init__(url, protocols, extensions, heartbeat_freq)
        self.final_hyps = []
        self.audiofile = audiofile
        self.byterate = byterate
        self.final_hyp_queue = Queue.Queue()
        self.save_adaptation_state_filename = save_adaptation_state_filename
        self.send_adaptation_state_filename = send_adaptation_state_filename

    @rate_limited(5)
    def send_data(self, data):
        self.send(data, binary=True)
        #print 'data sent',len(data)

    def opened(self):
        #print "Socket opened!"
        def send_data_to_ws():
            if self.send_adaptation_state_filename is not None:
                print >> sys.stderr, "Sending adaptation state from %s" % self.send_adaptation_state_filename
                try:
                    adaptation_state_props = json.load(open(self.send_adaptation_state_filename, "r"))
                    self.send(json.dumps(dict(adaptation_state=adaptation_state_props)))
                except:
                    e = sys.exc_info()[0]
                    print >> sys.stderr, "Failed to send adaptation state: ",  e
            # self.send('{"lang":"en"}')
            with self.audiofile as audiostream:
                for block in iter(lambda: audiostream.read(self.byterate/5), ""):
                    #print 'sending',self.byterate/20
                    self.send_data(block)

                    #sys.exit(0)
            print >> sys.stderr, "Audio sent, now sending end message"
            self.send_data('{\"end\": \"true\"}')

        t = threading.Thread(target=send_data_to_ws)
        t.start()


    def received_message(self, m):
        print 'received',str(m)


    def get_full_hyp(self, timeout=60):
        return self.final_hyp_queue.get(timeout)

    def closed(self, code, reason=None):
        #print "Websocket closed() called"
        #print >> sys.stderr
        self.final_hyp_queue.put(" ".join(self.final_hyps))
def encrypt(signStr):
    hash = hashlib.sha256()
    hash.update(signStr.encode('utf-8'))
    return hash.hexdigest()

def main():

    parser = argparse.ArgumentParser(description='Command line client for kaldigstserver')
    parser.add_argument('-u', '--uri', default="ws://openapi.youdao.com/stream_asropenapi", dest="uri", help="Server websocket URI")
    parser.add_argument('-r', '--rate', default=32000, dest="rate", type=int, help="Rate in bytes/sec at which audio should be sent to the server. NB! For raw 16-bit audio it must be 2*samplerate!")
    parser.add_argument('--lan', default="en", dest="langType", help="en or zh-CHS")
    parser.add_argument('--fast', default="false", dest="fast", help="false or true")
    parser.add_argument('--system', default="default", dest="system", help="default yd or hy")
    parser.add_argument('--save-adaptation-state', help="Save adaptation state to file")
    parser.add_argument('--send-adaptation-state', help="Send adaptation state from file")
    parser.add_argument('--content-type', default='', help="Use the specified content type (empty by default, for raw files the default is  audio/x-raw, layout=(string)interleaved, rate=(int)<rate>, format=(string)S16LE, channels=(int)1")
    parser.add_argument('audiofile', help="Audio file to be sent to the server", type=argparse.FileType('rb'), default=sys.stdin)
    args = parser.parse_args()

    content_type = args.content_type
    if content_type == '' and args.audiofile.name.endswith(".raw"):
        content_type = "audio/x-raw, layout=(string)interleaved, rate=(int)%d, format=(string)S16LE, channels=(int)1" %(args.rate/2)

    nonce = str(uuid.uuid1())
    curtime = str(int(time.time()))
    signStr = app_key + nonce + curtime + app_secret
    print(signStr)
    sign = encrypt(signStr)

    ws = MyClient(args.audiofile, args.uri + '?appKey=' + app_key + "&salt=" + nonce + "&curtime="
                  + curtime + "&sign=" + sign + "&fast=" + args.fast + "&system=" + args.system  + "&version=v1&channel=1&format=wav&signType=v4&rate=16000&langType="
                  + args.langType, byterate=args.rate,
                  save_adaptation_state_filename=args.save_adaptation_state, send_adaptation_state_filename=args.send_adaptation_state)
    ws.connect()
    result = ws.get_full_hyp()
    print result.encode('utf-8')
if __name__ == "__main__":
    main()

