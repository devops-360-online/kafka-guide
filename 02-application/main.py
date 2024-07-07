from flask import Flask, render_template, Response
from kafka import KafkaConsumer

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/topic/<topicname>')
def get_messages(topicname):
    consumer = KafkaConsumer(
        topicname,
        bootstrap_servers='172.20.255.240:9094', # Replace with svc Kafka external address `dev-cluster-kafka-external-bootstrap`
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='my-group'
    )
    
    def events():
        for message in consumer:
            yield f"data:{message.value.decode()}\n\n"
    return Response(events(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
