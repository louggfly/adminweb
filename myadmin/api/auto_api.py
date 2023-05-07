from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import paddlehub as hub
import torch
from transformers import BertConfig, BertForSequenceClassification, BertTokenizer
import torch.nn.functional as F


class SentaAutoScore(APIView):
    @staticmethod
    def post(request):
        input = request.data.get('input')
        senta = hub.Module(name="senta_bilstm")
        input_dict = {"text": [input]}
        results = senta.sentiment_classify(data=input_dict)
        positive_probs = results[0]['positive_probs']
        print(positive_probs)
        return Response({'score': positive_probs}, status=status.HTTP_200_OK)


class BertAutoScore(APIView):
    @staticmethod
    def post(request):
        input = request.data.get('input')
        result = predict(input)
        return Response({'score': result}, status=status.HTTP_200_OK)


def to_input_id(sentence_input):
    tokenizer = BertTokenizer(vocab_file='myadmin/api/cache/vocab.txt')
    return tokenizer.build_inputs_with_special_tokens(
        tokenizer.convert_tokens_to_ids(tokenizer.tokenize(sentence_input)))


def predict(text):
    model = BertForSequenceClassification.from_pretrained('myadmin/api/cache', local_files_only=True)
    model.eval()
    sentence = text
    input_id = to_input_id(sentence)
    assert len(input_id) <= 512
    input_ids = torch.LongTensor(input_id).unsqueeze(0)
    outputs = model(input_ids)
    prediction = torch.max(F.softmax(outputs[0], dim=-1), dim=1)[1]
    predict_label = prediction.data.cpu().numpy().squeeze()
    result = predict_label
    return result
