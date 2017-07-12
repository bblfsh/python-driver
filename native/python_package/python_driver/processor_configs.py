import sys
from python_driver.requestprocessor import RequestProcessorJSON

ProcessorConfigs = {
        'json': {
            'class': RequestProcessorJSON,
            'inbuffer': sys.stdin,
            'outbuffer': sys.stdout
        },
}
