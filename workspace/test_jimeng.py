import base64
import json
import http.client
from volcengine.visual.VisualService import VisualService

service = VisualService()
service.set_ak(os.environ.get('JIMENG_AK', 'YOUR_ACCESS_KEY'))
service.set_sk(os.environ.get('JIMENG_SK', 'YOUR_SECRET_KEY'))

# Submit task
resp = service.cv_sync2async_submit_task({
    'req_key': 'jimeng_t2i_v31',
    'prompt': 'A cute cat sitting on grass, realistic photo',
    'seed': -1,
    'width': 1024,
    'height': 1024
})

task_id = resp['data']['task_id']
print(f'Task ID: {task_id}')

# Wait for result
import time
time.sleep(8)

# Get result
result = service.cv_sync2async_get_result({
    'req_key': 'jimeng_t2i_v31',
    'task_id': task_id,
    'req_json': '{"return_url":true}'
})

# Save image
if result['data']['binary_data_base64']:
    img_data = result['data']['binary_data_base64'][0]
    img_bytes = base64.b64decode(img_data)
    with open(r'C:\Users\Administrator\Desktop\jimeng_test.jpg', 'wb') as f:
        f.write(img_bytes)
    print('Image saved to Desktop!')
else:
    print('No image data')
    print(result)
