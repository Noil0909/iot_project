from common import response_html
async def mainHandle(request):
    return response_html('index.html')
async def temperatureHandle(request):
    return response_html('temperature.html')        
async def smarthomeHandle(request):
    return response_html('smarthome.html')