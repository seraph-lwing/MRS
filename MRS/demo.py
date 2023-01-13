from predict import predict
from pathlib import Path
import time

if __name__ == '__main__':
    txt = Path('lyrics_test.txt').read_text()
    start = time.time()
    predictions = predict(txt)
    print(f'time taken: {time.time()-start}')
    predictions.to_json('recommendations.json')
    print('recommendations can be found in the recommendations.json file as well')
    print('done')