import time
def get_header(status_no, type = 'default', mime_type = '', content_length = 0, file_name = ''):
    header = ''
    if(status_no == 200 and type == 'default'):
        header += 'HTTP/1.1 200 OK\n'
        time_now = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
        header += 'Date: {now}\n'.format(now=time_now)
        header += 'Server: AAM-Server\n'
        header += 'Connection: close\n\n'
        
    if(status_no == 200 and type == 'download'):
        header += 'HTTP/1.1 200 OK\n'
        time_now = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
        header += 'Date: {now}\n'.format(now=time_now)
        header += 'Content-disposition: attachment; filename=' + file_name + '\n'
        header += 'Server: AAM-Server\n'
        header += 'Content-Type: ' + mime_type + '\n'
        header += 'Content-Length: ' + str(content_length) + '\n'
        header += 'Connection: close\n\n'
        print(file_name)
        
        
    if(status_no == 404):
        header += 'HTTP/1.1 404 Not Found\n'
        time_now = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
        header += 'Date: {now}\n'.format(now=time_now)
        header += 'Server: AAM-Server\n'
        header += 'Connection: close\n\n'
    return header
