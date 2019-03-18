import ussl
import usocket

def urlinfo(url):
    try:
        proto, dummy, host, path = url.split("/", 3)
    except ValueError:
        proto, dummy, host = url.split("/", 2)
        path = ""
    if proto == "http:":
        port = 80
    elif proto == "https:":
        import ussl
        port = 443
    else:
        raise ValueError("Unsupported protocol: " + proto)

    if ":" in host:
        host, port = host.split(":", 1)
        port = int(port)

    return (proto, dummy, host, path, port)

def cwifi():
    from wifi import Wifi
    w = Wifi()
    w.active(True)
    w.connect()

def send_get_request(socket, host, path, headers={}):
    socket.write(b"%s /%s HTTP/1.0\r\n" % ("GET", path))
    socket.write(b"Host: %s\r\n" % host)
    # write header
    if headers:
        for k in headers:
            s.write(k)
            s.write(b": ")
            s.write(headers[k])
            s.write(b"\r\n")
    socket.write(b"\r\n")

def download_from_url(url, filepath):
    """
    使用http GET协议，从一个url中下载文件到指定文件位置
    """
    proto, dummy, host, path, port = urlinfo(url)
    ai = usocket.getaddrinfo(host, port, 0, usocket.SOCK_STREAM)
    if len(ai) == 0:
        raise ValueError("No network")

    ai = ai[0]

    print('urlinfo ===>', proto, dummy, host, path, port)

    print('ai ===>', ai)
    print('ai ===>', ai)
    print('ai ===>', ai)

    s = usocket.socket(ai[0], ai[1], ai[2])

    try:
        s.connect(ai[-1])
        if proto == "https:":
            s = ussl.wrap_socket(s, server_hostname=host)

        send_get_request(s, host, path, headers={})

        l = s.readline()
        print('first line of response ===>',l)
        l = l.split(None, 2)
        status = int(l[1])
        reason = ""
        print('status==>', status)

        if len(l) > 2:
            reason = l[2].rstrip()
            print('reason==>', reason)
        while True:
            l = s.readline()
            print('content==>', l)
            if not l or l == b"\r\n":
                break
            #print(l)
            if l.startswith(b"Transfer-Encoding:"):
                if b"chunked" in l:
                    raise ValueError("Unsupported " + l)
            elif l.startswith(b"Location:") and not 200 <= status <= 299:
                raise NotImplementedError("Redirects not yet supported")
    except Exception:
        raise
    finally:
        s.close()



