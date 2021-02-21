from Crypto.PublicKey import RSA
import json
import hashlib
import requests
import jsonpickle
import flask
import Article

CENTRAL_SERVER_ADDRESS = '35.225.55.196'
PORT = 5000

app = flask.Flask(__name__)


@app.route('/get_latest_blockchain', methods=['GET'])
def get_latest_blockchain():
    peer_address = requests.get('http://' + CENTRAL_SERVER_ADDRESS + ':' + str(PORT) + '/get_peer_addresses').json()[0]
    json_dict = json.loads(requests.get('http://' + peer_address + ':' + str(PORT) + '/get_blockchain').text.decode('utf-8'))
    json_dict.update({'py/object': 'Blockchain.Blockchain'})
    return json.dumps(json_dict)


@app.route('/generate_keys', methods=['GET'])
def generate_keys():
    key_pair = RSA.generate(bits=1024)
    key_pair_dict = {
        'e': key_pair.e,
        'd': key_pair.d,
        'n': key_pair.n
    }
    return json.dumps(key_pair_dict)


@app.route('/broadcast_article', methods=['POST'])
def broadcast_article():
    text = flask.request.args.get('text', None)
    e = flask.request.args.get('e', None)
    d = flask.request.args.get('d', None)
    n = flask.request.args.get('n', None)
    signature = pow(int.from_bytes(hashlib.sha512(str.encode(text)).digest(), byteorder='big'), d, n)
    article = Article.Article(text, signature, e, n)
    if not article.verify():
        return 'Not Valid'
    peer_address = requests.get('http://' + CENTRAL_SERVER_ADDRESS + ':' + str(PORT) + '/get_peer_addresses').json()[0]
    requests.post('http://' + peer_address + ':' + str(PORT) + '/new_article', data=jsonpickle.encode(article))
    return 'Valid'


if __name__ == '__main__':
    app.run(host='0.0.0.0')

