# real-state-ml-pipeline

Para fazer insert no MySQL a partir de um arquivo .csv:

```bash
curl -X POST "http://localhost:8000/properties/from-csv/" -F "file=@data/train.csv"
```

É esperado o seguinte retorno com a execução:

```bash
{
    "message":"16212 properties inserted successfully"
}
```

Para executar a componente de treino do modelo:

```bash
curl -X GET http://localhost:8001/train
```

É esperado o seguinte retorno:

```bash
{
    "message":"Model trained and saved successfully"
}
```
