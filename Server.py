from cgi import print_arguments
from http.server import SimpleHTTPRequestHandler, HTTPServer
import imp
import json
from threading import Thread
from web3 import Web3
import time
from urllib import response
from Swapmotor import SWAP
import threading
import Prices as db
import RSIst as rsi
INTERFACE = '127.0.0.1'
PORT = 5001
keys=[1]
dic_valus={}

# This class will handle any incoming GET requests
# URLs starting with /api/ is catched for REST/JSON calls
# Other URLs are handled by default handler to serve static
# content (directories, files)

class RequestHandler(SimpleHTTPRequestHandler):

    # Override handler for GET requests
    def do_GET(self):

        if self.path.startswith('/api'):
            self.send_response(200)
            self.send_header('Content-type', 'text/json')
            self.end_headers()
            if self.path.startswith('/api/slump'):     

    #             result: int = [1, 2, 3]
    #             self.wfile.write(json.dumps(result).encode())
                 return
    #         else:
    #             response = "WRONG"
    #             self.wfile.write(json.dumps(response).encode())
    #             return

    #     # Call default serving static files if not '/api'
    #     # from 'html' subdirectory
        self.path = '/html' + self.path
        return super().do_GET()
        

    def bot(self):
                out_db=False

                content_len = int(self.headers['content-length'])
                post_body = self.rfile.read(content_len)
                test_data = json.loads(post_body)
                data = test_data
                print(data)

                firstprice = float(db.pairPrice(data['from'],data['till']))
                trade = SWAP()
                key= str(data['sympol']+data['tosympol'])
                if(data['strategi']=='rsi'):
                    for i in keys:
                        if key == i:
                            out_db = False
                            break
                        elif (i == keys[-1]):
                            dic_valus.update({key:None})
                            print(key, "==", i)
                            print("append")
                            keys.append(key)
                            out_db = True
                            break


                if data['till'] == '0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c':
                    rsivalues=[1]
                    print("This swap is from a ",data['sympol']," to BNB") 
                    print(threading.currentThread().getName())                  
                    while True:
                        print("first price is : " , firstprice )
                        if data['strategi']=='rsi':


                            if (out_db == True):
                                print(dic_valus)
                                rsival = rsi.rsivalue(data['from'], data['till'], key)
                                dic_valus.update({key: rsival})

                            else:
                                print("New thread for existed tokens ")
                                print(dic_valus)
                                if dic_valus[key] is None:
                                    time.sleep(90)
                                    continue
                                rsival = dic_valus[key]
                                # lastprice = float(db.pairPrice(data['from'], data['till']))
                                # print("last price is : " , lastprice )
                                # if(lastprice >= firstprice + 0.0005):
                            if rsival == False:
                                trade.swaping(data['user_address'], data['from'], data['till'], data['inamount'],
                                              data['tosympol'])
                                # firstprice=lastprice
                                # elif(lastprice <= firstprice -0.0005):

                            else:
                                price = float(db.pairPrice(data['from'], data['till']))
                                actualamount = price * data['inamount']
                                trade.sell(data['user_address'], data['till'], data['from'], actualamount,
                                           data['tosympol'])
                            # firstprice=lastprice
                            # time.sleep(15)
                        elif data['strategi']=='timing':
                            price = float(db.pairPrice(data['from'], data['till']))
                            actualamount = price * data['inamount']

                            trade.swaping(data['user_address'],data['from'],data['till'], data['inamount'], data['tosympol'])
                            time.sleep(30)
                            trade.sell(data['user_address'],data['till'],data['from'], actualamount, data['tosympol'])
                            time.sleep(30)

                       
                elif data['from'] == '0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c':
                    rsivalues=[1]
                    print("this is from BNB to ",data['sympol'])
                    print(threading.currentThread().getName())
                    while True:                        
                        print("first price is : " , firstprice )
                        if data['strategi']=='rsi':

                            if (out_db == True):
                                print(dic_valus)
                                rsival = rsi.rsivalue(data['from'], data['till'], key)
                                dic_valus.update({key: rsival})

                            else:
                                print("New thread for existed tokens ")
                                print(dic_valus)
                                if dic_valus[key] is None:
                                    time.sleep(90)
                                    continue
                                rsival = dic_valus[key]
                                # lastprice = float(db.pairPrice(data['from'], data['till']))
                                # print("last price is : " , lastprice )
                                # if(lastprice >= firstprice + 0.0005):
                            if rsival == False:
                                trade.sell(data['user_address'], data['from'], data['till'], data['inamount'],
                                           data['tosympol'])
                                # firstprice=lastprice
                                # elif(lastprice <= firstprice -0.0005):

                            else:
                                price = float(db.pairPrice(data['from'], data['till']))
                                actualamount = price * data['inamount']
                                trade.swaping(data['user_address'], data['from'], data['till'], actualamount,
                                              data['tosympol'] )
                            # firstprice=lastprice
                            # time.sleep(15)
                        elif data['strategi']=='timing':
                            price = float(db.pairPrice(data['from'], data['till']))
                            actualamount = price * data['inamount']

                            trade.sell(data['user_address'], data['from'], data['till'], data['inamount'], data['tosympol'])
                            time.sleep(30)
                            trade.swaping(data['user_address'], data['from'], data['till'], actualamount,data['tosympol'])
                            time.sleep(30)







                else:
                    print ("this swap is from", data['sympol'], " to ",data['tosympol'] )
                    print(threading.currentThread().getName())
                    while True:
                        if data['strategi'] == 'rsi':

                            if (out_db == True):
                                print(dic_valus)
                                rsival = rsi.rsivalue(data['from'], data['till'], key)
                                dic_valus.update({key: rsival})

                            else:
                                print("New thread for existed tokens ")
                                print(dic_valus)
                                rsival = dic_valus[key]
                                if dic_valus[key] is None:
                                    time.sleep(90)
                                    continue
                                
                                # lastprice = float(db.pairPrice(data['from'], data['till']))
                                # print("last price is : " , lastprice )
                                # if(lastprice >= firstprice + 0.0005):
                            if rsival == False:
                                trade.swapOtherTokens(data['user_address'], data['from'], data['till'],
                                                      data['inamount'], data['tosympol'])

                                # firstprice=lastprice
                                # elif(lastprice <= firstprice -0.0005):

                            else:
                                price = float(db.pairPrice(data['from'], data['till']))
                                actualamount = price * data['inamount']
                                trade.swapOtherTokens(data['user_address'], data['till'], data['from'], actualamount,
                                                      data['tosympol'])

                            # firstprice=lastprice
                            # time.sleep(15)
                        elif data['strategi'] == 'timing':
                            price = float(db.pairPrice(data['from'], data['till']))
                            actualamount = price * data['inamount']

                            trade.swapOtherTokens(data['user_address'], data['from'], data['till'], data['inamount'],
                                                  data['tosympol'])
                            time.sleep(30)
                            trade.swapOtherTokens(data['user_address'], data['till'], data['from'], actualamount,
                                                  data['tosympol'])
                            time.sleep(30)


    def do_POST(self):
        thread = Thread(target=self.bot, daemon=True)
        thread.start()

try:
    # Create a web server and define the handler to manage the
    # incoming request
    server = HTTPServer((INTERFACE, PORT), RequestHandler)
    print('Starting HTTP server on http://' + INTERFACE + ":" + str(PORT))
    server.serve_forever()
except KeyboardInterrupt:
    print('Ctrl-C received, shutting down the web server')
    server.socket.close().py

