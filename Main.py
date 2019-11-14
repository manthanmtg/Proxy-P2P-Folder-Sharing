from html_snips import *
from resp_header import get_header
from my_zipper import create_zip
import time
import urllib
from mimetypes import MimeTypes
import os


def main(connection, home_dir = os.environ['HOME']):
    data = connection.receive()
    if(data == ''):         # if the data received is empty don't proceed
        connection.close()
        return
    req_name = (data.split('\n')[0]).split(' ')[1].strip()
    curr_req_time = time.time()
    """
    if(req_name == prev_req_name
            and str(addr[0]) == str(prev_addr) 
            and (curr_req_time - prev_req_time) < 2):   # if the request is duplicate don't proceed
        connectionSocket.close()
        continue
    prev_req_name = req_name
    prev_req_time = curr_req_time
    prev_addr = addr[0]
    """
    
    connection.logger.info("Connection Accepted: Client: " + str(connection.clientAddr))
    # use the below print statement to print the request ( for debugging )
    # print(data)
    
    connection.logger.info("Requested  File: " + urllib.parse.unquote(req_name))
    # ? Check whether the request is to download
    if(req_name[-3:] == "get"):
        file_path = home_dir + urllib.parse.unquote(req_name[:-3])
        # print file path ( for debugging )
        # print("file Path: ", file_path)
        mime = MimeTypes()
        mime_type = mime.guess_type(file_path)[0]
        if(mime_type == None):
            mime_type = 'text/plain'
        # ? Check whether the request is directory
        if(os.path.isdir(file_path)):
            create_zip(file_path.split('/')[-1], file_path)
            data = ''
            with open(file_path.split('/')[-1] + '.zip', 'rb') as f:
                data = f.read()     # reading the file in the binary format
            zip_path = os.getcwd() + '/' + file_path.split('/')[-1] + ".zip"
            mime_type = mime.guess_type(zip_path)[0]
            if(mime_type == None):
                mime_type = 'text/plain'
            response = get_header(200, 'download', mime_type, os.path.getsize(zip_path), file_path.split('/')[-1] + ".zip").encode()
            response += data    # attaching the binary format of the text to the http response
            os.remove(zip_path)
        # ? Else it's not a direcrory, it's a file :)
        else:
            with open(file_path, "rb") as f:
                data = f.read()     # reading the file in the binary format
                response = get_header(200, 'download', mime_type, os.path.getsize(file_path), file_path.split('/')[-1]).encode()
                response += data    # attaching the binary format of the text to the http response
        # use the below print statement to print the statement ( for debugging )
        # print(response)
        connection.send(response)
        connection.logger.info("Request successfully served: Response Sent with the requested file atatched")
        connection.close()
        connection.logger.info("Connection Closed: Connection with client " + str(connection.clientAddr) + " closed")
        return

    curr_req_name = home_dir + urllib.parse.unquote(req_name)
    # ? Check whether the request is to list the contents of the directory
    resp_data = ""
    if(os.path.isdir(curr_req_name)):
        resp_data = html_start
        resp_data += """<div class="container"><div class="page-header"><h1> Here are the list of files </h1></div>"""
        resp_data += """<table class="table">"""
        resp_data += """<thead class="thead-dark"><tr><th scope="col">File/Dir</th><th scope="col">Action</th></tr></thead><tbody>"""
        resp_data += html_end
        for content in os.listdir(curr_req_name):
            curr_full_path = curr_req_name.rstrip('/') + '/' + content
            # for debugging
            # print(curr_full_path)
            # ? Check whether it is a file
            #if(os.path.isfile(curr_full_path)):
            resp_data += "<tr>" + """<td><a href = "{}">""".format(curr_full_path.replace(home_dir, "", 1)) +  content + """</a></td>""" + """<td><a href="{}get" target="_blank">""".format(curr_full_path.replace(home_dir, "", 1)) + """GET</a></td>""" + "</tr>"
            #else:
            # resp_data += "<li>" + """<a href = "{}">""".format(curr_full_path.replace("/home/manthanby", "", 1)) +  content + """</a>""" + """ Download """ +  """<a href="{}get" target="_blank">""".format(curr_full_path.replace("/home/manthanby", "", 1)) + """GET</a>""" + "</li>"
        resp_data += "</tbody></table></div>"        
    if(os.path.isfile(curr_req_name)):
            with open(curr_req_name, 'r') as f:
                try:
                    resp_data = f.read()
                except:
                    resp_data = "Can't read the file: Please download using GET"
    response = get_header(200).encode() + bytes(resp_data, 'utf-8')
    connection.send(response)
    connection.logger.info("Request successfully served: Resposne Sent with the requested file atatched")
    # use the below print statement for printing the response ( for debugging )
    # print('=== Response ===')
    # print(response)
    connection.close()
    connection.logger.info("Connection Closed: Connection with client " + str(connection.clientAddr) + " closed")
    return
    # print("\n------- " + str(times) + " ------ Connection Closed ----------------\n")