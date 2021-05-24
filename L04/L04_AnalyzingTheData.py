#Sean Blanchard
#2/28/2021
#Lab 4 429

import json

data_file = 'harhar\\com.deitycomponents.har'
with open(data_file, encoding='utf-8') as f:
    jdata = json.load(f)

    total_load_time = str(jdata['log']['entries'][0]['request']['url']) + " took " + str(
        jdata['log']['pages'][0]['pageTimings']['onLoad']) + ' ms to load.'

    #median_number_of_requests = str(jdata['log']['entries'][0]['request']['url']) + " has " + str(jdata['log']['entries'][0]['request']['headersSize']) + ' Header Size'
    #print(median_number_of_requests)

ContentLoadTime = jdata['log']['pages'][0]['pageTimings']['onContentLoad']
fileName = str(jdata['log']['entries'][0]['request']['url'])
requestTotal = 0
responseTotal = 0
timingTotal = 0
http1Counter = 0
http2Counter = 0
http1RequestCounter = 0
http2RequestCounter = 0
headers = {'Largest request header': 0, 'Average request header': 0}
loadTime = {'Average Load Time': 0, 'Minimum Load Time': 0, 'Largest Load Time': 0}
responseSize = {'Total Response Size': 0, 'Average Response Size': 0}
lengthOfReturnedContent = {'Length Of Returned Content': 0}


for entry in jdata['log']['entries']:

    if 'request' in entry:
        requestTotal += 1
        size = entry['request']['headersSize']
        headers['Average request header'] += size
        if size > headers['Largest request header']:
            headers['Largest request header'] = size

    if 'response' in entry:
        responseTotal += 1
        headerSize = entry['request']['headersSize']
        bodySize = entry['request']['bodySize']
        totalResponseSize = headerSize + bodySize
        responseSize['Average Response Size'] += totalResponseSize
        if totalResponseSize > responseSize['Total Response Size']:
            responseSize['Total Response Size'] = totalResponseSize

    #HTTP total counter
    if 'response' in entry:
        if entry['request']['httpVersion'] == 'HTTP/1.1':
            http1Counter += 1
        if entry['response']['httpVersion'] == 'HTTP/1.1':
            http1Counter += 1
        if entry['request']['httpVersion'] == 'HTTP/2':
            http2Counter += 1
        if entry['response']['httpVersion'] == 'HTTP/2':
            http2Counter += 1
        totalHttpCounter = http1Counter + http2Counter

    #HTTP request counter
    if 'response' in entry:
        if entry['request']['httpVersion'] == 'HTTP/1.1':
            http1RequestCounter += 1
        if entry['request']['httpVersion'] == 'HTTP/2':
            http2RequestCounter += 1
        totalHttpRequestCounter = http1RequestCounter + http2RequestCounter

    if 'timings' in entry:
        timingTotal += 1
        size = entry['time']
        loadTime['Average Load Time'] += size
        if size > loadTime['Largest Load Time']:
            loadTime['Largest Load Time'] = size
        if size < loadTime['Minimum Load Time']:
            loadTime['Minimum Load Time'] = size


#for key in averageTiming:
#    averageTiming[key] /= timingTotal

#CALCULATIONS

loadTime['Average Load Time'] /= timingTotal

responseSize['Average Response Size'] /= responseTotal

headers['Average request header'] /= requestTotal

percentageHttp = totalHttpCounter / (requestTotal + responseTotal)

percentageHttp1request = http1RequestCounter / totalHttpRequestCounter

percentageHttp2request = http2RequestCounter / totalHttpRequestCounter


# PRINT STATEMENTS

print(total_load_time)

print(f'\n{fileName} took {ContentLoadTime} ms to load Content.')

print(f'\nThere were {requestTotal + responseTotal} requests/responses')
print()

#PRINT FOR REQUEST SIZE
for key, value in responseSize.items():
    print(f'{key} are {value} bytes')
print()

#PRINT FOR PERCENTAGE OF URLS using HTTPS
print(f'The percentage of URLs using HTTP is {percentageHttp}%')
print()

#PRINT PERCENTAGE OF HTTP1.1 requests
print(f'The percentage of requests over HTTP/1.1 is {percentageHttp1request}%')
print(f'The percentage of requests over HTTP/2 is {percentageHttp2request}%')
print()

#PRINT FOR MAX LOAD TIME
for key, value in loadTime.items():
    print(f'{key} takes {value} ms')
#print(headers.items())
print()

#HEADERS
for key, value in headers.items():
    print(f'{key} : {value} bytes')
print()




