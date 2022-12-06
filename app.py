from flask import Flask, request, render_template
import json
import boto3

client = boto3.client("textract", aws_access_key_id="ASIASGY4BHFD77SJRCWW",
                              aws_secret_access_key="aUwr+bUccSLJO4ZXuAHvkIROSBnVn3s7owdPa43E",aws_session_token="FwoGZXIvYXdzELb//////////wEaDD2G0V0sr8Q5oBBOgSLPAXup2I9uMUHYx39DOTlO01kWojYDUY9xe+dyF1p3wCMwQdKmDT9qz1h1vKlR5RsyJbVBnVGPHE/C9g+BcSA6kv3ShcgnjtyXtnc3+wcjyVzmrZrXOmrR/OzTXa97TBR95/JBUbAQQ7PD26Daeh8J+vKI1NTIvngwJT0EQqpEiJVlB4uRyrOEZkWMTOZ/AzCcvPBbwIUh2/nf3ZE7THSpL6Lim3prHLFMiQ/9SE4ujAgNH41SCBRrBNt8yhARfUiJPvDCa9/5iRNietQR2OHQEyij/6ycBjItY86uceB2/w/B6HX4cdvOX+p8YvbcPOc22U+AD28wHC573V4tJfa8ZyOyfx/Y", region_name="us-east-1")


app = Flask(__name__)


@app.route("/", methods=["GET"])
def main():
    return render_template("index.html", jsonData=json.dumps({}))


@app.route("/extract", methods=["POST"])
def extractImage():

    file = request.files.get("filename")
    binaryFile = file.read()
    response = client.detect_document_text(
        Document={
            "Bytes": binaryFile
        }
    )

    extractedText = ""

    for block in response['Blocks']:
        if block["BlockType"] == "LINE":
            # print('\033[94m' + item["Text"] + '\033[0m')
            extractedText = extractedText+block["Text"]+" "

    responseJson = {

        "text": extractedText
    }
    print(responseJson)
    return render_template("index.html", jsonData=json.dumps(responseJson))


app.run("0.0.0.0", port=5000, debug=True)
